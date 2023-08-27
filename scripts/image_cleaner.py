#!/usr/bin/env python3

'''
Usage:

- To remove only the dangling images:

python3 docker_image_cleaner.py

- To remove images that haven't been used for 30 days or more:

python3 docker_image_cleaner.py --days 30

'''


import subprocess
import argparse
from datetime import datetime, timedelta

def get_dangling_images():
    """Fetch all dangling images."""
    cmd = ["docker", "images", "-f", "dangling=true", "-q"]
    result = subprocess.check_output(cmd)
    return result.decode('utf-8').splitlines()

def get_old_images(days_old):
    """Fetch images older than the specified days."""
    cmd = ["docker", "images", "--format", "{{.ID}} {{.CreatedSince}}"]
    result = subprocess.check_output(cmd)
    lines = result.decode('utf-8').splitlines()

    old_images = []
    for line in lines:
        image_id, age = line.split(' ', 1)
        if "days" in age:
            num_days = int(age.split(' ')[0])
            if num_days > days_old:
                old_images.append(image_id)
    return old_images

def remove_images(image_list):
    """Remove Docker images."""
    if not image_list:
        print("No images to remove.")
        return

    cmd = ["docker", "rmi", "-f"] + image_list
    subprocess.run(cmd)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker Image Cleaner")
    parser.add_argument("--days", type=int, default=0,
                        help="Number of days the image hasn't been used to be considered old. Default is 0 (will not remove based on age).")

    args = parser.parse_args()

    images_to_remove = set(get_dangling_images())

    if args.days > 0:
        images_to_remove.update(get_old_images(args.days))

    remove_images(list(images_to_remove))
