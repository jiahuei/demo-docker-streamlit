# Setup / Dependencies


## Git (optional but recommended)

1. (Optional) Install Git & GitHub Desktop
    * https://git-scm.com/downloads
    * https://desktop.github.com/


## Docker

1. Install Docker Desktop
    * https://www.docker.com/products/docker-desktop

2. For Windows, you might want to limit the resources consumed by the WSL virtual machine
    * Edit the file `resources/.wslconfig`
    * Place it in `C:\Users\<yourUserName>` directory
    * Reference: https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig

3. Build the Docker image:
    * From scratch:
        1. Change terminal working directory to this directory
        2. Run `docker build -f Dockerfile -t demo-docker/python:3.9 .`
    * Alternatively, pull a pre-built image from Docker Hub:
        1. Run `docker pull jiahuei/pytorch:1.9-cpu-opencv`
        2. Tag the image: `docker tag jiahuei/pytorch:1.9-cpu-opencv demo-docker/python:3.9`


## VS Code Development Environment with Docker

This is to use Docker images as dev envs for VS Code.
ALternatively, *Anaconda* or *virtualenv* can be used.

1. Launch VS Code and install extensions:
    * `ms-azuretools.vscode-docker`
    * `ms-vscode-remote.remote-containers`

2. Add `.devcontainer/devcontainer.json` to root
    * Specify the Docker image: 
        ```
        "image": "demo-docker/python:3.9",
        ```
    * Specify the extensions:
        ```
        "extensions": [
            "ms-python.python",
            "ms-python.vscode-pylance"
        ],
        ```
    * Example `devcontainer.json`:
        ```
        {
            "image": "demo-docker/python:3.9",
            "extensions": ["ms-python.python"],
        }
        ```

3. Run VS Code command: `Remote-Containers: Open Folder in Container`
    * ![Remote 0](../resources/vscode-screen/remote%20(0).png)

4. VS Code will build the container, connect to it, and install extensions
    
    * ![Remote 1](../resources/vscode-screen/remote%20(1).png)
    * ![Remote 2](../resources/vscode-screen/remote%20(2).png)
    * ![Remote 4](../resources/vscode-screen/remote%20(4).png)
    * You can view the container logs using this command:
        - ![Remote 3](../resources/vscode-screen/remote%20(3).png)

5. Reload VS Code to use the extensions
    * ![Remote 5](../resources/vscode-screen/remote%20(5).png)
    * ![Remote 6](../resources/vscode-screen/remote%20(6).png)

6. Completed setup:
    * ![Remote 7](../resources/vscode-screen/remote%20(7).png)

