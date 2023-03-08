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
    Start a webui for a MODEL :robot:

    Example: rubbrband web sd-webui
    """


@app.command(rich_help_panel="Models :robot:", help="Webui for stable diffusion models")
def sd_webui(
    ctx: typer.Context,
):
    web(ctx, "sd-webui")


# '''name''' corresponds to the name column in db.csv
# the option '''-d''' or '''--dataset_dir''' is the path to the dataset directory
# this directory gets mounted to the container at /home/engineering/data
def web(ctx: typer.Context, model: str):
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

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert the parameters to a list of strings
    params = []
    for key, value in ctx.params.items():
        params.append(f"--{key}")
        params.append(value)

    with yaspin():
        subprocess.run(["chmod", "a+x", f"{this_dir}/models/{model}/web.sh"])
        # ctx.args is a list of arguments passed to the train command
        subprocess.run(["/bin/bash", f"{this_dir}/models/{model}/web.sh"] + params)


if __name__ == "__main__":
    app()
