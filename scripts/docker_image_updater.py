#!/usr/bin/env python3

'''
Usage:

To check for image updates and pull the new versions without restarting the containers:

python3 docker_image_updater.py

To also restart the containers after pulling the updated image:

python3 docker_image_updater.py --restart
'''

import subprocess
import argparse

def get_running_containers():
    """Get a list of IDs of all running containers."""
    cmd = ["docker", "ps", "-q"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    container_ids = result.stdout.strip().split("\n")
    return container_ids

def get_container_image(container_id):
    """Get the image name of the specified container."""
    cmd = ["docker", "inspect", "--format", "{{.Config.Image}}", container_id]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def pull_image(image_name):
    """Pull the latest version of the specified image."""
    cmd = ["docker", "pull", image_name]
    subprocess.run(cmd)

def restart_container(container_id):
    """Restart the specified container."""
    cmd = ["docker", "restart", container_id]
    subprocess.run(cmd)

def main(args):
    containers = get_running_containers()

    for container in containers:
        image = get_container_image(container)
        print(f"Checking updates for image: {image} used by container: {container}")
        pull_image(image)

        if args.restart:
            print(f"Restarting container: {container}")
            restart_container(container)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker Image Updater")
    parser.add_argument("--restart", action="store_true",
                        help="Restart containers if an updated image is pulled")
    args = parser.parse_args()
    
    main(args)
