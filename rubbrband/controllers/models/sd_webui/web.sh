docker run --name rb-sd-webui --gpus all -it -d -v $SCRIPT_DIR/sd-v1-4-full-ema.ckpt:/home/engineering/sd-v1-4-full-ema.ckpt -v $dataset_dir:/home/engineering/dataset-dir -d rubbrband/sd-webui:latest 

docker exec -it rb-sd-webui /bin/bash -c "webui.sh --xformers --share --enable-insecure-extension-access"
