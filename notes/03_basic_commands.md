## Docker Commands Overview

Understanding Docker commands is crucial for effective container management. Below are some commonly used Docker commands categorized based on their operations.

### Image Operations

- **List all images**: Displays all images stored locally.

```bash
docker images
```

- **Remove an image**: Deletes a specified image from local storage.

```bash
docker image rm <image name or ID>
```

- **Build a docker image**: Constructs an image using a Dockerfile, which is usually located in the current directory.

```bash
docker build -t <name>:<tag> <path to dockerfile>
```

### Container Operations

- **Start and log into a container**: Executes a container and gives you an interactive terminal access.

```bash
docker run -it <image name or ID> /bin/bash
```

- **Start a detached container**: Initiates a container in the background without keeping the terminal occupied.

```bash
docker run -itd --name <container name> <image name or ID>
```

- **Copy data from a running container**: Moves files or directories between a specific container and your local filesystem.

```bash
docker cp <container name or ID>:<source path> <destination path>
```

- **List all containers**: Shows every container, regardless of its current state (running, stopped, etc.).

```bash
docker ps -a
```

- **Stop a container**: Gracefully terminates a running container.

```bash
docker stop <container name or ID>
```

- **Stop all running containers**: Handy when needing to cease all active containers at once.
```bash
docker stop $(docker ps -a -q)
```

- **Remove a container**: Erases a particular container. Note that the container must be stopped first.

```bash
docker rm <container name or ID>
```

- **Remove all stopped containers**: Deletes every container that is not currently running.

```bash
docker rm $(docker ps -a -q -f status=exited)
```

### System Operations

- **Housekeeping**: Clean up unused data.

```bash
docker system prune --all
```

- **View Docker disk usage**: Understand how much space Docker is using on your system.

```bash
docker system df
```

- **Clean up unused volumes**: Volumes can take up space if not actively used by containers.

```bash
docker volume prune
```

### SSH into a Container

- **Start the helper container**:

```bash
docker run -d -p 2222:22 -v /var/run/docker.sock:/var/run/docker.sock -e FILTERS={"name":["^/my-container$"]} -e AUTH_MECHANISM=noAuth <image-name>
```

- **SSH into the helper container**:

```bash
ssh user-name@localhost -p 2222
```

- **Exit SSH session**:

```bash
exit
```

### Networking

- **Get the container's hostname IP address**:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name_or_id>
```

- **Display container's port mappings**:

```bash
docker port <container_name_or_id>
```

- **Inspect network details**: View detailed configuration and connected containers of a specific network.

```bash
docker network inspect <network_name_or_id>
```

- **List all networks**: See what networks are currently defined.

```bash
docker network ls
```

- **Create a new network**: Useful when setting up custom networking for a group of containers.

```bash
docker network create <network_name>
```

- **Connect a container to a network**: Attach a running container to an existing network.

```bash
docker network connect <network_name> <container_name_or_id>
```

- **Disconnect a container from a network**: Detach a running container from a network.

```bash
docker network disconnect <network_name> <container_name_or_id>
```

### Docker Volumes

**Volumes** are the preferred way to persist data in Docker:

- **List volumes**: See what volumes are present on your system.

```bash
docker volume ls
```

- **Create a volume**: Prepare storage for use with a container.

```bash
docker volume create <volume_name>
```

- **Inspect a volume**: Get detailed information about a specific volume.

```bash
docker volume inspect <volume_name>
```

- **Remove a volume**: Delete a volume when it's no longer needed. Caution: This deletes the data!

```bash
docker volume rm <volume_name>
```
