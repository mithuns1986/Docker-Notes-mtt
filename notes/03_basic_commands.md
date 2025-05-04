## From idea to runnable image

Every Docker journey begins with an image, so the first scenario follows a developer who has just cloned a project and wants to explore it locally. The ASCII drawing places the three main objects on stage—Dockerfile, image cache, and registry—so you can picture the flow before typing a single command.

```
ASCII pipeline for “docker build”
+------------+      docker build      +------------+
| Dockerfile |  --------------------> |   Image    |
+------------+                        +------------+
                                          |
                                          | docker push
                                          v
                                    +-------------+
                                    |  Registry   |
                                    +-------------+
```

### 1.1 Checking what you have before building

* Listing the local cache with `docker images` usually answers the question, *“Did I already pull alpine?”*

  ```bash
  docker images
  ```

  ```
  REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
  alpine       3.20      45d09fee87a5   2 weeks ago    7MB
  ```

  Interpretation: the presence of `alpine:3.20` means a fresh `docker pull alpine:3.20` would be wasted bandwidth.

### 1.2 Tidying up outdated images

* Removing an unused layer keeps laptops snappy.

  ```bash
  docker image rm alpine:3.19
  ```

  ```
  Untagged: alpine:3.19
  Deleted: 9b3b3b3b3b3b
  ```

  Interpretation: the short digest shows that the layer vanished from the cache; any container still referencing it will fail to start, so prune with care.

### 1.3 Forging your own image

* Building from the current directory feels almost like compiling source code.

  ```bash
  docker build -t myweb:1.0 .
  ```

  ```
  [+] Building  3.7s (8/8) FINISHED
   => exporting to image
   => => naming to docker.io/library/myweb:1.0
  ```

  Interpretation: the green “FINISHED” banner confirms every instruction in the Dockerfile ran without error.

A quick reference for the most-used `docker build` flags sits in the table below.

| Flag          | Meaning                       | Example value     |
| ------------- | ----------------------------- | ----------------- |
| `-t`          | Assigns name and tag          | `myweb:1.0`       |
| `--target`    | Stop at an intermediate stage | `builder`         |
| `--build-arg` | Pass build-time variable      | `VERSION=release` |
| `--no-cache`  | Ignore layer cache            | n/a               |

---

## 2 Spinning containers for daily work

Imagine the image is ready and curiosity strikes: *“What does the service actually do?”* The next sequence follows the developer through interactive tests, background runs, file extraction, and graceful shutdowns.

```
ASCII view of host vs container namespace
+------------+           +-----------------+
|   Host OS  |  <------> |   Container     |
+------------+  exec/sock+-----------------+
```

### 2.1 Opening an interactive shell

* Dropping into Bash helps verify environment variables in seconds.

  ```bash
  docker run -it myweb:1.0 /bin/bash
  ```

  ```
  root@7abc123:/#
  ```

  Interpretation: the prompt change tells you that PID 1 inside the namespace is now `/bin/bash`, giving full control over the container.

### 2.2 Running a long-lived service in the background

* A detached instance frees the terminal yet keeps logs flowing to `docker logs`.

  ```bash
  docker run -itd --name web01 -p 8080:80 myweb:1.0
  ```

  ```
  9c8b7a6d5e4f3
  ```

  Interpretation: the opaque ID is good news; port 8080 on the host now forwards to the Nginx port inside the container.

### 2.3 Grabbing build artefacts after a compile step

* Copying files avoids rebuilding images just to read outputs.

  ```bash
  docker cp web01:/usr/share/nginx/html/index.html ./index.html
  ```

  ```
  Successfully copied 1.2kB
  ```

  Interpretation: data left the namespace without exposing a volume, useful when you need a quick look at generated files.

### 2.4 Seeing everything that ever ran

* Listing all containers, even the exited ones, helps trace flaky scripts.

  ```bash
  docker ps -a
  ```

  ```
  CONTAINER ID   NAMES   STATUS          IMAGE
  9c8b7a6d5e4f   web01   Up 34 minutes   myweb:1.0
  7abc123        wizard  Exited (0) 2h  alpine
  ```

  Interpretation: spotting `Exited (0)` signals a normal shutdown, while codes above 0 hint at crashes.

