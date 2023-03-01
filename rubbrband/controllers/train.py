import os
import subprocess

import docker
import typer
from yaspin import yaspin

from rubbrband.clients.docker_client import pull_image_handler

db = {}
client = None
app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    """
    Train a MODEL :robot:

    Example: rubbrband train lora
    """


@app.command(rich_help_panel="Models :robot:", help="Stable diffusion models, trained with dreambooth method")
def dreambooth(
    ctx: typer.Context,
    class_word: str = typer.Option(
        ..., help="The name that you want to give to the class of images that you'll want to generate"
    ),
    regularization_prompt: str = typer.Option(
        ..., help="The prompt to regularize the images. Try to describe the type of images you want to generate"
    ),
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to finetune on"),
    logdir: str = "experiment_logs",
):
    train(ctx, "dreambooth")


@app.command(rich_help_panel="Models :robot:", help="Low-rank adapation for efficient stable diffusion fine tuning")
def lora(
    ctx: typer.Context,
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to finetune on"),
):
    train(ctx, "lora")


@app.command(rich_help_panel="Models :robot:", help="Control diffusion models by adding extra conditions")
def control(
    ctx: typer.Context,
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to finetune on"),
):
    image_name = "rubbrband/control"
    container_name = "rb-control"
    pull_image_handler(image_name)

    abs_path = os.path.abspath(ctx.params["dataset_dir"])

    try:
        container = client.containers.get(container_name)

        # stop and remove container if it is already running
        if container.status == "running":
            container.stop()
            container.remove()

    except docker.errors.NotFound:
        pass
    this_dir = os.path.dirname(os.path.abspath(__file__))

    subprocess.run(["chmod", "a+x", f"{this_dir}/models/control/train.sh"])
    # ctx.args is a list of arguments passed to the train command
    subprocess.run(["/bin/bash", f"{this_dir}/models/control/train.sh", abs_path])


# '''name''' corresponds to the name column in db.csv
# the option '''-d''' or '''--dataset_dir''' is the path to the dataset directory
# this directory gets mounted to the container at /home/engineering/data
def train(ctx: typer.Context, model: str):
    """Entrypoint for training a model."""
    if model not in db:
        typer.echo("Model not found")
        return

    image_name = f"rubbrband/{model}"
    container_name = f"rb-{model}"
    pull_image_handler(image_name)

    abs_path = os.path.abspath(ctx.params["dataset_dir"])

    try:
        container = client.containers.get(container_name)

        # stop and remove container if it is already running
        if container.status == "running":
            container.stop()
            container.remove()

    except docker.errors.NotFound:
        pass
    try:
        subprocess.check_output("nvidia-smi")
        device_requests = [docker.types.DeviceRequest(count=-1, capabilities=[["gpu"]])]
    except (
        Exception
    ):  # this command not being found can raise quite a few different errors depending on the configuration
        device_requests = []

    client.containers.run(
        image_name,
        device_requests=device_requests,
        detach=True,
        name=container_name,
        volumes={f"{abs_path}": {"bind": "/home/engineering/data", "mode": "rw"}},
        tty=True,
        stdin_open=True,
    )
    container = client.containers.get(f"rb-{model}")

    if container.status != "running":
        container.start()

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert the parameters to a list of strings
    params = []
    for key, value in ctx.params.items():
        params.append(f"--{key}")
        params.append(value)

    with yaspin():
        subprocess.run(["chmod", "a+x", f"{this_dir}/models/{model}/train.sh"])
        # ctx.args is a list of arguments passed to the train command
        subprocess.run(["/bin/bash", f"{this_dir}/models/{model}/train.sh"] + params)


if __name__ == "__main__":
    app()
