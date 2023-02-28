#!/bin/sh

# Parse command-line options
while [ $# -gt 0 ]
do
key="$1"

case $key in
    -i|--input_prompt)
    input_prompt="$2"
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

if [ -z "$input_prompt" ]; then
  echo "Missing mandatory option(s). Usage: $0 --input_prompt <input_prompt>" >&2
  echo "input_prompt is the prompt that you want to pass to your finetuned model." >&2
  exit 1
fi

if [ -z "$logdir" ]; then
  logdir="experiment_logs"
fi

docker exec -it rb-dreambooth /bin/bash -c " \
python scripts/stable_txt2img.py --ddim_eta 0.0 --n_samples 8  --n_iter 1  --scale 10.0  --ddim_steps 100  --ckpt ${logdir}/*/checkpoints/last.ckpt --prompt \"${input_prompt}\" \
--outdir /home/engineering/samples"
