#!/usr/bin/env python3

'''
Usage:

To use this script, you provide a list of images and, optionally, container names, ports, environment variables, and volume mounts. The format for each image is:

image,name=container_name,port=8080,env=KEY:VALUE,volume=/host:/container

For example, to run two containers:

- nginx image with the name web_server and port 80 mapped.
- mysql image with the name db_server, port 3306 mapped, an environment variable MYSQL_ROOT_PASSWORD=my-secret-pw, and a volume mount /mydata:/var/lib/mysql.

You would execute:

python3 batch_container_runner.py nginx,name=web_server,port=80 mysql,name=db_server,port=3306,env=MYSQL_ROOT_PASSWORD:my-secret-pw,volume=/mydata:/var/lib/mysql
'''

import subprocess
import argparse

def run_container(image, name=None, port=None, envs=None, volumes=None):
    """Start a container from the specified image."""
    cmd = ["docker", "run", "-d"]

    if name:
        cmd += ["--name", name]

    if port:
        cmd += ["-p", f"{port}:{port}"]

    if envs:
        for key, value in envs.items():
            cmd += ["-e", f"{key}={value}"]

    if volumes:
        for vol in volumes:
            cmd += ["-v", vol]

    cmd.append(image)
    subprocess.run(cmd)

def main(args):
    """Run containers from provided images."""
    for image_data in args.images:
        params = image_data.split(',')
        image = params[0]
        name = None
        port = None
        envs = {}
        volumes = []

        for param in params[1:]:
            if param.startswith('name='):
                name = param.split('=', 1)[1]
            elif param.startswith('port='):
                port = int(param.split('=', 1)[1])
            elif param.startswith('env='):
                key, value = param.split('=', 1)[1].split(':')
                envs[key] = value
            elif param.startswith('volume='):
                volumes.append(param.split('=', 1)[1])

        run_container(image, name, port, envs, volumes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Container Runner")
    parser.add_argument("images", type=str, nargs='+', 
                        help="List of images and associated parameters. Format: image,name=container_name,port=8080,env=KEY:VALUE,volume=/host:/container")
    
    args = parser.parse_args()
    main(args)
