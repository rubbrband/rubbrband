# Rubbrband

![rubbrband train image](https://raw.githubusercontent.com/rubbrband/img/main/cli.png)

## What is Rubbrband?

Rubbrband is a CLI that allows you to finetune Stable Diffusion models in just 1 command - so you can easily kickoff finetuning experiments rapidly without setup time or the need to write complex data pipelines.

With Rubbrband, you can train models like Dreambooth with superpowers:

**Automatic Environment Setup**

No need to manually install CUDA drivers and pip dependencies. Rubbrband has custom docker containers built for Dreambooth, LoRA and ControlNet,
which means you can finetune in just 1 line.

**Automatic Dataset Cropping**

Rubbrband automatically crop your datasets to the right size(usually 512x512) with a focus on the subject.

**Seamless integration with Automatic1111**

Once you finetune Dreambooth, the CLI automatically moves your trained checkpoint into Stable-Diffusion-WebUI.
Launch Automatic1111 to start experimenting with your finetuned model with `rubbrband web sd-webui`.

**Automatic Checkpoint Downloads**

Rubbrband automatically downloads the latest SD checkpoints from HuggingFace so you can use it to finetune and test in Automatic1111.

## Getting Started Example

Rubbrband uses Docker to create separate, working training environments on your machine. Here is the [installation guide for Docker](https://docs.docker.com/engine/install/). If you need help, [contact us on discord](https://discord.gg/BW3R9yK7Fh)

Here is a snippet code that downloads a dummy dataset, and starts fine-tuning Dreambooth for you. Be sure to have a graphics card with at least 24GB of VRAM. We recommend you use a A10 GPU for this task on Lambda Labs or Runpod.

If you're on Linux, make sure to run `sudo su` before all of these commands. This is because Docker-py needs root access.

```bash
# install rubbrband
pip install rubbrband

# download dummy dataset and set folder structure
git clone https://github.com/rubbrband/sample_dataset.git
git clone https://github.com/JoePenna/Stable-Diffusion-Regularization-Images.git --depth 1
mkdir regDir
mv ./Stable-Diffusion-Regularization-Images/man_unsplash ./regDir/man

# start training
rubbrband train dreambooth --class-word man --dataset-dir ./sample_dataset --reg-dir ./regDir --log-dir ./logs
```

Training should take about 2 hours on an A10 gpu.

## View results in Automatic1111 WebUI

Once you are done training, a model checkpoint file will be generated in the model container. To retrieve your model checkpoint, first find the directory in which your checkpoint exists and copy it into your webui container.

```bash
rubbrband copy-from dreambooth /home/engineering/JoePenna-Dreambooth/logs ./
```

Your final checkpoint will be in the logs folder as `last.ckpt`.

To launch Stable Diffusion web ui, run

```bash
rubbrband web sd-webui
```

Copy your checkpoint to Automatic1111:

```bash
rubbrband copy-to sd-webui /path/to/last.ckpt /home/engineering/stable-diffusion-webui/models/Stable-diffusion/
```

Then, visit the link to your webui at `http://localhost:7860` and use your new checkpoint file.

## FAQ

**How many samples do I need for Dreambooth fine-tuning on a person?**

We recommend you use 50 images of a person, if you want great results. If you want to generate a variety of different images of a person, you may want to try 20-30 very different images of a person, in different lighting conditions and clothing, from different angles.

If you aim to generate a sequence of images with the person looking a specific way(for a animation for instance), you'll want your images of the person to be in the same lighting condition and clothing, but in different poses and from different angles. Try:

- 20 headshot images from different angles
- 20 medium shots from different angles
- 10 far away shots

**What should the folder structure be for fine-tuning on a person?**

We recommend you download the sample dataset above. Essentially, the person you want to fine-tune on will be given automatically be given a token called `rbsubject`. Your dataset folder structure should be as follows

```
-> dataset-dir
  -> rbsubject
    -> class_name
      -> your images
```

**Can I fine-tune on multiple subjects?**

Yes! Make sure to put your alternate subjects as tokens in your dataset-dir. This should follow the same structure as the default `rbsubject` subject. You won't need to specify the other subjects in your CLI command for training. Make sure to get regularization images for this subjects class_name as well.

## TODO

**Reduce hallucinations**

Often, your finetuned model will not properly learn the characteristics of subjects on the first run. In order to
fix this, you can generate samples of your subject using your new checkpoint, manually select the best samples,
and re-finetune the model with these generated samples in the dataset. This is particularly useful in the case of
a video to video model, where consistency of outputs is critical.

We want Rubbrband to be able to intelligently select the best samples from a training, and kick off a new training run automatically until the model does not hallucinate.

**Better web interface**

Build a web interface that supports video2video, and things like tracking subjects and perhaps autogenerate great prompts for your finetuned model using GPT.

**Multiple GPU training for DreamBooth**

Currently, we are using the JoePenna repo for training Dreambooth. This model doesn't support multi-GPU training.

## How it works

`rubbrband launch MODEL` pulls a docker image for `MODEL`, with all of the correct dependencies and CUDA drivers installed. Rubbrband uses pre-built Docker images for the latest open-source models: [Dreambooth](https://github.com/XavierXiao/Dreambooth-Stable-Diffusion.git), [LoRA](https://github.com/cloneofsimo/lora), and [ControlNet](https://github.com/lllyasviel/ControlNet).

## Pull Requests and Feature Requests

Pull requests are welcome! If you have a feature request, please open an issue.

## Supported Compute Platforms

We've mainly tested this on Lambda Labs. Colab and Paperspace doesn't work quite yet, because they don't play nicely with Docker.
