# Project-HAILML

## Project Description
Open WebUI is being used to provide an easily maintained UI for users to interact with a range of AI models. The team has `Kubernetes` and `Ray` infrastructure deployed to serve models. Project-HAILML is a repository for data scientists / engineers to integrate customized model deployments into the UI.

## Open WebUI

Open WebUI enables OpenAI and Ollamma integration, in addition to supporting custom inference endpoints.

## Ray
We use `Ray Serve` to deploy models. `Ray Serve` allows users to serve models to both local and remote (`Kubernetes`) `Ray Clusters` through adding a simple Python decorator. See [here](https://docs.ray.io/en/latest/serve/getting_started.html) for more information.  

## Overview

 - **deployments/**: all model deployments are located at `deployments/<model_name>.py`. Each model will include a `README.md` describing the model and installation process, `requirements.txt` (specific model requirements), `model.py` (model code for deployment) and `test.py` (example HTTP request)
 - **pipes/**: Open WebUI Pipe functions to integrate model deployment into the UI
 - **schemas/**: data classes and model schemas
 - **pyproject.toml and uv.lock**: These files outline the base dependencies for contributing to the project. You will likely need to install specific model requirements for testing, but these should be specified in the `deployments/` folder.

## Developement
Read below to integrate a new model into Open WebUI

### Standards

Project-HAILML applies Black formatting as a pre-commit hook.

Use `uv` to manage dependencies.

### Getting started

Initialise `uv` environment 

```
pip install uv
uv sync
```

To test integration it is easiest to serve Open WebUI locally. To do this run:
```open-webui serve```
This will create a secret key for you a host the UI at [http://localhost:8080](http://localhost:8080). Go to the url and create a dummy account and login. Now you will be able to test adding new `Pipe Functions` (custom models) to the UI. 

You can also test Ray Serve locally by running the following to create a local `Ray Cluster` 
```ray start --head```


### Custom Model Integration Using Ray Serve
1. **Create a working model class**: the class should load model in `self.init` and execute model inference + return output with `self.pipline`.
2. **Convert to Ray Serve deployment**: add `ray.serve.deployment` decorator and bind to an app. See [here](https://docs.ray.io/en/latest/serve/getting_started.html) or `deployments.phi.model` for examples
3. **Serve locally**: execute `serve run deployments.<model_name>.model:<app_name>` to serve the model locally
4. **Test local deployment**: create a `test.py` file performing a test HTTP request to your deployment. Make sure it works as expected
5. **Create Pipe Function**: The Pipe Function is code added to Open WebUI enabling it to send requests to your deployment and add it to the chat interface. See [here](https://docs.openwebui.com/features/plugin/functions/pipe/#introduction-to-pipes) or `pipes/` for examples. The class must be called `Pipe` and include `Valves` sub-class, `init` and `pipe` functions. Store your `Pipe` at `pipes/<model_name>.py`
6. **Add model to Open WebUI**: Go to [http://localhost:8080/workspace/functions/create](http://localhost:8080/workspace/functions/create), copy and paste your `Pipe` into the code-editor and save (make sure to provide appropriate name and description). Then set the state to active, and test by creating a `new chat` (top left-hand corner), selecting your new model


### Ray Kubernetes Deployment
***TODO convert your local Ray Serve deployment to Kubernetes***
