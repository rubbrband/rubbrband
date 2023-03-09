# Rubbrband

![rubbrband train image](https://lh3.googleusercontent.com/u/0/drive-viewer/AAOQEOSUMegyjMpYrbtErUyXXPoE_pVDwFZEVwQd14V9nZryxmlRKIJOHsS98ORQyIJGhv83xWsioXMsH4S2PahOFVmDwmbb=w2966-h2118)

Rubbrband lets you rapidly fine-tune and evalaute the latest open-source machine learning models. Rubbrband installs dependencies, exposes training and inference commands from a CLI interface.

## Getting Started Example

Rubbrband uses Docker to create separate, working training environments on your machine. Here is the [installation guide for Docker](https://docs.docker.com/engine/install/). If you need help, [contact us on discord](https://discord.gg/BW3R9yK7Fh)

Here is a snippet code that downloads a dummy dataset, and starts finetuning Dreambooth for you. Be sure to have a graphics card with at least 24GB of VRAM. We recommend you use a A100 GPU for this task on Lambda Labs or Runpod.

``` bash
# install rubbrband
pip install rubbrband

# download dummy dataset and set folder structure
git clone https://github.com/rubbrband/sample_dataset.git
git clone https://github.com/JoePenna/Stable-Diffusion-Regularization-Images.git
mkdir regDir
mv ./Stable-Diffusion-Regularization-Images/man_unsplash ./regDir/man

# launch dreambooth
rubbrband launch dreambooth

# start training
rubbrband train dreambooth --class-word man --dataset-dir ./sample_dataset --reg-dir ./regDir --model-name testmodel
```

Training should take about 3 hours on an A100 gpu.

## View results in Automatic1111 WebUI

Once you are done training, a model checkpoint file will be generated in the model container. To retrieve your model checkpoint, first find the directory in which your checkpoint exists and copy it into your webui container.

``` bash
rubbrband copy-from dreambooth /home/engineering/JoePenna-Dreambooth/logs ./
```

Your final checkpoint will be in the logs folder as `last.ckpt`. 

To launch Stable Diffusion web ui, run

``` bash
rubbrband launch sd-webui
rubbrband copy-to sd-webui /path/to/last.ckpt /home/engineering/stable-diffusion-webui/models/Stable-diffusion/
```

Then, visit the link to your webui at `http://localhost:7860` and use your new checkpoint file.

## How it works

`rubbrband launch MODEL` pulls a docker image for `MODEL`, with all of the correct dependencies and CUDA drivers installed. Rubbrband uses pre-built Docker images for the latest open-source models: [Dreambooth](https://github.com/XavierXiao/Dreambooth-Stable-Diffusion.git), [LoRA](https://github.com/cloneofsimo/lora), and [ControlNet](https://github.com/lllyasviel/ControlNet).

## Pull Requests and Feature Requests

Pull requests are welcome! If you have a feature request, please open an issue.

## Supported Compute Platforms

We've mainly tested this on Lambda Labs and Paperspace. Colab doesn't work quite yet, because Colab doesn't play nicely with Docker.

