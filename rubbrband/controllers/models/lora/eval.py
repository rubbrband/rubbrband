import subprocess


def main(**kwargs):
    """Run the lora eval script."""

    # Call the shell command
    command = ["docker", "exec", "-it", "rb-lora", "python", "/home/engineering/infer.py", kwargs["input_prompt"]]
    subprocess.call(command)


if __name__ == "__main__":
    main()
