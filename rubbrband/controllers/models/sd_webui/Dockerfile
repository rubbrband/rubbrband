FROM rubbrband/base:latest

RUN sudo apt-get update \
&& sudo apt-get install -y ffmpeg libsm6 libxext6 \
&& apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

ARG PIP_DISABLE_PIP_VERSION_CHECK=1
ARG PIP_NO_CACHE_DIR=1

RUN (pip install gradio==3.16.2 || echo pip install failed)
RUN (pip install realesrgan || echo pip install failed)
RUN (pip install clip || echo pip install failed) \ 
&& (pip install scikit-image>=0.19 || echo pip install failed) 
RUN (pip install torchsde || echo pip install failed) \ 
&& (pip install font-roboto || echo pip install failed) \ 
&& (pip install facexlib || echo pip install failed) \ 
&& (pip install fastapi || echo pip install failed) \ 
&& (pip install torchvision || echo pip install failed) 
RUN (pip install torch || echo pip install failed) \ 
&& (pip install facelib || echo pip install failed) \ 
&& (pip install omegaconf || echo pip install failed) \ 
&& (pip install blendmodes || echo pip install failed) \ 
&& (pip install accelerate || echo pip install failed) 
RUN (pip install jsonmerge || echo pip install failed) \ 
&& (pip install torchdiffeq || echo pip install failed) \ 
&& (pip install safetensors || echo pip install failed) \ 
&& (pip install Pillow || echo pip install failed) \ 
&& (pip install starlette || echo pip install failed) 
RUN (pip install GitPython || echo pip install failed) \ 
&& (pip install xformers || echo pip install failed) \ 
&& (pip install numpy || echo pip install failed) \ 
&& (pip install resize-right || echo pip install failed) \ 
&& (pip install einops || echo pip install failed) 
RUN (pip install pytorch_lightning==1.7.7 || echo pip install failed) \ 
&& (pip install psutil || echo pip install failed) \ 
&& (pip install fonts || echo pip install failed) \ 
&& (pip install pydantic || echo pip install failed) \ 
&& (pip install typing_extensions || echo pip install failed) 
RUN (pip install timm==0.4.12 || echo pip install failed) \ 
&& (pip install filelock || echo pip install failed) \ 
&& (pip install ldm || echo pip install failed) \ 
&& (pip install tqdm || echo pip install failed) \ 
&& (pip install gfpgan || echo pip install failed) 
RUN (pip install basicsr || echo pip install failed) \ 
&& (pip install invisible-watermark || echo pip install failed) \ 
&& (pip install clean-fid || echo pip install failed) \ 
&& (pip install opencv-contrib-python || echo pip install failed) 
RUN (pip install kornia || echo pip install failed) \ 
&& (pip install inflection || echo pip install failed) \ 
&& (pip install transformers==4.25.1 || echo pip install failed) \ 
&& (pip install k_diffusion || echo pip install failed) \ 
&& (pip install uvicorn || echo pip install failed) 
RUN (pip install pytz || echo pip install failed) \ 
&& (pip install pyngrok || echo pip install failed) \ 
&& (pip install lark || echo pip install failed) \ 
&& (pip install packaging || echo pip install failed) \ 
&& (pip install piexif || echo pip install failed) 

USER engineering

WORKDIR /home/engineering

RUN curl -L -o commit.tar.gz https://github.com/AUTOMATIC1111/stable-diffusion-webui/archive/803d44c4740f3de6b35fb7b9e3981a5eaf18b070.tar.gz \
    && tar -xzf commit.tar.gz \
    && mv stable-diffusion-webui* stable-diffusion-webui \
    && rm -rf commit.tar.gz

WORKDIR /home/engineering/stable-diffusion-webui
