import os
import subprocess

import docker
import typer

from rubbrband.clients.docker_client import pull_image_handler
from rubbrband.controllers.models.control.train import main as train_control
from rubbrband.controllers.models.dreambooth.train import main as train_dreambooth
from rubbrband.controllers.models.lora.train import main as train_lora

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
    reg_dir: str = typer.Option(..., help="The full path that contains the regularization images."),
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to fine-tune on"),
    log_dir: str = typer.Option(..., help="The full path that contains the directory you want the logs to be in"),
    model_name: str = typer.Option(
        help="The name you want to give your model checkpoint file", default="rubbrband-dreambooth"
    ),
):
    train(ctx, "dreambooth")


@app.command(rich_help_panel="Models :robot:", help="Low-rank adaptation for efficient stable diffusion fine-tuning")
def lora(
    ctx: typer.Context,
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to fine-tune on"),
):
    train(ctx, "lora")


@app.command(rich_help_panel="Models :robot:", help="Control diffusion models by adding extra conditions")
def control(
    ctx: typer.Context,
    dataset_dir: str = typer.Option(..., help="The full path that contains the images you want to fine-tune on"),
):
    train(ctx, "control")


def handle_model_train(params: dict, model: str):
    """Handle the training of a model."""

    if model == "control":
        train_control(**params)
    elif model == "dreambooth":
        train_dreambooth(**params)
    elif model == "lora":
        train_lora()
    else:
        typer.echo(f"Model {model} is not supported.")


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

    handle_model_train(ctx.params, model)


if __name__ == "__main__":
    app()
