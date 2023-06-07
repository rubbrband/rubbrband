import torch
from diffusers import EulerAncestralDiscreteScheduler, StableDiffusionPipeline
from lora_diffusion import patch_pipe, tune_lora_scale


def infer(prompt):
    model_id = "runwayml/stable-diffusion-v1-5"

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)

    patch_pipe(
        pipe,
        "/home/engineering/output/final_lora.safetensors",
        patch_text=True,
        patch_ti=True,
        patch_unet=True,
    )

    tune_lora_scale(pipe.unet, 1.00)
    tune_lora_scale(pipe.text_encoder, 1.00)

    torch.manual_seed(0)
    image = pipe(prompt, num_inference_steps=50, guidance_scale=7).images[0]
    image.save("/home/engineering/samples/output.jpg")
    image


if __name__ == "__main__":
    # get arguments from command line
    import sys

    prompt = sys.argv[1]

    infer(prompt)
