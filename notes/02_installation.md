## 🐳 Quick Docker Installation via Script

For Debian-based systems (e.g. Ubuntu), Docker provides an automated installation script that simplifies the setup process.

### ⚠️ Remove Old Docker Versions

It's best to start fresh by removing any older Docker components to avoid conflicts.

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

### 🚀 Install Docker Using Official Script

This command downloads and runs the Docker install script from `get.docker.com`, which handles the setup:

```bash
curl -fsSL https://get.docker.com | sudo bash
```

You can optionally pass environment variables for customization—for example:

```bash
curl -fsSL https://get.docker.com | sudo bash -s -- --dry-run
```

To view options available in the script, visit the [install script documentation](https://photos.google.com/u/4/updates).

### ✅ Verify Docker Installation

Confirm Docker is working correctly:

```bash
sudo docker run hello-world
```

This will download and run a test container to verify everything is set up properly.
