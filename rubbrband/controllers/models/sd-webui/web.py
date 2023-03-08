import argparse
import os
import subprocess
import sys

import requests


def parse_args():
    """Parse sd-webui web arguments."""

    parser = argparse.ArgumentParser(description="Create webui for stable diffusion models")
    args = parser.parse_args()
    args.script_dir = os.path.dirname(os.path.realpath(__file__))

    return args


def main():
    """Run the webui script."""
    args = parse_args()

    ckpt_path = os.path.join(args.script_dir, "sd-v1-4-full-ema.ckpt")
    if not os.path.isfile(ckpt_path):
        url = "https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4-full-ema.ckpt"
        response = requests.get(url)
        if response.status_code == 200:
            with open(ckpt_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to download checkpoint file. Status code: {response.status_code}")
            sys.exit(1)

    if "rb-sd-webui" in subprocess.check_output(["docker", "ps", "-a"]).decode("utf-8"):
        subprocess.call(["docker", "stop", "rb-sd-webui"])
        subprocess.call(["docker", "rm", "rb-sd-webui"])

    subprocess.call(
        [
            "docker",
            "run",
            "--name",
            "rb-sd-webui",
            "--gpus",
            "all",
            "-it",
            "-d",
            "-v",
            os.path.join(args.script_dir, "sd-v1-4-full-ema.ckpt")
            + ":/home/engineering/stable-diffusion-webui/models/Stable-diffusion/sd-v1-4-full-ema.ckpt",
            "-d",
            "rubbrband/sd-webui:latest",
        ]
    )

    subprocess.call(
        [
            "docker",
            "exec",
            "-it",
            "rb-sd-webui",
            "/bin/bash",
            "-c",
            "bash webui.sh --xformers --share --enable-insecure-extension-access",
        ]
    )


if __name__ == "__main__":
    main()
