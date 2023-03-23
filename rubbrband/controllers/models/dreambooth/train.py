import argparse
import os
import subprocess
import sys
from datetime import datetime

import GPUtil
import requests


def parse_args():
    """Parse dreambooth train arguments."""

    parser = argparse.ArgumentParser(description="Fine-tune Dreambooth on a dataset with a regularization prompt")
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
        help="The full path that contains the images you want to fine-tune on.",
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
    parser.add_argument(
        "--log_dir",
        "-l",
        type=str,
        required=False,
        help="The full path that contains the directory you want the logs to be in",
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
        print("You need a GPU with at least 25GB VRAM to fine-tune the model.")
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

    # find the token for the dataset directory
    # go inside the dataset directory, and find the names of the directories
    # inside it. The first directory to have another directory called class-name inside it
    # is the token
    token = None
    for dir in os.listdir(datasetdir):
        if os.path.isdir(os.path.join(datasetdir, dir)):
            if os.path.isdir(os.path.join(datasetdir, dir, kwargs["class_word"])):
                token = dir
                break
    if token is None:
        print(
            "The dataset-directory is not in the correct format. \
              Refer to https://rubbrband.gitbook.io/cli-docs/training-models/dreambooth to correct it."
        )
        sys.exit(1)

    regdir = os.path.abspath(kwargs["reg_dir"])
    logdir = os.path.abspath(kwargs["log_dir"])

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
            "-v",
            logdir + ":/home/engineering/log-dir",
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

    # get current datetime in UTC format
    now_utc = datetime.utcnow()

    # create log file name with timestamp
    log_file_name = f"logfile-out{now_utc.strftime('%Y-%m-%dT%H-%M-%SZ')}_{model_name}.log"

    # create log directory inside the docker container
    subprocess.call("docker exec rb-dreambooth /bin/bash -c 'mkdir -p /home/engineering/log-dir/'", shell=True)

    conda_cmd = (
        "conda run --no-capture-output -n ldm",
        "python /home/engineering/JoePenna-Dreambooth/main.py "
        "--base /home/engineering/JoePenna-Dreambooth/configs/stable-diffusion/v1-finetune_unfrozen.yaml",
        f"-t --actual_resume /home/engineering/v1-5-pruned.ckpt -n {model_name} --gpus 0,",
        f"--token {token} --class_word {class_word} --max_training_steps {training_steps} --no-test",
        "--data_root /home/engineering/dataset-dir --reg_data_root /home/engineering/reg-dir",
        "--logdir /home/engineering/log-dir",
    )

    docker_cmd = f"docker exec -it rb-dreambooth /bin/bash -c \"{' '.join(conda_cmd)}\""

    # run the docker container and save the output to a log file
    subprocess.call(f"script -c '{docker_cmd}' {logdir}/{log_file_name}", shell=True)


if __name__ == "__main__":
    main()
