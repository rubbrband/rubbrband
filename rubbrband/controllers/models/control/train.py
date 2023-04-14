import os
import shutil
import subprocess
import sys

import requests


def main(**kwargs):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isfile(os.path.join(script_dir, "v1-5-pruned.ckpt")):
        url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt"
        response = requests.get(url)
        with open(os.path.join(script_dir, "v1-5-pruned.ckpt"), "wb") as f:
            f.write(response.content)

    if shutil.which("nvidia-smi"):
        gpu_arg = "--gpus all"
    else:
        gpu_arg = ""

    if not os.path.isfile(os.path.join(kwargs["dataset_dir"], "prompt.json")):
        print(
            "The dataset directory is missing a prompt.json file. "
            + "Please refer to the documentation for more information."
        )
        sys.exit(1)
    if "rb-control" in subprocess.check_output(["docker", "ps", "-a"]).decode("utf-8"):
        subprocess.call(["docker", "stop", "rb-control"])
        subprocess.call(["docker", "rm", "rb-control"])
    subprocess.call(["mkdir", "lightning_logs"])

    if gpu_arg:
        subprocess.call(
            [
                "docker",
                "run",
                "--name",
                "rb-control",
                "--gpus",
                "all",
                "-it",
                "-d",
                "-v",
                os.path.join(script_dir, "v1-5-pruned.ckpt") + ":/home/engineering/ControlNet/models/v1-5-pruned.ckpt",
                "-v",
                os.path.abspath(kwargs["dataset_dir"]) + ":/home/engineering/ControlNet/training/fill50k",
                "-v",
                os.path.abspath("lightning_logs") + ":/home/engineering/ControlNet/lightning_logs",
                "-d",
                "rubbrband/control:latest",
            ]
        )
    else:
        subprocess.call(
            [
                "docker",
                "run",
                "--name",
                "rb-control",
                "-it",
                "-d",
                "-v",
                os.path.join(script_dir, "v1-5-pruned.ckpt") + ":/home/engineering/ControlNet/models/v1-5-pruned.ckpt",
                "-v",
                os.path.abspath(kwargs["dataset_dir"]) + ":/home/engineering/ControlNet/training/fill50k",
                "-d",
                "rubbrband/control:latest",
            ]
        )

    conda_cmd = (
        "conda run --no-capture-output -n control sudo chmod 777 ./ && "
        "conda run --no-capture-output -n control sudo chmod 777 ./* && "
        "conda run --no-capture-output -n control "
        "python tool_add_control.py ./models/v1-5-pruned.ckpt ./models/control_sd15_ini.ckpt &&",
        "conda run --no-capture-output -n control sudo chmod 777 ./* && "
        "conda run --no-capture-output -n control python tutorial_train.py",
    )

    docker_cmd = f"docker exec -it rb-control /bin/bash -c \"{' '.join(conda_cmd)}\""
    print(docker_cmd, flush=True)
    subprocess.call(f"script -c '{docker_cmd}'", shell=True)


if __name__ == "__main__":
    main()
