import os
import subprocess

import requests


def main(**kwargs):
    """Run the control eval script."""
    # in the directory /home/engineering/ControlNet/lightning_logs/version_0/checkpoints/
    # there are many checkpoints in the format epoch=[epoch]-step=[step].ckpt
    # get the checkpoint with the highest step and store this as ckpt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ckpt = ""
    max_step = 0
    for file in os.listdir(f"{os.getcwd()}/lightning_logs/version_0/checkpoints"):
        if file.endswith(".ckpt"):
            step = int(file.split("-")[1].split(".")[0].split("=")[1])
            if step > max_step:
                max_step = step
                ckpt = f"{os.getcwd()}/lightning_logs/version_0/checkpoints/" + file
    subprocess.call(
        [
            "rubbrband",
            "web",
            "sd-webui",
            "--control-processor",
            ckpt
        ]
    )


if __name__ == "__main__":
    main()
