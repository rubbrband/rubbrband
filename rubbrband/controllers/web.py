import docker
import typer

from rubbrband.clients.docker_client import pull_image_handler
from rubbrband.controllers.models.sd_webui.web import main as web_sd_webui

db = {}
client = None
app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    """
    Start a webui for a MODEL :robot:

    Example: rubbrband web sd-webui
    """


@app.command(rich_help_panel="Models :robot:", help="Webui for stable diffusion models")
def sd_webui(
    ctx: typer.Context,
    dreambooth_checkpoint: str = typer.Option(help="Optional path to a dreambooth checkpoint.", default=None),
):
    web(ctx, "sd-webui", dreambooth_checkpoint)


def handle_model_web(params: dict, model: str, dreambooth_checkpoint: str):
    """Handle which model to run."""
    if model == "sd-webui":
        web_sd_webui(dreambooth_checkpoint)
    else:
        typer.echo(f"Model {model} not found")


# '''name''' corresponds to the name column in db.csv
# the option '''-d''' or '''--dataset_dir''' is the path to the dataset directory
# this directory gets mounted to the container at /home/engineering/data
def web(ctx: typer.Context, model: str, dreambooth_checkpoint: str):
    """Entrypoint for training a model."""
    if model not in db:
        typer.echo("Model not found")
        return
    image_name = f"rubbrband/{model}"
    container_name = f"rb-{model}"
    pull_image_handler(image_name)

    try:
        container = client.containers.get(container_name)

        # stop and remove container if it is already running

        if container.status == "running":
            container.stop()
            container.remove()
        container = client.containers.get(container_name)

    except docker.errors.NotFound:
        pass

    handle_model_web(ctx.params, model, dreambooth_checkpoint)


if __name__ == "__main__":
    app()
