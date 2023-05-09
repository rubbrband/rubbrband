import subprocess
from typing import Optional

import docker
import typer
from yaspin import yaspin

from rubbrband.clients import docker_client
from rubbrband.controllers import eval, train, web
from rubbrband.version import VERSION

__author__ = "Rubbrband"
__version__ = VERSION

app = typer.Typer(no_args_is_help=True, rich_markup_mode="rich")
app.add_typer(train.app, name="train", subcommand_metavar="MODEL")
app.add_typer(eval.app, name="eval", subcommand_metavar="MODEL")
app.add_typer(web.app, name="web", subcommand_metavar="MODEL")
image_models = ["lora", "dreambooth", "control"]
webui_models = ["sd-webui"]

try:
    client = docker.from_env()
except docker.errors.DockerException:
    typer.echo("Docker is not running as root. Please start Docker or run sudo su root.")
    exit()


# create our database of models
db = {
    "lora": {
        "description": "Low-rank adaptation for efficient stable diffusion fine-tuning",
        "shape": "anything",
    },
    "dreambooth": {
        "description": "Stable diffusion models, trained with dreambooth method",
        "shape": "anything",
    },
    "control": {
        "description": "Control diffusion models by adding extra conditions",
        "shape": "anything",
    },
    "sd-webui": {
        "description": "Stable diffusion models, trained with webui method",
        "shape": "anything",
    },
}

# Pass singleton objects to our subcommands
train.client = client
eval.client = client
web.client = client
train.db = db
eval.db = db
web.db = db


def version_callback(value: bool):
    """Display the current version of Rubbrband"""
    if value:
        typer.echo(f"Rubbrband CLI version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", help="Display the current version of Rubbrband", callback=version_callback, is_eager=True
    ),
):
    """
    The Rubbrband CLI allows you to rapidly train and evaluate models.
    """
    pass


@app.command()
def models():
    """List all supported MODELS :robot:"""
    typer.echo("Supported Models:")
    typer.echo(f"{'NAME':12} DESCRIPTION")
    for key, val in db.items():
        typer.echo(f"{key:12} {val['description']}")


@app.command()
def ls():
    """List all running MODELS :robot:"""
    typer.echo("Running Models:")
    containers = client.containers.list()

    # filter containers that start with rb-
    for container in containers:
        if container.name.startswith("rb-"):
            typer.echo(container.name)


@app.command()
def stop(model: str):
    """
    Stop a running MODEL :robot:

    MODEL is the name of the model.

    Example: rubbrband stop lora
    """
    with yaspin() as sp:
        sp.text = "Stopping Docker Container"

        container_name = f"rb-{model}"
        container = docker_client.get_container(container_name)

        if container:
            container.stop()


@app.command()
def copy_to(model: str, src: str, dest: str):
    """
    Copy a file from your computer to a running MODEL :robot:

    MODEL is the name of the model.
    SRC is the path to the file on your computer.
    DEST is the path to the file on the model.

    Example: rubbrband copy-to lora /path/on/my-computer/image.png /path/on/my-model/image.png
    """
    with yaspin() as sp:
        sp.text = "Copying File"

        container_name = f"rb-{model}"
        container = docker_client.get_container(container_name)

        if container:
            subprocess.run(["docker", "cp", src, f"{container.name}:{dest}"])


@app.command()
def copy_from(model: str, src: str, dest: str):
    """
    Copy a file from a running MODEL to your computer :robot:

    MODEL is the name of the model.
    SRC is the path to the file on the model.
    DEST is the path to the file on your computer.

    Example: rubbrband copy-from lora /path/on/my-model/image.png /path/on/my-computer/image.png
    """
    with yaspin() as sp:
        sp.text = "Copying File"

        container_name = f"rb-{model}"
        container = docker_client.get_container(container_name)
        if container:
            subprocess.run(["docker", "cp", f"{container.name}:{src}", dest])


@app.command()
def launch(model: str):
    """
    Launch a new MODEL :robot:

    MODEL is the name of the model to launch.

    Example: rubbrband launch lora
    """

    if model not in db:
        typer.echo("Model not found")
        return

    typer.echo("Downloading model. This may take up to 10 minutes.")
    image_name = f"rubbrband/{model}"
    docker_client.pull_image_handler(image_name)

    if model in webui_models:
        typer.echo("Finished. This model is based on a web interface.")
        typer.echo(
            "When you're ready, run rubbrband web {model} to launch the interface. \
                   We'll let you know how to access it."
        )
    else:
        typer.echo(f"Finished. Run rubbrband train {model} to train this model on sample data.")


@app.command()
def enter(model: str):
    """
    Enter into a running MODEL :robot:

    MODEL is the name of the model.

    Example: rubbrband enter lora
    """
    # if container not running, start it
    with yaspin() as sp:
        sp.text = "Launching Docker Container"

        container_name = f"rb-{model}"
        try:
            container = client.containers.get(container_name)
        except docker.errors.NotFound:
            client.containers.run(container_name, detach=True, name=container_name, tty=True, stdin_open=True)

        container = client.containers.get(container_name)

        if container.status != "running":
            container.start()

    subprocess.run(["docker", "exec", "-it", container_name, "/bin/bash"])


if __name__ == "__main__":
    app()
