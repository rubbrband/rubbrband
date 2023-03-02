import os
import subprocess

import docker
import typer
from yaspin import yaspin

db = {}
client = None
app = typer.Typer(no_args_is_help=True)


@app.callback()
def main():
    """
    Evaluate a trained MODEL :robot:

    Example: rubbrband eval lora
    """
    pass


@app.command(rich_help_panel="Models :robot:", help="Stable diffusion models, trained with dreambooth method")
def dreambooth(
    ctx: typer.Context,
    input_prompt: str = typer.Option(..., help="The prompt to input into the trained model."),
    logdir: str = "experiment_logs",
):
    eval(ctx, "dreambooth")


@app.command(rich_help_panel="Models :robot:", help="Low-rank adapation for efficient stable diffusion fine tuning")
def lora(
    ctx: typer.Context,
    input_prompt: str = typer.Option(..., help="The prompt to input into the trained model."),
):
    eval(ctx, "lora")


@app.command(rich_help_panel="Models :robot:", help="Low-rank adapation for efficient stable diffusion fine tuning")
def control(
    ctx: typer.Context,
    annotator_type: str = typer.Option(..., help="The edge detector to use."),
):
    valid_annotators = ["canny", "depth", "hed", "mlsd", "normal", "openpose", "scribble", "seg"]

    if annotator_type not in valid_annotators:
        typer.echo(f"Invalid annotator type. Valid types are: {', '.join(valid_annotators)}")
        return

    this_dir = os.path.dirname(os.path.abspath(__file__))

    with yaspin():
        typer.echo(["/bin/bash", f"{this_dir}/models/control/infer.sh", annotator_type])
        subprocess.run(["chmod", "a+x", f"{this_dir}/models/control/infer.sh"])
        subprocess.run(["/bin/bash", f"{this_dir}/models/control/infer.sh", annotator_type])


def eval(ctx: typer.Context, model: str):
    """Entrypoint for evaluating a model."""

    try:
        container = client.containers.get(f"rb-{model}")
    except docker.errors.NotFound:
        typer.echo(f"Container rb-{model} does not exist. Please train the model first.")
        return

    if container.status != "running":
        container.start()

    this_dir = os.path.dirname(os.path.abspath(__file__))

    # Convert the parameters to a list of strings
    params = []
    for key, value in ctx.params.items():
        params.append(f"--{key}")
        params.append(value)

    with yaspin():
        typer.echo(["/bin/bash", f"{this_dir}/models/{model}/infer.sh"] + params)
        subprocess.run(["chmod", "a+x", f"{this_dir}/models/{model}/infer.sh"])
        # add a parameter for prompt
        subprocess.run(["/bin/bash", f"{this_dir}/models/{model}/infer.sh"] + params)

        # move file from docker container to local directory
        # the file is located at /home/engineering/samples/output.jpg
        # the file is moved to the current directory
        subprocess.run(["docker", "cp", f"rb-{model}:/home/engineering/samples", "."])

    typer.echo("Inference complete. Check the current directory for the output image.")


if __name__ == "__main__":
    app()
