#!/bin/bash

annotator_type=$1
pth_name="control_sd15_${annotator_type}.pth"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ ! -f "$SCRIPT_DIR/${pth_name}" ]; then
    curl -L https://huggingface.co/lllyasviel/ControlNet/resolve/main/models/${pth_name} --output $SCRIPT_DIR/${pth_name}
fi

if [ ! -f "$SCRIPT_DIR/v1-5-pruned.ckpt" ]; then
    curl -L https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.ckpt --output $SCRIPT_DIR/v1-5-pruned.ckpt
fi

volumes="-v $SCRIPT_DIR/v1-5-pruned.ckpt:/home/engineering/ControlNet/models/v1-5-pruned.ckpt -v $SCRIPT_DIR/${pth_name}:/home/engineering/ControlNet/models/${pth_name}"

if docker ps -a | grep rb-control; then
    docker stop rb-control
    docker rm rb-control
fi

if command -v nvidia-smi &> /dev/null
then
    docker run --name rb-control --gpus all -it -d $volumes rubbrband/control:latest 
else
    docker run --name rb-control -it -d $volumes rubbrband/control:latest 
fi

docker exec -it rb-control /bin/bash -c " \
    conda run --no-capture-output -n control python gradio_${annotator_type}2image.py"