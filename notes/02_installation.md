## Installing Docker on Debian-based Systems

Before diving into the installation process, it's worth noting that this guide specifically caters to Debian-based distributions like Ubuntu. By following these steps, you can ensure a clean and effective installation of Docker.

### Remove Old Docker Versions

First, it's a good idea to remove any older versions of Docker that might exist on your system to avoid conflicts.

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

### Install Prerequisites

Update the package database and install essential packages required for Docker's installation.

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
```

### Add Docker’s Official GPG Key

The GPG key is essential for ensuring the integrity and authenticity of the Docker packages.

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

### Set Up the Docker Repository

Add the Docker repository to your APT sources:

```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker Engine

With the repository in place, you can now install the Docker engine, CLI tools, and related packages.

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### Verify Installation

It's a good practice to verify that Docker was installed correctly. Run the hello-world image, and if everything is set up correctly, you'll see a message indicating that Docker is running.

```bash
sudo docker run hello-world
```

## Installing Docker on Windows

Docker Desktop for Windows is the preferred choice for running Docker on Windows 10 and Windows 11. It integrates seamlessly with the OS and offers a comprehensive GUI for managing containers. This guide will walk you through the steps to install Docker Desktop on Windows.

### Prerequisites:

- **Windows 10 Pro, Enterprise, or Education** (64-bit). For Windows Home, ensure that you have Windows Subsystem for Linux 2 (WSL 2) installed.
- **Virtualization technology**: Ensure virtualization is enabled in your BIOS/UEFI settings.

### Download Docker Desktop

Navigate to the official [Docker Desktop page](https://www.docker.com/products/docker-desktop) and download the installer for Windows.

### Install Docker Desktop

1. Run the installer you downloaded.
2. Follow the installation instructions and accept the terms.
3. Choose whether to use WSL 2 based engine (recommended) or Hyper-V. If you're using Windows Home, you'll need to use WSL 2.
4. Click "Install."

### Start Docker Desktop

After installation, Docker Desktop will start automatically. You'll see the Docker icon in your system tray indicating that Docker is running.

### Verify Installation

Open a command prompt or PowerShell window and run:

```bash
docker --version
```

This should display the version of Docker installed on your system.

To test the Docker installation, you can run the `hello-world` container:

```bash
docker run hello-world
```

If everything works correctly, you'll see a message from Docker confirming your successful setup.
