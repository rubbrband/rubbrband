#!/bin/bash

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

docker exec -it rb-lora python /home/engineering/infer.py ${input_prompt}