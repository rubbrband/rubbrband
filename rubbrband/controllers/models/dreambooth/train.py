import argparse
import os
import subprocess
import sys

import GPUtil
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


def check_gpu():
    gpus = GPUtil.getGPUs()

    # Check if there is at least one GPU available
    if len(gpus) > 0:
        # Get the first GPU and check its VRAM
        gpu = gpus[0]
        if gpu.memoryTotal > 25:
            return True
        else:
            print("Graphics card found, but it has less than 25GB VRAM.")
            return False
    else:
        print("No graphics card found.")
        return False


def main(**kwargs):
    """Run the dreambooth train script."""

    script_dir = os.path.dirname(os.path.realpath(__file__))
    ckpt_path = os.path.join(script_dir, "v1-5-pruned.ckpt")

    gpu_ready = check_gpu()

    if not gpu_ready:
        print("You need a GPU with at least 25GB VRAM to finetune the model.")
        sys.exit(1)

    if not os.path.isfile(ckpt_path):
        print("Downloading SD checkpoint file. This is about 7GB.")
        url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt"
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

    datasetdir = os.path.abspath(kwargs["dataset_dir"])
    regdir = os.path.abspath(kwargs["reg_dir"])

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
            os.path.join(script_dir, "v1-5-pruned.ckpt") + ":/home/engineering/v1-5-pruned.ckpt",
            "-v",
            datasetdir + ":/home/engineering/dataset-dir",
            "-v",
            regdir + ":/home/engineering/reg-dir",
            "-d",
            "rubbrband/dreambooth:latest",
        ]
    )

    class_word = kwargs["class_word"]
    model_name = kwargs["model_name"]

    # count the number of images in dataset_dir, including files in subdirectories
    num_images = sum(len(files) for _, _, files in os.walk(kwargs["dataset_dir"]))
    training_steps = num_images * 70

    if num_images < 50:
        print("You should have least 100 images to finetune the model. Otherwise, you may not get good results")

    conda_cmd = (
        "conda run --no-capture-output -n ldm",
        "python /home/engineering/JoePenna-Dreambooth/main.py "
        "--base /home/engineering/JoePenna-Dreambooth/configs/stable-diffusion/v1-finetune_unfrozen.yaml",
        f"-t --actual_resume /home/engineering/v1-5-pruned.ckpt -n {model_name} --gpus 0,",
        "--data_root /home/engineering/dataset-dir --reg_data_root /home/engineering/reg-dir",
        f"--token rbsubject --class_word {class_word} --max_training_steps {training_steps} --no-test",
    )

    subprocess.call(
        " ".join(["docker", "exec", "-it", "rb-dreambooth", "/bin/bash", "-c", f"'{' '.join(conda_cmd)}'"]), shell=True
    )


if __name__ == "__main__":
    main()
