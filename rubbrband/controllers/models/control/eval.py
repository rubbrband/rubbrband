import os
import subprocess

def main(**kwargs):
    """Run the control eval script."""
    ckpt = ""
    max_step = 0
    for file in os.listdir(f"{os.getcwd()}/lightning_logs/version_0/checkpoints"):
        if file.endswith(".ckpt"):
            step = int(file.split("-")[1].split(".")[0].split("=")[1])
            if step > max_step:
                max_step = step
                ckpt = f"{os.getcwd()}/lightning_logs/version_0/checkpoints/" + file
    subprocess.call(["rubbrband", "web", "sd-webui", "--control-processor", ckpt])


if __name__ == "__main__":
    main()
