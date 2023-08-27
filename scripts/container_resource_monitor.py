#!/usr/bin/env python3

'''
Usage:

Simply run the script, and it will start monitoring all running Docker containers every 10 seconds. If a container's CPU or memory usage exceeds the thresholds specified in the CPU_THRESHOLD and MEMORY_THRESHOLD variables, an alert will be printed to the console.

python3 container_resource_monitor.py
'''

import subprocess
import time
import json

def get_container_stats():
    """Get stats of all running containers."""
    cmd = ["docker", "stats", "--no-stream", "--format", "{{json .}}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")

    stats = []
    for line in lines:
        stats.append(json.loads(line))
    return stats

def monitor_containers(cpu_threshold, mem_threshold):
    """Monitor and log container resources. Alert if thresholds are exceeded."""
    while True:
        stats = get_container_stats()
        for stat in stats:
            name = stat["Name"]
            cpu_percent = float(stat["CPUPerc"].replace("%", ""))
            mem_usage_data = stat["MemUsage"].split("/")
            mem_usage = int(mem_usage_data[0].replace("MiB", "").strip())
            mem_limit = int(mem_usage_data[1].replace("MiB", "").strip())
            mem_percent = (mem_usage / mem_limit) * 100
            
            print(f"{name} - CPU: {cpu_percent}%, Memory: {mem_percent:.2f}%")

            if cpu_threshold and cpu_percent > cpu_threshold:
                print(f"ALERT: {name} has exceeded the CPU threshold!")
            
            if mem_threshold and mem_percent > mem_threshold:
                print(f"ALERT: {name} has exceeded the Memory threshold!")

        time.sleep(10)  # Check every 10 seconds. This interval can be adjusted.

if __name__ == "__main__":
    # You can set these thresholds according to your requirements.
    CPU_THRESHOLD = 75.0  # Alert if CPU usage exceeds 75%
    MEMORY_THRESHOLD = 80.0  # Alert if memory usage exceeds 80%

    monitor_containers(CPU_THRESHOLD, MEMORY_THRESHOLD)
