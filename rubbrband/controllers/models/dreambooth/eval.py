import subprocess


def main(**kwargs):
    """Run the dreambooth eval script."""
    # Execute the command inside a Docker container
    cmd = (
        f"conda run --no-capture-output -n ldm "
        f"python /home/engineering/JoePenna-Dreambooth/scripts/stable_txt2img.py "
        f"--ddim_eta 0.0 "
        f"--n_samples 8 "
        f"--n_iter 1 "
        f"--scale 10.0 "
        f"--ddim_steps 100 "
        f"--ckpt {kwargs['log_dir']} "
        f"--prompt '{kwargs['input_prompt']}' "
        f"--outdir /home/engineering/samples"
    )
    subprocess.run(["docker", "exec", "-it", "rb-dreambooth", "/bin/bash", "-c", cmd])


if __name__ == "__main__":
    main()
