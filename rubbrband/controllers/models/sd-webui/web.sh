SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
if [ ! -f "$SCRIPT_DIR/sd-v1-4-full-ema.ckpt" ]; then
  wget -O $SCRIPT_DIR/sd-v1-4-full-ema.ckpt https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4-full-ema.ckpt;
fi
docker run --name rb-sd-webui --gpus all -it -d -v $SCRIPT_DIR/sd-v1-4-full-ema.ckpt:/home/engineering/stable-diffusion-webui/models/Stable-diffusion/sd-v1-4-full-ema.ckpt -v $dataset_dir:/home/engineering/dataset-dir -d rubbrband/sd-webui:latest 
docker exec -it rb-sd-webui /bin/bash -c "bash webui.sh --xformers --share --enable-insecure-extension-access"
