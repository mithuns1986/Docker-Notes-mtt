## Docker Networking

Underneath every running container a tiny, software-defined network card passes packets around much like copper in an old data-centre rack. Docker hides the cabling, switches and routers, yet the picture is still helpful: containers have virtual Ethernet interfaces; those interfaces plug into a virtual switch created by Docker; the switch in turn peers with the host’s real NIC or with other hosts through VXLAN tunnels. Once that mental diagram clicks, the CLI options start to feel like rack-diagrams instead of random flags.

Sketch of the default bridge network:

```
+------------+          +---------------+
| containerA |--eth0----|               |
+------------+          |   docker0     |--- host NIC ---> Internet/LAN
+------------+          |  (bridge)     |
| containerB |--eth0----|               |
+------------+          +---------------+
```

### Network Drivers

Drivers decide how packets travel. The default **bridge** driver keeps traffic local to one machine. **Overlay** stretches a virtual L2 segment across a Swarm or Kubernetes cluster by hiding UDP-encapsulated packets inside VXLAN. **Host** removes isolation entirely so the container shares the host stack, trading security for raw speed. **Macvlan** lets a container masquerade as a first-class device on the physical LAN, perfect for boxes that insist on static IPs. Finally **none** disables networking altogether, handy when you need a compute sandbox with zero packet leaks.

- **Bridge**:
    - The go-to default network driver when you initialize a Docker container.
    - Facilitates communication between containers residing on the same host.
    - Provides a security layer by isolating the container network from the host by default.
    - Each container gets its own internal IP, and any required ports can be mapped to the host.

- **Host**:
    - A step away from isolation — this driver integrates the container's network stack directly with the Docker host.
    - Can prove to be helpful in scenarios where network performance is paramount and the slight compromise in isolation can be afforded.
    - Containers can share the host's IP, eliminating the need for port mapping.

- **Overlay**:
    - A specialized driver tailored for scenarios involving multiple Docker daemons, typically seen in Docker Swarm deployments.
    - It builds a decentralized network among the daemons, paving the way for container-to-container traffic, even if they are on disparate hosts.
    - Implements VXLAN to encapsulate traffic.

- **Macvlan**:
    - With the Macvlan driver, each container gets its own dedicated MAC address. This makes the container's virtual network interface mimic a physical one on the network.
    - It finds its utility in scenarios requiring the containerization of applications that are hardcoded with static IP addresses.
    - Multiple containers can be mapped to the same physical network interface without causing MAC address conflicts.


| Driver  | Typical use-case                 | Isolation level | Notes                                      |
| ------- | -------------------------------- | --------------- | ------------------------------------------ |
| bridge  | Stand-alone hosts, local dev     | Namespace-based | NATs outbound traffic                      |
| overlay | Swarm services, mesh networks    | Cross-host      | Requires key-value store or built-in Swarm |
| host    | High-performance network tools   | None            | Container sees host ports directly         |
| macvlan | Legacy systems needing static IP | Per-VLAN        | Needs physical NIC in promiscuous mode     |
| none    | Batch jobs with no network need  | Full            | No interface except loopback               |

### Network Modes

When working with Docker, understanding its diverse network modes can assist in effectively deploying and communicating with containers. Here's an in-depth overview:

#### Host Mode
In this mode, containers completely share the host's network stack.

```
+----------------------------------------------------------------------------+
|                                 Host Machine                               |
|                                                                            |
|         +---------------------+   +---------------------+                  |
|         |                     |   |                     |                  |
|         |     Container A     |   |     Container B     |                  |
|         |                     |   |                     |                  |
|         +---------------------+   +---------------------+                  |
|                                                                            |
|                    |                                    |                  |
|                    |                                    |                  |
|      Host IP: 192.168.1.10                Host IP: 192.168.1.10            |
|                    |                                    |                  |
|                    +----------------+-------------------+                  |
|                                     |                                      |
|                                     | Host's Physical NIC                  |
|                                     |                                      |
|                                     |                                      |
|                                     +--------------------------------------+
|                                             |                              |
|                                             |                              |
|                                       External Network                     |
|                                             |                              |
+----------------------------------------------------------------------------+
```

- Containers and the host share the exact IP address (e.g., 192.168.1.10).
- Network ports are shared between the host and the containers. Thus, if a service inside Container A listens on port 80, it's as though the host itself listens on port 80.
- No port mapping or NAT is necessary since the container directly uses the host's network.
- Offers performance benefits since there's no intermediary bridge, but it does compromise the container isolation principle.
- Ensuring no port clashes between host services and container services is crucial.

