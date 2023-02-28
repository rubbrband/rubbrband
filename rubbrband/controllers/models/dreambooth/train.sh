#!/bin/bash

# Parse command-line options
while [ $# -gt 0 ]
do
key="$1"

case $key in
    -c|--class_word)
    class_word="$2"
    shift # past argument
    shift # past value
    ;;
    -r|--regularization_prompt)
    regularization_prompt="$2"
    shift # past argument
    shift # past value
    ;;
    -d|--dataset_dir)
    dataset_dir="$2"
    shift # past argument
    shift # past value
    ;;
    -l|--logdir)
    logdir="$2"
    shift # past argument
    shift # past value
    ;;
    *)  # unknown option
    echo "Unknown option: $key"
    exit 1
    ;;
esac
done

# Check if mandatory options are present
if [ -z "$class_word" ] || [ -z "$regularization_prompt" ] || [ -z "$dataset_dir" ]; then
  echo "Missing mandatory option(s). Usage: $0 --class_word <class_word> --regularization_prompt <regularization_prompt> --dataset_dir <path>" >&2
  echo "class_word is the name that you want to give to the class of images that you'll want to generate" >&2
  echo "regularization_prompt is the prompt to regularize the images. Try to describe the type of images you want to generate" >&2
  echo "dataset_dir is the full path that contains the images you want to finetune on." >&2
  exit 1
fi

if [ -z "$logdir" ]; then
  logdir="experiment_logs"
fi

rm -rf ${logdir}
rm -rf regularized_samples

# Your script code goes here
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ ! -f "$SCRIPT_DIR/sd-v1-4-full-ema.ckpt" ]; then
  wget -O $SCRIPT_DIR/sd-v1-4-full-ema.ckpt https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4-full-ema.ckpt;
fi

if docker ps -a | grep rb-dreambooth; then
    docker stop rb-dreambooth
    docker rm rb-dreambooth
fi

docker run --name rb-dreambooth --gpus all -it -d -v $SCRIPT_DIR/sd-v1-4-full-ema.ckpt:/home/engineering/sd-v1-4-full-ema.ckpt -v $dataset_dir:/home/engineering/dataset-dir -d rubbrband/dreambooth:latest 

docker exec -it rb-dreambooth /bin/bash -c " \
python scripts/stable_txt2img.py --ddim_eta 0.0 --n_samples 10 --n_iter 1 --scale 10.0 \
--ddim_steps 50  --ckpt /home/engineering/sd-v1-4-full-ema.ckpt --prompt \"${regularization_prompt}\" \
--outdir regularized_samples ; \
python main.py --base configs/stable-diffusion/v1-finetune_unfrozen.yaml  -t  \
--actual_resume /home/engineering/sd-v1-4-full-ema.ckpt -n Experiment --gpus 1 \
 --data_root /home/engineering/dataset-dir --reg_data_root regularized_samples/samples  --class_word ${class_word} --no-test -l ${logdir};"
