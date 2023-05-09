import argparse
import os
import shutil
import subprocess

import requests


def parse_args():
    """Parse control eval arguments."""
    parser = argparse.ArgumentParser(description="Eval ControlNet inside a Docker container")
    parser.add_argument("annotator_type", type=str, help="Type of ControlNet annotator to use")

    return parser.parse_args()


def main(**kwargs):
    """Run the control eval script."""

    pth_name = f"control_sd15_{kwargs['annotator_type']}.pth"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isfile(os.path.join(script_dir, pth_name)):
        url = f"https://huggingface.co/lllyasviel/ControlNet/resolve/main/models/{pth_name}"
        response = requests.get(url)
        with open(os.path.join(script_dir, pth_name), "wb") as f:
            f.write(response.content)

    if not os.path.isfile(os.path.join(script_dir, "v1-5-pruned.ckpt")):
        url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt"
        response = requests.get(url)
        with open(os.path.join(script_dir, "v1-5-pruned.ckpt"), "wb") as f:
            f.write(response.content)

    volumes = (
        f"-v {script_dir}/v1-5-pruned.ckpt:/home/engineering/ControlNet/models/v1-5-pruned.ckpt "
        f"-v {script_dir}/{pth_name}:/home/engineering/ControlNet/models/{pth_name}"
    )

    if subprocess.run(["docker", "ps", "-a", "--filter", "name=rb-control"]).returncode == 0:
        subprocess.run(["docker", "stop", "rb-control"])
        subprocess.run(["docker", "rm", "rb-control"])

    if shutil.which("nvidia-smi"):
        subprocess.run(
            ["docker", "run", "--name", "rb-control", "--gpus", "all", "-it", "-d", volumes, "rubbrband/control:latest"]
        )
    else:
        subprocess.run(["docker", "run", "--name", "rb-control", "-it", "-d", volumes, "rubbrband/control:latest"])

    subprocess.run(
        [
            "docker",
            "exec",
            "-it",
            "rb-control",
            "/bin/bash",
            "-c",
            f"conda run --no-capture-output -n control python gradio_{kwargs['annotator_type']}2image.py",
        ]
    )


if __name__ == "__main__":
    main()
