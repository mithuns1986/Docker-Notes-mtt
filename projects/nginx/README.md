## Setting Up an Nginx Docker Container

This guide will walk you through deploying an Nginx container using Docker and hosting a simple static web page.

### Creating a Static Web Page

For this demonstration, let's start by creating a simple HTML file that we wish to serve via our Nginx server:

Create a directory for your project:

```bash
mkdir nginx_sample_site
cd nginx_sample_site
```

Now, create a index.html file:

```bash
echo "<h1>Welcome to our Nginx Docker Container!</h1>" > index.html
```

### Setting Up Nginx Docker Container

Now, we'll run an Nginx Docker container and mount our static site to it:

```bash
docker run --name nginx_container -p 80:80 -v $(pwd):/usr/share/nginx/html:ro -d nginx:latest
```

- `--name nginx_container`: Names our container "nginx_container" for easy reference.
- `-p 80:80`: Maps port 80 on the host to port 80 on the container.
- `-v $(pwd):/usr/share/nginx/html:ro`: This mounts our current directory (which contains our index.html file) to the default Nginx content directory in the container. The :ro at the end ensures the volume is mounted as read-only for safety.

### Accessing the Static Site

Once the container is up and running, you can access your static website by navigating to:

```
http://localhost
```

You should see a message saying "Welcome to our Nginx Docker Container!"