#### Bridge Mode (default)
Containers obtain an IP from an internal private range, and they communicate with the outer world via NAT (Network Address Translation).

```
+----------------------------------------------------------------------------+
|                                 Host Machine                               |
|                                                                            |
|       +------------------+       +-----------------+                       |
|       |                  |       |                 |                       |
|       |    Container A   |       |   Container B   |                       |
|       |                  |       |                 |                       |
|       +--------+---------+       +-------+---------+                       |
|                |                         |                                 |
|                |  172.17.0.2             |  172.17.0.3                     |
|                |                         |                                 |
|      +---------+----------+    +---------+---------+                       |
|      |                    |    |                   |                       |
|      | Docker0 Bridge     +----+                   |                       |
|      |    Network         |    |                   |                       |
|      |                    |    |                   |                       |
|      +---------+----------+    +---------+---------+                       |
|                |                         |                                 |
|       Host IP: 192.168.1.10   Host IP: 192.168.1.10                        |
|                |                         |                                 |
|                +------------+------------+                                 |
|                             |                                              |
|                             | Host's Physical NIC                          |
|                             |                                              |
|                             |                                              |
|                             +----------------------------------------------+
|                                     |                                      |
|                                     |                                      |
|                               External Network                             |
|                                     |                                      |
+----------------------------------------------------------------------------+
```

- By default, each container gets an IP in the subnet 172.17.0.0/16.
- Docker0 bridge ensures both inter-container communication and host-container interactions.
- Host machine retains its distinct IP (e.g., 192.168.1.10).
- Containers communicate with one another through the bridge and with the host as well.
- External network communication by a container involves routing through docker0, then out the host's physical NIC, with the source IP changed to the host's IP due to Docker's NAT.

#### Container Mode
Containers can opt to share another container's network stack.

```
+----------------------------------------------------------------------------+
|                                 Host Machine                               |
|                                                                            |
|         +---------------------+   +---------------------+                  |
|         |                     |   |                     |                  |
|         |     Container A     |<--|     Container B     |                  |
|         | IP: 172.17.0.2      |   | IP: 172.17.0.3      |                  |
|         +---------------------+   +---------------------+                  |
|                                                                            |
+----------------------------------------------------------------------------+
```

- Both containers have unique IPs within Docker's network.
- Container B can directly communicate with Container A using Docker's internal DNS (by referencing container name/ID).
- This approach ensures container-to-container communication without any need for port exposure or mapping to the host, maintaining isolation.
- This mode proves useful when one container requires access to another container's service without exposing it externally.

#### None Mode
Containers come with a network stack, but no configuration is applied.

```
+----------------------------------------------------------------------------+
|                                 Host Machine                               |
|                                                                            |
|         +---------------------+                                            |
|         |                     |                                            |
|         |     Container A     |                                            |
|         | No IP, No external  |                                            |
|         |  network interface  |                                            |
|         +---------------------+                                            |
|                                                                            |
+----------------------------------------------------------------------------+
```

- The container in this mode can't interact with external systems, other containers, or even the host.
- Although a network namespace exists, no interfaces are configured.
- This mode provides a way to isolate a container's networking completely. It's useful in scenarios where the network should be set up manually or for containers that should be entirely isolated from any networking.
- Without manual network settings adjustments, processes/services inside the container won't be able to communicate outside.

### Ports 

When running a container, the services inside are isolated by default. However, Docker provides the capability to map a container's port to the host's port, allowing external entities to access services running inside the container.

- **Usage**: Utilize the `-p` flag during the `docker run` command.
  - Example: `-p 80:80` maps the host's port 80 to the container's port 80.
- **Access**: After mapping, services can be accessed using the host's IP and mapped port.
  - If a service inside a container runs on port 80 and it's mapped to port 8080 on the host, access it using `http://host-ip:8080`.
- **Multiple Containers**: Multiple containers can run services on the same internal port, but each must map to a unique host port.

```plaintext
+----------------------------------------------------------------------------+
|                                 Host Machine                               |
|                                                                            |
|    +---------+   Host Port 8080   +------------+ Container Port 80         |
|    |         |  <-------------->  |            |                           |
|    | Host OS |                    | Container  |                           |
|    | Network |                    |   Nginx    |                           |
|    +---------+                    +------------+                           |
|                                                                            |
+----------------------------------------------------------------------------+
```