### 2.5 Stopping misbehaving workloads

* Graceful termination lets PID 1 handle cleanup.

  ```bash
  docker stop web01
  ```

  ```
  web01
  ```

  Interpretation: Docker sent SIGTERM, then after ten seconds SIGKILL; one line means it finished within the grace period.

### 2.6 Bringing an entire lab down in one swoop

* Halting every running container is handy before system upgrades.

  ```bash
  docker stop $(docker ps -a -q)
  ```

  ```
  9c8b7a6d5e4f
  7abc123
  ```

  Interpretation: each returned ID confirms one container has moved to the *Exited* state.

### 2.7 Cleaning up dead husks

* Removing a single stopped container keeps lists short.

  ```bash
  docker rm wizard
  ```

  ```
  wizard
  ```

  Interpretation: the name echoes back when the filesystem layers vanish.

### 2.8 Deleting every exited container in bulk

* A mass purge makes perfect sense after automated test runs.

  ```bash
  docker rm $(docker ps -a -q -f status=exited)
  ```

  ```
  7abc123
  ```

  Interpretation: silence means nothing matched; one or more IDs show successful deletion.

---

## 3 Housekeeping before / after a sprint

Disk fills silently, so regular pruning is a minor ritual that prevents frantic searches for free space on demo day.

### 3.1 Removing everything unused—the nuclear option

* System prune wipes dangling images, stopped containers, and unused networks.

  ```bash
  docker system prune --all
  ```

  ```
  Total reclaimed space: 1.3 GB
  ```

  Interpretation: the reclaimed figure validates that dead layers were taking up real bytes.

### 3.2 Visualising space at a glance

* Disk-usage reports replace guesswork with numbers.

  ```bash
  docker system df
  ```

  ```
  TYPE            TOTAL SIZE   ACTIVE SIZE   RECLAIMABLE
  Images          1.5GB        300MB         1.2GB
  Containers      0B           0B            0B
  ```

  Interpretation: most bloat often hides in image layers rather than volumes.

### 3.3 Clearing orphaned volumes

* Old named volumes from previous releases can hog SSDs.

  ```bash
  docker volume prune
  ```

  ```
  Deleted Volumes:
  blog_dbdata
  Total reclaimed space: 95 MB
  ```

  Interpretation: if an expected production volume appears here, abort quickly with Ctrl-C.

---

## 4 Secure shell access without exposing the Docker socket

Sometimes policy forbids direct `docker exec`. A helper container acting as a tiny SSH jump box bridges usability and security.

### 4.1 Launching the jump box

* The run command below binds the Docker socket, opens port 2222, yet disables password auth for speed during local testing.

  ```bash
  docker run -d -p 2222:22 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e FILTERS='{"name":["^/web01$"]}' \
    -e AUTH_MECHANISM=noAuth \
    my/helper:ssh
  ```

  ```
  3f2e1d0c9b8a
  ```

  Interpretation: only containers whose names match **web01** become reachable through the SSH tunnel.

### 4.2 Jumping into the box

* Standard OpenSSH commands keep muscle memory intact.

  ```bash
  ssh user@localhost -p 2222
  ```

  ```
  Welcome to web01 (Debian GNU/Linux 12 ✨)
  ```

  Interpretation: you are now inside the target container without ever installing an SSH daemon inside it.

### 4.3 Leaving cleanly

* Exiting returns control to the host shell.

  ```bash
  exit
  ```

  ```
  Connection to localhost closed.
  ```

  Interpretation: the tunnel survives, so a second `ssh` is instantaneous.

---

## 5 Networking detective work

When two services refuse to talk, the fix usually lies one `inspect` away. The diagram shows where each command collects information.

```
ASCII locator for network commands
           docker inspect
         +----------------+
         |  Network JSON  |
         +----------------+
               ^
               |
docker ps  docker port
               |
               v
         +--------------+
         |   Container  |
         +--------------+
```

