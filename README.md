# Rubbrband

![rubbrband train image](https://lh3.googleusercontent.com/u/0/drive-viewer/AAOQEOSUMegyjMpYrbtErUyXXPoE_pVDwFZEVwQd14V9nZryxmlRKIJOHsS98ORQyIJGhv83xWsioXMsH4S2PahOFVmDwmbb=w2966-h2118)

Rubbrband is a Python library built to make it easy to setup and train the latest open-source machine learning models. It sets up dependencies and data loaders all under the hood, and exposes training and inference commands all from a CLI.

## How to use

Rubbrband depends on Docker. Here is the [installation guide for Docker](https://docs.docker.com/engine/install/)

Install it using pip:

```
pip install rubbrband
```

Rubbrband uses pre-built Docker images for the latest open-source models: [Dreambooth](https://github.com/XavierXiao/Dreambooth-Stable-Diffusion.git), [LoRA](https://github.com/cloneofsimo/lora), and [ControlNet](https://github.com/lllyasviel/ControlNetv).

To train a model, do the following:

```
rubbrband launch lora
# ./data should have ~10 images
rubbrband train lora --dataset-dir ./data
```

## How it works

`rubbrband launch MODEL` pulls a docker image for `MODEL`, with all of the correct dependencies and CUDA drivers installed. Once the image is pulled, you'll be able to run commands like `rubbrband train`, `rubbrband eval`, and `rubbrband enter`.

## LoRA Training Guide

To train LoRA, make a folder called `data` and stuff some images in it. The author recommends about 7-10 images for good results.

```
rubbrband launch lora

rubbrand train lora --dataset-dir=./data
```

After training, you should get a checkpoint file in the output directory in your LoRA container.

```
$ rubbrband enter LoRA //enter the docker container

$ ls output
final_lora.safetensors  step_200.safetensors  step_500.safetensors  step_800.safetensors      step_inv_1000.safetensors  step_inv_400.safetensors  step_inv_700.safetensors
step_100.safetensors    step_300.safetensors  step_600.safetensors  step_900.safetensors      step_inv_200.safetensors   step_inv_500.safetensors  step_inv_800.safetensors
step_1000.safetensors   step_400.safetensors  step_700.safetensors  step_inv_100.safetensors  step_inv_300.safetensors   step_inv_600.safetensors  step_inv_900.safetensors
```

final_lora.safetensors is the file you want.
You'll able to use the safetensors file in a Jupyter Notebook like this:

```
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from lora_diffusion import tune_lora_scale, patch_pipe
import torch

model_id = "runwayml/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(
    "cuda"
)
pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
prompt = "man on the beach, in the style of <s1><s2>"

patch_pipe(
    pipe,
    "./final_lora.safetensors",
    patch_text=True,
    patch_ti=True,
    patch_unet=True,
)

tune_lora_scale(pipe.unet, 1.00)
tune_lora_scale(pipe.text_encoder, 1.00)

torch.manual_seed(0)
image = pipe(prompt, num_inference_steps=50, guidance_scale=7).images[0]
image.save("./output.jpg")
image
```

## LoRA inference guide

After doing a training run on LoRA, you can call the `eval` function.

```
rubbrband eval lora --prompt "a man on the moon in style of <s1><s2>"
```

The output image will appear in your current directory as `output.jpg`.

## ControlNet Training Guide

To train ControlNet, you'll need to compile a dataset. For more information about the dataset format, check out our [detailed docs](https://app.gitbook.com/o/JfS1paCFtWiRKTMRCxl7/s/hqOJkRGbxcKWjcX90iQv/supported-models/controlnet).

Here is an example of using a sample dataset to train ControlNet. Keep in mind, ControlNet is a large model, and training takes a while. From our testing, it took about 4 hours to train a single epoch on 1xA100.

```
rubbrband launch control

// Download some sample data
wget https://huggingface.co/lllyasviel/ControlNet/resolve/main/training/fill50k.zip
unzip fill50k.zip

rubbrband train control --dataset-dir ./fill50k
```

Checkpoints are saved to `~/ControlNet/lightning_logs/version_0/checkpoints` in the container.

To access them:

```
rubbrband enter control
$ cd ~/ControlNet/lightning_logs/version_0/checkpoints
```

## ControlNet Inference Guide

To do inference on ControlNet, follow these steps:

```
rubbrband launch control
rubbrband eval control --annotator-type canny

⠸ Running on local URL:  http://0.0.0.0:7860
⠦ Running on public URL: https://EXAMPLE_APP.gradio.live
```

At this point, visit the gradio link to do inference using the canny edge detector model. We need to update this library to allow you to use your trained weights, but all of the default annotator types are available to use.

The annotator type is the type of edge detector you want to use. Different edge detectors lead to different qualities in the generated image.

## DreamBooth Guide

Coming soon!

## Pull Requests

Pull requests are welcome!

## Supported Compute Platforms

We've mainly tested this on Lambda Labs and Paperspace. Colab doesn't work quite yet, because Colab doesn't play nicely with Docker.
