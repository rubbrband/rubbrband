import argparse
import subprocess


def parse_args():
    """Parse dreambooth eval arguments."""
    parser = argparse.ArgumentParser(description="Run a Docker container with Dreambooth stable_txt2img.py")
    parser.add_argument(
        "-i", "--input_prompt", type=str, required=True, help="Input prompt passed to your fine-tuned model"
    )
    parser.add_argument(
        "-l",
        "--logdir",
        type=str,
        help="the directory containing the experiment logs (default: experiment_logs)",
        default="experiment_logs",
    )
    return parser.parse_args()


def main(**kwargs):
    """Run the dreambooth eval script."""
    # Execute the command inside a Docker container
    cmd = (
        f"python scripts/stable_txt2img.py "
        f"--ddim_eta 0.0 "
        f"--n_samples 8 "
        f"--n_iter 1 "
        f"--scale 10.0 "
        f"--ddim_steps 100 "
        f"--ckpt {kwargs['logdir']}/*/checkpoints/last.ckpt "
        f"--prompt '{kwargs['input_prompt']}' "
        f"--outdir /home/engineering/samples"
    )
    subprocess.run(["docker", "exec", "-it", "rb-dreambooth", "/bin/bash", "-c", cmd])


if __name__ == "__main__":
    main()
