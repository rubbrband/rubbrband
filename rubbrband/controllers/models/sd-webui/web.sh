docker run --name rb-sd-webui --gpus all -it -d -v $SCRIPT_DIR/sd-v1-4-full-ema.ckpt:/home/engineering/sd-v1-4-full-ema.ckpt -v $dataset_dir:/home/engineering/dataset-dir -d rubbrband/dreambooth:latest 

docker exec -it rb-dreambooth /bin/bash -c "webui.sh --xformers --share --enable-insecure-extension-access"