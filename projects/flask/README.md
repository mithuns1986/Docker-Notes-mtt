## TODO

- THIS SHOULD BE PURE FLASK IN DOCKER

## Setting Up a Flask Application with Nginx in Docker

This guide will detail how to deploy a Flask application using Docker, with Nginx acting as a reverse proxy.

### Create a Flask Application

Let's start by creating a simple Flask app:

app.py:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask running in Docker!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
```

## Dockerizing the Flask App

For this step, you'll need a Dockerfile:

```Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

And a requirements.txt file:

```
flask==2.0.1
```

### Setting up Nginx

First, create an Nginx configuration file named `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://flask_app:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Next, you'll need a `docker-compose.yml` file to orchestrate the Flask and Nginx containers:

```yaml
version: '3'

services:
  flask_app:
    build: .
    ports:
      - "5000:5000"

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - flask_app
```

### Deploying with Docker Compose

With the above files in place, you can now use Docker Compose to deploy both the Flask app and the Nginx server:

```bash
docker-compose up
```

Once the deployment is complete, you can navigate to `http://localhost` in your web browser. You should see the message "Hello from Flask running in Docker!", served through Nginx.
