import subprocess

import docker
import typer

from rubbrband.controllers.models.control.eval import main as eval_control
from rubbrband.controllers.models.dreambooth.eval import main as eval_dreambooth
from rubbrband.controllers.models.lora.eval import main as eval_lora

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
    log_dir: str = typer.Option(
        help="Path inside the container that contains the checkpoint file",
        default="/home/engineering/log-dir/*/checkpoints/last.ckpt",
    ),
):
    eval(ctx, "dreambooth")


@app.command(rich_help_panel="Models :robot:", help="Low-rank adaptation for efficient stable diffusion fine-tuning")
def lora(
    ctx: typer.Context,
    input_prompt: str = typer.Option(..., help="The prompt to input into the trained model."),
):
    eval(ctx, "lora")


def control_callback(annotator_type: str):
    """Callback for the control command."""
    valid_annotators = ["canny", "depth", "hed", "mlsd", "normal", "openpose", "scribble", "seg"]

    if annotator_type not in valid_annotators:
        typer.echo(f"Invalid annotator type. Valid types are: {', '.join(valid_annotators)}")
        return


@app.command(rich_help_panel="Models :robot:", help="Low-rank adaptation for efficient stable diffusion fine-tuning")
def control(
    ctx: typer.Context,
    annotator_type: str = typer.Option(..., callback=control_callback, help="The edge detector to use."),
):
    eval(ctx, "control")


def handle_model_eval(params: dict, model: str):
    """Handle which model to run."""

    if model == "control":
        eval_control(**params)
    elif model == "dreambooth":
        eval_dreambooth(**params)
    elif model == "lora":
        eval_lora(**params)
    else:
        typer.echo(f"Model {model} is not supported.")

    # move file from docker container to local directory
    # the file is located at /home/engineering/samples/output.jpg
    # the file is moved to the current directory
    subprocess.run(["docker", "cp", f"rb-{model}:/home/engineering/samples", "."])


def eval(ctx: typer.Context, model: str):
    """Entrypoint for evaluating a model."""

    try:
        container = client.containers.get(f"rb-{model}")
    except docker.errors.NotFound:
        typer.echo(f"Container rb-{model} does not exist. Please train the model first.")
        return

    if container.status != "running":
        container.start()

    handle_model_eval(ctx.params, model)
    typer.echo("Inference complete. Check the current directory for the output image.")


if __name__ == "__main__":
    app()
