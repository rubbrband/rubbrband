import os
import subprocess
import sys

import requests


def main():
    """Run the webui script."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    ckpt_path = os.path.join(script_dir, "sd-v1-4-full-ema.ckpt")
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
            os.path.join(script_dir, "sd-v1-4-full-ema.ckpt")
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
