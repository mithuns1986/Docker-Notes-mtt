# Docker
A comprehensive guide to understanding and mastering Docker.

## Notes

| Topic                     | Description                                                                   | Notes                                                                                                     |
| --------------------------| ------------------------------------------------------------------------------| --------------------------------------------------------------------------------------------------------- |
| Docker Intro               | An introduction to the basic concepts and components of Docker.                | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/01_intro.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>               |
| Installation               | Step-by-step guide on how to install Docker on different platforms.           | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/02_installation.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>        |
| Basic Commands             | Overview of fundamental commands for Docker usage.                            | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/03_basic_commands.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>        |
| Dockerfile                 | Instructions and best practices for creating Docker images using Dockerfile.   | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/04_docker_file.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>            |
| Networking                 | Basics of networking within Docker and connecting containers.                  | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/05_networking.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>            |
| Security                   | Measures and best practices to secure Docker containers and images.            | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/06_security.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>               |
| Swarm                      | Introduction to Docker Swarm, a native clustering and orchestration tool.      | <a href="https://github.com/djeada/Docker-Notes/blob/main/notes/07_swarm.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a>                  |




## Assessing Your Docker Proficiency

Evaluate your Docker understanding and skills using the following benchmarks:

### Fundamental Concepts

1. **Containerization vs. Virtualization**:
   - Distinguish between containers and traditional virtual machines.
   - Recognize how containers optimize performance by sharing the host system's kernel, whereas VMs require their own OS instance.

2. **Linux Kernel Components**:
   - Understand critical Linux kernel components that power containerization, like cgroups and namespaces.

### Practical Knowledge

3. **Utilizing Public Docker Images**:
   - Pull and execute containers from images on Docker Hub or other public repositories.

4. **Crafting Dockerfiles**:
   - Write Dockerfiles that adhere to best practices:
     - Optimize layer ordering for caching.
     - Leverage multi-stage builds to reduce image size.
     - Ensure the usage of secure base images and up-to-date dependencies.

5. **Docker Compose Mastery**:
   - Create `docker-compose` configurations to manage multiple containerized applications, easing local development and testing setups.

6. **Docker Networking**:
   - Understand Docker's various networking modes, such as bridge, host, and overlay.
   - Set up communication between containers and define how external systems access them.

### Advanced Practices

7. **Docker Security**:
   - Enforce Docker security best practices:
     - Operate containers as non-root users.
     - Opt for secure and lightweight base images.
     - Consistently scan images for potential vulnerabilities.
     - Use read-only filesystems when suitable.

8. **Alternative Containerization Tools**:
   - Get acquainted with other container tools beyond Docker:
     - `buildkit`: A modern approach to building container images.
     - `buildah`: Constructs OCI-compatible container images.
     - `kaniko`: Constructs container images from a `Dockerfile`, suitable for container or Kubernetes environments.

## Contributing

Your contributions are valued! For significant updates or changes, initiate an issue for discussion.

Ensure that you adapt tests to reflect your changes where necessary.

## License
[MIT License](https://choosealicense.com/licenses/mit/)
