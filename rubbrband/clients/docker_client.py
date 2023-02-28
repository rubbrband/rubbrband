import docker
import typer
from rich.progress import Progress

tasks = {}

try:
    DOCKER_CLIENT = docker.from_env()
except docker.errors.DockerException:
    typer.echo("Docker is not running. Please start Docker and try again.")
    exit()


# Show task progress (red for download, green for extract)
def show_progress(line, progress):
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def pull_image(image_name):
    with Progress() as progress:
        resp = DOCKER_CLIENT.api.pull(image_name, stream=True, decode=True)
        for line in resp:
            show_progress(line, progress)


def pull_image_handler(image_name):
    """Pulls an image from the registry if it is not found locally or if the local image is outdated."""

    matched_images = DOCKER_CLIENT.images.list(image_name)
    registry_digest_sha = DOCKER_CLIENT.images.get_registry_data(image_name).attrs["Descriptor"]["digest"]

    if len(matched_images) == 0:
        typer.echo("Model not found locally, downloading model.")
        pull_image(image_name)
    elif matched_images[0].attrs["RepoDigests"][0].split("@")[1] != registry_digest_sha:
        typer.echo("Model found locally, but is outdated. Downloading new model.")
        pull_image(image_name)
    else:
        typer.echo("Model found locally, skipping download.")
