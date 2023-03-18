import argparse
import subprocess


def parse_args():
    """Parse lora eval arguments."""
    parser = argparse.ArgumentParser(description="Eval lora inside a Docker container")
    parser.add_argument("-i", "--input_prompt", required=True, help="Input prompt passed to your fine-tuned model")
    return parser.parse_args()


def main(**kwargs):
    """Run the lora eval script."""

    # Call the shell command
    command = ["docker", "exec", "-it", "rb-lora", "python", "/home/engineering/infer.py", kwargs["input_prompt"]]
    subprocess.call(command)


if __name__ == "__main__":
    main()