### 5.1 Discovering a container’s IP the quick way

* A tiny Go template avoids scrolling through full JSON.

  ```bash
  docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web01
  ```

  ```
  10.0.2.17
  ```

  Interpretation: copy this IP into `ping` to check L3 reachability.

### 5.2 Confirming published ports

* Seeing a mapping reassures load-balancer teams that traffic is routed.

  ```bash
  docker port web01
  ```

  ```
  80/tcp -> 0.0.0.0:8080
  ```

  Interpretation: the wildcard bind means any interface on the host will accept the request.

### 5.3 Peering into a user-defined network

* Inspect returns every container endpoint plus subnet details.

  ```bash
  docker network inspect app_net
  ```

  ```
  "Subnet": "10.0.2.0/24",
  "Containers": {
      "9c8b7a6d5e4f": {
          "Name": "web01",
          "IPv4Address": "10.0.2.17/24"
      }
  }
  ```

  Interpretation: overlapping subnets between networks jump out instantly.

### 5.4 Listing available cables and switches

* A high-level view of networks often explains mysterious IPs.

  ```bash
  docker network ls
  ```

  ```
  NETWORK ID     NAME      DRIVER    SCOPE
  a1b2c3d4e5f6   bridge    bridge    local
  f1e2d3c4b5a6   app_net   overlay   swarm
  ```

  Interpretation: seeing *overlay* under DRIVER confirms that cross-host traffic rides VXLAN tunnels.

### 5.5 Carving out a brand-new network

* Custom subnets prevent clashes with corporate VPNs.

  ```bash
  docker network create --subnet 10.42.0.0/24 app_net
  ```

  ```
  f1e2d3c4b5a6
  ```

  Interpretation: the returned ID means the bridge, iptables rules, and DNS entries are all ready.

| Flag        | Role in network creation | Example        |
| ----------- | ------------------------ | -------------- |
| `--driver`  | Selects backend          | `overlay`      |
| `--subnet`  | CIDR range               | `10.42.0.0/24` |
| `--gateway` | Custom gateway address   | `10.42.0.1`    |

### 5.6 Switching a running container between LANs

* Attaching and detaching helps simulate fail-over scenarios.

  ```bash
  docker network connect app_net web01
  docker network disconnect bridge web01
  ```

  ```
  (no output on success)
  ```

  Interpretation: silence is golden; errors would complain if the container were already joined or depended on the bridge for published ports.

---

## 6 Keeping data alive with volumes

Stateless containers reboot happily, but databases throw tantrums when storage disappears. Volumes give state a comfortable home.

```
ASCII snapshot of a volume mount
+-----------+                 +---------------+
| Container | -- /var/lib/db->|  Volume data  |
+-----------+                 +---------------+
```

### 6.1 Surveying the volume landscape

* Listing volumes identifies potential disk hogs.

  ```bash
  docker volume ls
  ```

  ```
  DRIVER    VOLUME NAME
  local     blog_dbdata
  local     cache
  ```

  Interpretation: each entry is a directory under `/var/lib/docker/volumes/…`.

### 6.2 Reserving space for a new service

* Pre-creating avoids mismatched driver defaults in Swarm.

  ```bash
  docker volume create photos
  ```

  ```
  photos
  ```

  Interpretation: the single-word reply repeats the chosen name.

### 6.3 Peeking into a volume’s metadata

* Inspect shows mount-points and consumer containers.

  ```bash
  docker volume inspect photos
  ```

  ```
  "Mountpoint": "/var/lib/docker/volumes/photos/_data",
  "Labels": null
  ```

  Interpretation: mounting the path directly on the host helps quick troubleshooting.

### 6.4 Removing a forgotten volume

* Deleting a volume frees bytes but cannot be undone.

  ```bash
  docker volume rm cache
  ```

  ```
  cache
  ```

  Interpretation: any container using **cache** will now fail to start until a new volume is attached.

