import argparse
import os
import shutil
import subprocess
import sys

import requests


def parse_args():
    parser = argparse.ArgumentParser(description="Run Rubbrband ControlNet training script")
    parser.add_argument("dataset_dir", help="Path to directory containing training data")

    return parser.parse_args()


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

    if "rb-control" in subprocess.check_output('docker ps -a --format "{{.Names}}"').decode("utf-8"):
        subprocess.call("docker stop rb-control")
        subprocess.call("docker rm rb-control")

    volumes = (
        f"-v {os.path.join(script_dir, 'v1-5-pruned.ckpt')}:/home/engineering/ControlNet/models/v1-5-pruned.ckpt "
        f"-v {os.path.abspath(kwargs['dataset_dir'])}:/home/engineering/ControlNet/training/fill50k"
    )
    subprocess.call(f"docker run --name rb-control {gpu_arg} -it -d {volumes} -d rubbrband/control:latest")

    conda_cmd = (
        "conda run --no-capture-output -n control"
        "python tool_add_control.py ./models/v1-5-pruned.ckpt ./models/control_sd15_ini.ckpt &&"
        "conda run --no-capture-output -n control python tutorial_train.py"
    )

    subprocess.call(f"docker exec -it rb-control /bin/bash -c '{' '.join(conda_cmd)}'", shell=True)


if __name__ == "__main__":
    main()
