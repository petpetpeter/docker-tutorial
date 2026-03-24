# Docker and Docker Compose Tutorial

This guide walks you through containerizing a Python application that uses system-level dependencies. In this example, we use `pyzbar` to decode QR codes, which requires the `libzbar0` system library.

## What you will learn?
- Solving "It works on my machine": How to package system-level dependencies (like libzbar0) so your app runs anywhere.

- Docker Fundamentals: How to write a Dockerfile, build images, and manage containers via the CLI.
- Environment Management: Using .env files and environment variables to keep secrets out of your code.
- Persistent Development: Using Volumes to see code changes in real-time without constantly rebuilding your image.
- Debugging & Inspection: How to "shell into" a running container and view logs to troubleshoot issues.
- Docker Compose: Scaling from a single docker run command to a manageable docker-compose.yaml file for multiple services.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed.
- [Docker Compose](https://docs.docker.com/compose/install/) installed.

---

## Part 0: No Docker -> broken package
1. Clone this repo
```
git clone https://github.com/petpetpeter/docker-tutorial.git
cd docker-tutorial
```

2. Try run the code in python virtual environment
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

3. You would encounter the following error:
```
raise ImportError('Unable to find zbar shared library')
ImportError: Unable to find zbar shared library
```

4. Looking at https://pypi.org/project/pyzbar/ we see that it requires `zbar` system library. We can install it using `apt-get`.

---
## Part 1: Using Docker

### 1. Understanding the Dockerfile

The `Dockerfile` is a blueprint for your container. It specifies the base image, installs dependencies, and copies your code.

- **Base Image**: `python:3.9-slim` (a lightweight Python environment).
- **Working Directory**: `/app` (where the code will be copied to).
- **System Deps**: `apt-get install -y libzbar0` (required for `pyzbar`).
- **Python Deps**: `pip install pyzbar Pillow`.

### 2. Building the Image

Run the following command to build your Docker image and tag it as `qr-decoder`:

```bash
docker build -t qr-decoder .
```

Check your image
```bash
docker images
```

### 3. Running the Container

To run the container, use the `docker run` command.

```bash
docker run -e PYTHONUNBUFFERED=1 qr-decoder:latest
```

Change env variable
```bash
docker run -e PYTHONUNBUFFERED=1 -e API_KEY_THAT_WILL_MAKE_YOU_BANKRUPT=Put-key-here-is-big-no qr-decoder:latest
```

Use .env file instead (For development)
```bash
cp .env.example .env
```
```bash
docker run --env-file .env qr-decoder:latest
```

### 4. Debugging

Try change src/main.py and run again

```bash
docker run --env-file .env qr-decoder:latest
```

> ❔ Nothing changed? Let check what actually run in your container
- try run container again in detatched mode
```bash
docker run -d --env-file .env qr-decoder:latest
```
- view your running containers in background
```bash
docker ps
```
- view logs
```bash
docker logs <container_id> -f
```
- shell into container
```bash
docker exec -it <container_id> /bin/bash
```
- list files in container
```bash
ls
```
- view file content, noticed that the file is not updated
```bash
cat src/main.py
```
- exit container (ctrl+d or type exit)
- stop container
```bash
docker stop <container_id>
```

> 💡 If you want to see the changes you made, you need to rebuild the image


- rebuild image
```bash
docker build -t qr-decoder .
```
- run again
```bash
docker run --env-file .env qr-decoder:latest
```
- view logs again
```bash
docker logs <container_id> -f
```

> ❔ Can we make change without rebuilding the image?

> 💡 Yes, by using volumes

- try making some changes in src/main.py
- run container with volume
```bash
docker run --env-file .env -v $(pwd):/app qr-decoder:latest
```

---

## Part 2: Extending to Docker Compose

As your application grows (e.g., adding a database or multiple services), managing `docker run` commands becomes difficult. **Docker Compose** simplifies this with a YAML configuration.

### 1. The `docker-compose.yaml` File

Our `docker-compose.yaml` defines a service called `qr-decoder`:

- `build: .`: Tells Compose to build the image from the local `Dockerfile`.
- `volumes`: Maps your local directory to `/app` in the container, allowing for "Live Coding" (changes you make locally appear instantly in the container).

### 2. Running with Compose

Instead of building and running manually, just run:

```bash
docker compose up
```

This will:
1. Build the image (if not already built).
2. Start the container defined in the YAML file.


### 3. Try adding more service with different env
- uncomment qr-decoder-2 in docker-compose.yaml
- run `docker compose up`

### 4. Try running in detached mode
```bash
docker compose up -d
```
- view logs
```bash
docker compose logs -f
```
- stop container
```bash
docker compose down
```
---

## Summary of Commands

| Action | Docker CLI | Docker Compose |
| :--- | :--- | :--- |
| **Build** | `docker build -t name .` | `docker compose build` |
| **Run** | `docker run name` | `docker compose up` |
| **Stop** | `docker stop container_id` | `docker compose down` |
| **Clean up** | `docker system prune` | `docker compose down --rmi all` |
