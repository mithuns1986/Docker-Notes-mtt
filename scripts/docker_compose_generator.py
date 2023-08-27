#!/usr/bin/env python3

'''
Usage:

The script uses command-line arguments to take in services, networks, and volumes and then creates a docker-compose.yml file. Here's how you would use the script to define two services (a web server and a database) and a network:

python3 docker_compose_generator.py \
    --networks webnet \
    --service-name webapp --service-image nginx --service-ports 80:80 --service-volumes /webroot:/var/www \
    --service-name db --service-image mysql:5.7 --service-ports 3306:3306 --service-env MYSQL_ROOT_PASSWORD:secret

This will generate a docker-compose.yml file with a web server and database, a network named webnet, and some specified volumes and environment variables.
'''

import argparse
import yaml

def create_service(service):
    """Parse service input and return a dictionary representation."""
    service_data = {
        'image': service['image'],
    }
    if 'ports' in service:
        service_data['ports'] = service['ports'].split(',')
    if 'volumes' in service:
        service_data['volumes'] = service['volumes'].split(',')
    if 'env' in service:
        service_data['environment'] = {}
        for env_pair in service['env'].split(','):
            key, value = env_pair.split(':')
            service_data['environment'][key] = value
    return service_data

def main(args):
    """Generate a docker-compose.yml file."""
    compose_data = {
        'version': '3.8',
        'services': {},
        'networks': args.networks.split(',') if args.networks else None,
        'volumes': args.volumes.split(',') if args.volumes else None
    }

    for service in args.services:
        service_name = service['name']
        compose_data['services'][service_name] = create_service(service)

    with open('docker-compose.yml', 'w') as file:
        yaml.dump(compose_data, file, default_flow_style=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker Compose Generator")
    
    parser.add_argument("--networks", type=str, help="Comma-separated list of networks. Example: network1,network2")
    parser.add_argument("--volumes", type=str, help="Comma-separated list of volumes. Example: volume1,volume2")
    
    service_parser = parser.add_argument_group("services")
    service_parser.add_argument("--service-name", dest="services", action="append", type=lambda kv: kv.split("="), metavar="name=VALUE",
                                help="The name of the service. Example: --service-name webapp")
    service_parser.add_argument("--service-image", dest="services", action="append", type=lambda kv: kv.split("="), metavar="image=VALUE",
                                help="The image for the service. Example: --service-image nginx")
    service_parser.add_argument("--service-ports", dest="services", action="append", type=lambda kv: kv.split("="), metavar="ports=VALUE",
                                help="Comma-separated ports for the service. Example: --service-ports 80:80,443:443")
    service_parser.add_argument("--service-volumes", dest="services", action="append", type=lambda kv: kv.split("="), metavar="volumes=VALUE",
                                help="Comma-separated volumes for the service. Example: --service-volumes /host:/container")
    service_parser.add_argument("--service-env", dest="services", action="append", type=lambda kv: kv.split("="), metavar="env=VALUE",
                                help="Comma-separated environment variables for the service. Example: --service-env KEY1:VAL1,KEY2:VAL2")

    args = parser.parse_args()
    main(args)
