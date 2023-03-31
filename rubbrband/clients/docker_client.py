import docker
import typer
from rich.progress import Progress

tasks = {}

try:
    DOCKER_CLIENT = docker.from_env()
except docker.errors.DockerException:
    typer.echo("Docker is not running as root. Please start Docker or run sudo su root.")
    exit()


def show_progress(line, progress):
    """Show progress of a docker pull (red for download, green for extract)"""
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks:
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])

    # remove the download task if complete
    download_id = f'[red][Download {line["id"]}]'
    if line["status"] == "Extracting" and download_id in tasks:
        progress.remove_task(tasks[download_id])
        del tasks[download_id]


def pull_image(image_name):
    with Progress() as progress:
        resp = DOCKER_CLIENT.api.pull(image_name, stream=True, decode=True)
        for line in resp:
            show_progress(line, progress)


def pull_image_handler(image_name):
    """Pulls an image from the registry if it is not found locally or if the local image is outdated."""

    matched_images = DOCKER_CLIENT.images.list(image_name)
    registry_digest_sha = DOCKER_CLIENT.images.get_registry_data(image_name).attrs["Descriptor"]["digest"]

    try:
        local_digest_sha = matched_images[0].attrs["RepoDigests"][0].split("@")[1]
    except IndexError:
        local_digest_sha = None

    if len(matched_images) == 0:
        typer.echo("Model not found locally, downloading model.")
        pull_image(image_name)
    elif local_digest_sha != registry_digest_sha:
        typer.echo("Model found locally, but is outdated. Downloading new model.")
        pull_image(image_name)
    else:
        typer.echo("Model found locally, skipping download.")


def get_container(container_name):
    """Returns a container object if it exists and is running."""
    try:
        container = DOCKER_CLIENT.containers.get(container_name)
    except docker.errors.NotFound:
        typer.echo("Model not found, try running rubbrband launch <model>")
        return

    if container.status != "running":
        typer.echo("Model is not running, attempting to start model.")
        try:
            container.start()
        except docker.errors.APIError:
            typer.echo("Unable to start model. Please try again.")
            return

    return container