- **Why Mapping?** Containers run in isolated environments. Port mapping ensures that services in containers are accessible externally. This process essentially punches a hole in the isolation layer, linking a specified port inside the container to a port on the host.

- **Flexibility**: Docker allows for a lot of flexibility in port mapping:
  - A high-traffic web service can be mapped to port 80 on the host while running on port 8080 inside the container.
  - Development environments can utilize random port mapping (-p 80) where Docker auto-assigns a host port.

- **Limitations and Conflicts**: It's crucial to ensure there are no port conflicts. If a port on the host is already in use, Docker will throw an error when attempting to bind to that port.

- **Security Considerations**: Exposing services to the outside world may introduce security risks. Always ensure that services are securely configured, and unnecessary ports are not exposed.

## Surveying what already exists

Running a few inspection commands quickly shows the lay of the land. The list below demonstrates the command, a trimmed sample output, and what that output means.

* `docker network ls`

  ```
  NETWORK ID     NAME      DRIVER    SCOPE
  a1b2c3d4e5f6   bridge    bridge    local
  0d1e2f3a4b5c   host      host      local
  9a8b7c6d5e4f   none      null      local
  ```

  Interpretation: the daemon ships with three built-ins—bridge, host and none—so any missing custom network here hints that your compose file never created one.

* `docker network inspect bridge --format '{{range .IPAM.Config}}{{println .Subnet}}{{end}}'`

  ```
  172.17.0.0/16
  ```

  Interpretation: learning the bridge subnet prevents accidental clashes when a VPN hands out the same range.

* `docker network inspect my_overlay | grep -i ingress -A1`

  ```
      "Ingress": false,
      "ConfigFrom": {
  ```

  Interpretation: an overlay with `Ingress=false` is an ordinary service network, not the Swarm-wide load-balancing ingress, which matters for port-publishing decisions.

## Creating and tuning custom networks

Before services can talk you often need to carve out a purpose-built network. Here is a quick reference table for the most used `docker network create` flags.

| Flag           | Meaning                                            | Example value  |
| -------------- | -------------------------------------------------- | -------------- |
| `--driver`     | Pick the driver                                    | overlay        |
| `--subnet`     | Specify CIDR                                       | 10.42.0.0/24   |
| `--gateway`    | Override default gateway                           | 10.42.0.1      |
| `--attachable` | Allow stand-alone containers to join Swarm overlay | true           |
| `--ip-range`   | Hand out IPs only from part of the subnet          | 10.42.0.128/25 |

Now watch the flags in action.

* `docker network create --driver overlay --subnet 10.42.0.0/24 --attachable app_net`

  ```
  f1e2d3c4b5a6
  ```

  Interpretation: the plain hexadecimal string is the network’s ID; seeing it printed confirms the manager stored your definition in the cluster store.

* `docker run -d --name db --network app_net postgres:16`

  ```
  9c8b7a6d5e4f
  ```

  Interpretation: the container joined *app\_net* instead of the default bridge, so other tasks in the same overlay can now reach it by the DNS name **db**.

## Real-World Scenarios 

Working through concrete stories makes the flags and drivers stick far better than dry reference material. Picture each subsection as a postcard from the field, stamped with a quick sketch and annotated with the exact commands engineers ran while the pager was buzzing.

### Microservices Architecture

A microservice stack resembles a bustling food-court: every stall offers one speciality, yet customers stroll between them without noticing the plumbing behind the walls. Docker’s bridge or overlay networks build those hidden passageways, keeping traffic swift and failures contained.

```
ASCII map of a tiny microservice city
+-----------+      vxlan/overlay       +-----------+
| checkout  |<------------------------>|  cart     |
+-----------+                          +-----------+
       ^                                    |
       | bridge                             v
+-----------+                          +-----------+
| frontend  |------------------------->|  search   |
+-----------+                          +-----------+
```

Because each container lives in its own namespace, a crash in *checkout* no longer topples *search*. When Black-Friday traffic doubles, adding ten more *cart* replicas takes one line in a Compose file.

Commands you will run in real life

* `docker service create --name cart --network shop overlay cart:2.0`

  ```
  z1y2x3w4v5u6
  ```

  Interpretation: Swarm accepted the service and attached it to the overlay named **shop**; the opaque ID confirms placement in the cluster store.

* `docker service scale cart=20`

  ```
  cart scaled to 20
  ```

  Interpretation: Swarm begins spawning extra tasks; combine this with `docker events --filter event=service_update` to watch them pop into existence.

---

### Hybrid Systems

