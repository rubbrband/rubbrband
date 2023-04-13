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
    for file in os.listdir("{script_dir}", "lightning_logs", "version_0", "checkpoints"):
        if file.endswith(".ckpt"):
            step = int(file.split("-")[1].split(".")[0])
            if step > max_step:
                max_step = step
                ckpt = file
    pth_name = f"control_sd15_{kwargs['annotator_type']}.pth"

    if not os.path.isfile(os.path.join(script_dir, pth_name)):
        url = f"https://huggingface.co/lllyasviel/ControlNet/resolve/main/models/{pth_name}"
        response = requests.get(url)
        with open(os.path.join(script_dir, pth_name), "wb") as f:
            f.write(response.content)

    subprocess.call(
        [
            "rubbrband",
            "web",
            "sd-webui",
            "--dreambooth-checkpoint",
            ckpt,
            "--control-preprocessor",
            os.path.join(script_dir, pth_name),
        ]
    )


if __name__ == "__main__":
    main()
