## Making a Container in VirtualBox Accessible to LAN Devices

When you're running Docker within a VirtualBox VM and want to expose a Docker container to other devices on your LAN, you need to adjust the networking settings in both VirtualBox and your host system. Here's a step-by-step guide:

### Set up a Docker Container in VirtualBox

Assuming you already have a Docker container running within a VirtualBox VM, take note of the port on which the service inside the container is running. For example, if you're running a web service in Docker, it might be exposed on port 80 or 8080 inside the VM.

### Configure Port Forwarding in VirtualBox

Before your container's service becomes accessible from the LAN, you must set up port forwarding in the VirtualBox settings:

1. Open VirtualBox.
2. Select the VM running Docker.
3. Go to Settings > Network.
4. Under the Adapter 1 tab, ensure that the Attached to field is set to NAT.
5. Click on Advanced > Port Forwarding.
6. Add a new rule:
  - Name: A descriptive name (e.g., "DockerWeb")
  - Protocol: Typically TCP for web services
  - Host IP: Leave blank
  - Host Port: An unused port on your host machine (e.g., `8080`)
  - Guest IP: Leave blank
  -  Guest Port: The port the service in the Docker container is running on (e.g., `80`)
7. Click OK to close the windows and save the settings.

### Find Your Host Machine's IP Address

To make your container accessible on the LAN, you'll need to provide the IP address of the machine hosting VirtualBox (your host machine). To get this on a Windows machine:

1. Open the command prompt (cmd).
2. Enter the command: `ipconfig /all`
3. Locate the section corresponding to your primary network adapter (often labeled "Ethernet adapter" or "Wi-Fi").
4. Take note of the IPv4 Address. This will be the IP address other devices on the LAN will use to access the Docker container.

### Access the Docker Container from LAN Devices

With the above configurations in place, other devices on your LAN can now access the Docker container using the host machine's IP address and the forwarded port.

For example, if the host machine's IP address is 192.168.1.100 and you forwarded to port 8080, devices on the LAN can access the Docker container's service by navigating to `http://192.168.1.100:8080`.
