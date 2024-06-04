# Docker
A comprehensive collection of notes on Docker, designed to help you understand and leverage Docker for containerization and DevOps practices. This repository covers a wide range of topics, from basic concepts to advanced techniques, providing valuable insights and practical examples for both beginners and experienced users.

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

## Projects

| Project           | Description                                                      | Link                                                                                                   |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| MySQL             | A relational database management system (RDBMS) based on SQL.     | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/mysql/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |
| PostgreSQL        | An advanced open-source relational database management system.    | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/postgresql/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |
| MongoDB           | A NoSQL database platform for scalable and high-performance needs. | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/mongodb/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |
| Flask             | A lightweight web framework in Python for building web applications. | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/flask/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |
| NodeJS            | A runtime environment for executing JavaScript outside of a browser. | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/nodejs/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |
| VirtualBox Networking | Configuration and management of network settings in VirtualBox. | <a href="https://github.com/djeada/Docker-Notes/blob/main/projects/virtualbox_networking/README.md"><img src="https://img.icons8.com/color/344/markdown.png" height="50" /></a> |

## Scripts

| Script Name                     | Description                                                                                           | Link                                                                                              |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| docker_image_updater.py         | Script to update Docker images.                                                                       | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/docker_image_updater.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |
| docker_compose_generator.py     | Generates a `docker-compose` file based on specified parameters.                                      | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/docker_compose_generator.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |
| image_cleaner.py                | Script to clean up old or unused Docker images.                                                       | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/image_cleaner.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |
| container_runner.py             | Handles the launching of individual Docker containers.                                                | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/container_runner.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |
| batch_container_runner.py       | Script designed to run multiple Docker containers in batches.                                          | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/batch_container_runner.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |
| container_resource_monitor.py   | Monitors and reports on resource usage (like CPU, memory) of running containers.                       | <a href="https://github.com/djeada/Docker-Notes/blob/main/scripts/container_resource_monitor.py"><img src="https://img.icons8.com/color/344/python.png" height="50" /></a> |


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
