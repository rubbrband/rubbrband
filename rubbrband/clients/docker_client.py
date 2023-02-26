import docker
from rich.progress import Progress

tasks = {}
DOCKER_CLIENT = docker.from_env()


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


def image_pull(image_name):
    with Progress() as progress:
        resp = DOCKER_CLIENT.api.pull(image_name, stream=True, decode=True)
        for line in resp:
            show_progress(line, progress)
