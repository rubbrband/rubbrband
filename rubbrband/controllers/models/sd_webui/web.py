import os
import subprocess
import sys

import requests


def main(dreambooth_checkpoint: str = None, control_preprocessor: str = None):
    """Run the webui script."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    ckpt_path = os.path.join(script_dir, "v1-5-pruned-emaonly.ckpt")
    if not os.path.isfile(ckpt_path):
        url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt"
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
            ckpt_path
            + ":/home/engineering/stable-diffusion-webui/"
            + "models/Stable-diffusion/v1-5-pruned-emaonly.ckpt",
            "-d",
            "rubbrband/sd-webui:latest",
        ]
    )

    if dreambooth_checkpoint and control_preprocessor:
        # get the last part of the path that is the file name
        dreambooth_checkpoint_name = dreambooth_checkpoint.split("/")[-1]
        control_preprocessor_name = control_preprocessor.split("/")[-1]
        subprocess.run(
            [
                "docker",
                "exec",
                "-it",
                "rb-sd-webui",
                "/bin/bash",
                "-c",
                "git clone --depth 1 https://github.com/Mikubill/sd-webui-controlnet.git "
                + "/home/engineering/stable-diffusion-webui/extensions",
            ]
        )
        subprocess.run(
            [
                "docker",
                "cp",
                dreambooth_checkpoint,
                "rb-sd-webui:/home/engineering/stable-diffusion-webui/"
                + f"models/Stable-diffusion/{dreambooth_checkpoint_name}",
            ]
        )
        subprocess.run(
            [
                "docker",
                "cp",
                control_preprocessor,
                "rb-sd-webui:/home/engineering/stable-diffusion-webui/"
                + f"models/Stable-diffusion/{control_preprocessor_name}",
            ]
        )

    elif dreambooth_checkpoint:
        subprocess.run(
            [
                "docker",
                "cp",
                dreambooth_checkpoint,
                "rb-sd-webui:/home/engineering/stable-diffusion-webui/models/Stable-diffusion/last.ckpt",
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
            "bash webui.sh --api --xformers --share --enable-insecure-extension-access",
        ]
    )


if __name__ == "__main__":
    main()