Most enterprises look like geological strata: shiny containers on top of venerable VMs and even bare-metal relics. Host and macvlan modes let those layers speak a common tongue.

```
ASCII bridge between worlds
+----------+        eth0         +-----------+
| legacy   |<------------------->| macvlan0  |
|  VM      |                     | container |
+----------+                     +-----------+
```

Setting macvlan on the same VLAN as the Oracle server gives your container a first-class seat on the LAN—no NAT, no port-mapping headaches.

Typical toolkit

| Flag               | Purpose                       | Example                                |
| ------------------ | ----------------------------- | -------------------------------------- |
| `--driver macvlan` | Create L2-native network      | `docker network create -d macvlan ...` |
| `--ip-range`       | Hand out a slice of addresses | `192.168.10.128/26`                    |
| `--parent`         | Bind to physical NIC          | `eth0`                                 |

---

### Database ↔ Application Communication

Applications and databases converse thousands of times per second, so dependable discovery matters more than memorising IPs. Docker ships a lightweight DNS that updates the moment a container is replaced, just like a dynamic phonebook.

Inside an app container you might see:

```bash
getent hosts db
# → 10.0.2.17  db
```

That single-line proof shaves hours off debugging “works on my machine” DNS complaints.

Live-fire diagnostic

* `docker exec api ping -c2 db`

  ```
  PING db (10.0.2.17): 56 data bytes
  64 bytes from 10.0.2.17: icmp_seq=0 ttl=64 time=0.10 ms
  ```

  Interpretation: latency under a millisecond shows packets never leave the bridge; if name resolution fails, check that both tasks share the same user-defined network.

---

### Load Balancing at Scale

Swarm’s ingress network behaves like a self-healing traffic roundabout. Publish port 80 once, and every manager node starts welcoming cars, quietly steering them to whichever replica waves “I’m healthy.”

```
Text view of IPVS round-robin table
VIP: 10.255.0.2:80
  -> 10.0.3.5:3000 Route   1
  -> 10.0.3.6:3000 Route   1
```

If roadworks take down node *B*, IPVS removes that destination instantly, so no driver turns up at a closed stall.

Battle-tested commands

* `docker service create --name web --publish 80:80 --replicas 3 --network ingress nginx`

  ```
  q9r8s7t6u5v4
  ```

  Interpretation: publishing attaches the service to the special ingress overlay and seeds the IPVS table across the cluster.

* `docker service ps web --no-trunc`

  ```
  NAME           NODE  DESIRED STATE  CURRENT STATE           PORTS
  web.1.x...     nodeA Running        Running 5m              *:80->80/tcp
  ```

  Interpretation: ensure that at least one replica sits on each availability zone; uneven spread hints at resource constraints rather than networking flaws.

---

### Integrating Legacy Systems

Containers rarely start in a vacuum. A 1990s billing system demanding the static address `10.1.2.99` can still join the modern party thanks to macvlan.

```bash
docker network create -d macvlan \
  --subnet 10.1.2.0/24 --gateway 10.1.2.1 \
  --ip-range 10.1.2.96/29 \
  -o parent=eth0 legacy_net
docker run -d --name modern_api --network legacy_net --ip 10.1.2.99 my/api:latest
```

Output

```
Created network legacy_net
Started container modern_api
```

Interpretation: the old mainframe sees *modern\_api* at the expected IP; meanwhile the container still enjoys cgroup limits and log drivers, giving you safety upgrades without painful code rewrites.

## Debugging and monitoring traffic

Packets can still disappear into black holes, so a few CLI probes save hours.

* `docker exec -it web ping -c3 db`

  ```
  PING db (10.42.0.3): 56 data bytes
  64 bytes from 10.42.0.3: icmp_seq=0 ttl=64 time=0.094 ms
  ```

  Interpretation: successful ICMP shows L3 reachability; a *Name or service not known* error would instead point at DNS, not connectivity.

* `docker run --network host --rm nicolaka/netshoot tcpdump -i any port 5432 -c 5`

  ```
  10:15:42.123456 IP 10.42.0.5.53412 > 10.42.0.3.5432: Flags [S], seq 123456, win 64240, options [...]
  ```

  Interpretation: seeing SYN packets leave but no replies come back hints the database process is down rather than a network ACL.

* `docker events --since 5m --filter type=network`

  ```
  2025-05-04T10:18:02Z network disconnect app_net container=db
  ```

  Interpretation: an unexpected disconnect right before application errors often traces to Swarm rescheduling or human redeploys.
