# Rubbrband

![rubbrband train image](https://lh3.googleusercontent.com/u/0/drive-viewer/AAOQEOSUMegyjMpYrbtErUyXXPoE_pVDwFZEVwQd14V9nZryxmlRKIJOHsS98ORQyIJGhv83xWsioXMsH4S2PahOFVmDwmbb=w2966-h2118)

Rubbrband lets you rapidly fine-tune and evalaute the latest open-source machine learning models. Rubbrband installs dependencies, exposes training and inference commands from a CLI interface.

## Getting Started

Rubbrband uses Docker to create separate, working training environments on your machine. Here is the [installation guide for Docker](https://docs.docker.com/engine/install/). If you need help, [contact us on discord](https://discord.gg/BW3R9yK7Fh)

Install Rubbrband using pip:

``` bash
pip install rubbrband
```

To train a model, do the following:

``` bash
rubbrband launch lora
# data folder should contain 5-10 images you want to finetune
rubbrband train lora --dataset-dir ./data
```

## How it works

`rubbrband launch MODEL` pulls a docker image for `MODEL`, with all of the correct dependencies and CUDA drivers installed. Rubbrband uses pre-built Docker images for the latest open-source models: [Dreambooth](https://github.com/XavierXiao/Dreambooth-Stable-Diffusion.git), [LoRA](https://github.com/cloneofsimo/lora), and [ControlNet](https://github.com/lllyasviel/ControlNet).


## LoRA Training Guide

To train LoRA, add some images to a folder named `data`. The author recommends about 7-10 images for good results.

``` bash
rubbrband launch lora
rubbrand train lora --dataset-dir=./data
```

## LoRA Inference guide

After doing a training run on LoRA, run the `rubbrband eval` command.
``` bash
rubbrband launch lora
rubbrband eval lora --input-prompt "a man on the moon in style of <s1><s2>"
```

To view the output image on your local machine, run
``` bash
rubbrband copy-from lora /home/engineering/samples/output.jpg .
```

To copy the checkpoint safetensor file onto your local machine, run the following:
``` bash
rubbrband copy-from lora /home/engineering/output/final_lora.safetensors .
```

## ControlNet Guide

Visit our [ControlNet Training and Inference Guide](https://rubbrband.gitbook.io/cli-docs/training/controlnet) for more information.

## DreamBooth Guide

Visit our [DreamBooth Training and Inference Guide](https://rubbrband.gitbook.io/cli-docs/training/dreambooth) for more information.

## Pull Requests and Feature Requests

Pull requests are welcome! If you have a feature request, please open an issue.

## Supported Compute Platforms

We've mainly tested this on Lambda Labs and Paperspace. Colab doesn't work quite yet, because Colab doesn't play nicely with Docker.

