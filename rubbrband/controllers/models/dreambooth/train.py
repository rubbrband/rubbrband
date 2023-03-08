import argparse
import os
import subprocess
import sys

import requests


def parse_args():
    """Parse dreambooth train arguments."""

    parser = argparse.ArgumentParser(description="Finetune Dreambooth on a dataset with a regularization prompt")
    parser.add_argument(
        "--class_word",
        "-c",
        type=str,
        required=True,
        help="The name that you want to give to the class of images that you'll want to generate",
    )
    parser.add_argument(
        "--dataset_dir",
        "-d",
        type=str,
        required=True,
        help="The full path that contains the images you want to finetune on.",
    )
    parser.add_argument(
        "--reg_dir",
        "-r",
        type=str,
        required=True,
        help="The full path that contains the regularization images.",
    )
    parser.add_argument(
        "--model_name",
        "-n",
        type=str,
        required=True,
        help="The name you want to give your model checkpoint file.",
    )

    return parser.parse_args()


def main(**kwargs):
    """Run the dreambooth train script."""
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

    if "rb-dreambooth" in subprocess.check_output(["docker", "ps", "-a"]).decode("utf-8"):
        subprocess.call(["docker", "stop", "rb-dreambooth"])
        subprocess.call(["docker", "rm", "rb-dreambooth"])

    subprocess.call(
        [
            "docker",
            "run",
            "--name",
            "rb-dreambooth",
            "--gpus",
            "all",
            "-it",
            "-d",
            "-v",
            os.path.join(script_dir, "sd-v1-4-full-ema.ckpt") + ":/home/engineering/sd-v1-4-full-ema.ckpt",
            "-v",
            kwargs["dataset_dir"] + ":/home/engineering/dataset-dir",
            "-v",
            kwargs["reg_dir"] + ":/home/engineering/reg-dir",
            "-d",
            "rubbrband/dreambooth:latest",
        ]
    )

    class_word = kwargs["class_word"]
    model_name = kwargs["model_name"]

    # count the number of images in dataset_dir, including files in subdirectories
    num_images = sum(len(files) for _, _, files in os.walk(kwargs["dataset_dir"]))
    training_steps = num_images * 70

    subprocess.call(
        [
            "docker",
            "exec",
            "-it",
            "rb-dreambooth",
            "/bin/bash",
            "-c",
            "python main.py " "--base configs/stable-diffusion/v1-finetune_unfrozen.yaml",
            f"-t --actual_resume /home/engineering/sd-v1-4-full-ema.ckpt -n {model_name} --gpus 0,",
            "--data_root /home/engineering/dataset-dir --reg_data_root /home/engineering/reg-dir",
            f" --token rbsubject --class_word {class_word} --max_training_steps {training_steps} --no-test",
        ]
    )


if __name__ == "__main__":
    main()
