## Docker Security

Containers feel like neat little sandboxes, yet they still share the host kernel. That subtle detail means a mis-configured image can claw its way out, so defence in depth becomes essential rather than optional. A handy mental model is the classic risk equation \$R = L \times I\$, where \$L\$ represents the likelihood of compromise and \$I\$ the impact; our goal is to drive either factor—preferably both—toward zero through layered safeguards.

```
+--------------------+
|  Application code  |
+--------------------+
|   Container image  |
+--------------------+
| Namespaces/Cgroups |
+--------------------+
|     Host kernel    |
+--------------------+
|     Hardware       |
+--------------------+
```

Even though each box looks isolated, a vulnerability in any layer can pierce everything beneath it, which is why attention to detail pays dividends.

## Hardening the host and daemon

Before tweaking container flags, start by reducing the daemon’s own attack surface. Running the engine as a **rootless** service stops most privilege-escalation tricks in their tracks. Mapping UIDs with `--userns-remap` or installing Docker in rootless mode keeps file ownership tidy and obstructs host-level write attempts. Seccomp, AppArmor, and SELinux profiles form the next barrier, blocking dangerous syscalls or filesystem paths even if a process gains extra tokens. Docker 25.0 refreshes the built-in seccomp profile to cover Linux 6 .x syscalls, closing gaps that had opened as kernels evolved. ([Docker Documentation][1])

```bash
docker info --format '{{json .SecurityOptions}}'
```

```
["name=seccomp,profile=default","name=apparmor","name=selinux"]
```

Listing active security options quickly shows whether the daemon is enforcing policies; an empty array would suggest that seccomp or AppArmor never loaded, which is a red flag.

### Seccomp, AppArmor, SELinux quick reference

| Mechanism | What it does                                        | Typical tuning method                   |
| --------- | --------------------------------------------------- | --------------------------------------- |
| Seccomp   | Filters individual syscalls                         | `--security-opt seccomp=profile.json`   |
| AppArmor  | Restricts file and network access by path           | `--security-opt apparmor=myprofile`     |
| SELinux   | Labels processes and resources with mandatory rules | `--security-opt label:type:container_t` |

Combining the three feels like placing lock, bar and alarm on the same door: redundant yet reassuring.

## Image provenance and supply-chain integrity

Images downloaded straight from the internet resemble unsigned email attachments. Content Trust uses Notary signatures to guarantee an image’s digest, while Software Bills of Materials (SBOMs) document every package inside for later scanning. The CLI now ships with `docker sbom`, powered by Syft, so generating an SPDX or CycloneDX document is as simple as one command. ([Anchore][2]) BuildKit can even embed the SBOM during `docker buildx build --sbom=true`, creating a tamper-evident trail from source to registry. ([Docker][3])

```bash
docker sbom alpine:3.20
```

```
Syft v0.90.0

 ✔ Loaded image
 ✔ Parsed image
 ✔ Cataloged packages      [111 packages]

alpine:3.20 (docker-img)
├── musl@1.2.5-r1
├── busybox@1.36.1-r0
└── ...
```

The command surfaces every library in the image, which feeds neatly into vulnerability scanners or compliance reports.

```bash
docker buildx build --sbom=true -t myorg/web:1.0 --push .
```

```
#5 exporting to image
#5 exporting layers
#5 exporting SBOM
#5 pushing layers 7.1s done
```

Confirming that the build pipeline pushed an SBOM alongside the layers means any downstream consumer can verify contents without rebuilding.

## Runtime least-privilege patterns

Running as PID 1 inside a container grants no special capability by default, yet many images pile on extras they never use. Dropping everything with `--cap-drop ALL` and then selectively re-adding, or running with a read-only filesystem, turns potential exploits into harmless log entries.

| Flag                  | Purpose                                 | Default                  |
| --------------------- | --------------------------------------- | ------------------------ |
| `--cap-drop`          | Remove one or more Linux capabilities   | None dropped             |
| `--cap-add`           | Add capabilities back selectively       | Inherited from base list |
| `--read-only`         | Mount root filesystem as read-only      | Read–write               |
| `--no-new-privileges` | Block `setuid` binaries from escalating | Off                      |

```bash
docker run --cap-drop ALL --read-only -d nginx:alpine
```

```
Unable to update /var/cache/nginx: Read-only file system
```

The warning reminds you that health checks writing to disk will fail, prompting either a writable volume mount or a stateless check; that awareness stops surprises in production.

## Network boundaries and secrets

User-defined bridge networks isolate containers at the virtual switch, acting like private VLANs on the same host. Overlay networks stretch that idea across Swarm nodes and encrypt traffic in transit. Secrets, introduced in Swarm and mirrored in Docker Compose v3, stay in tmpfs and never touch the image layers, preventing accidental pushes of API keys.

```bash
docker network inspect app_net --format '{{json .IPAM.Config}}'
```

```
[{"Subnet":"172.18.0.0/16","Gateway":"172.18.0.1"}]
```

Verifying CIDR ranges avoids collisions with corporate networks, a subtle cause of connectivity failures that masquerade as security blocks.

## Auditing, monitoring and incident response

The `docker events` stream covered earlier doubles as an audit bus: every exec, attach, pull and push lands there. Feeding that stream into SIEM tooling satisfies “who did what, when” clauses in many compliance frameworks. Pair it with machine-readable SBOMs and CVE feeds, and you end up with real-time guardrails instead of quarterly checkbox exercises.

```bash
docker events --filter event=exec_create --since 24h
```

```
2025-05-04T06:17:21Z container exec_create  cmd=["/bin/sh"]
```

Interpretation: spotting unexpected `exec` attempts outside maintenance windows could indicate lateral movement by an attacker or a misfired automation script.

## Quick checklist for everyday hardening

Thinking shorter thoughts during a deploy often prevents longer nights during an incident.

* Confirm the daemon runs in rootless or user-namespace mode.
* Enable the default seccomp profile and load AppArmor or SELinux on boot.
* Sign images with Content Trust and attach an SBOM before pushing to the registry.
* Run containers as non-root users, drop unused capabilities, mount filesystems read-only when possible.
* Place services on least-exposed networks, publish only required ports and use TLS proxies for external traffic.
* Stream `docker events` into your logging pipeline and alert on unusual actions.
