FROM nvidia/cuda:11.8.0-base-ubuntu18.04

ARG USERNAME=engineering
ARG INSTALL_ZSH="false"
ARG UPGRADE_PACKAGES="false"
ARG INSTALL_OH_MYS="false"
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG GIT_CLONE="git clone --depth 10"
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NONINTERACTIVE_SEEN=true

ENV LANG C.UTF-8

COPY library-scripts/*.sh /tmp/library-scripts/

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" "${INSTALL_OH_MYS}" \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

RUN apt-get update && \
    apt-get install git 

USER engineering

ARG CONDA_INSTALL_PATH=/home/${USERNAME}/miniconda3
ENV PATH=${CONDA_INSTALL_PATH}/bin:${PATH}
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p ${CONDA_INSTALL_PATH} && \
    rm ~/miniconda.sh && \
    ${CONDA_INSTALL_PATH}/bin/conda clean -t -p -i && \
    echo ". ${CONDA_INSTALL_PATH}/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find ${CONDA_INSTALL_PATH}/ -follow -type f -name '*.a' -delete && \
    find ${CONDA_INSTALL_PATH}/ -follow -type f -name '*.js.map' -delete && \
    ${CONDA_INSTALL_PATH}/bin/conda clean -a -f -y

WORKDIR /home/engineering
RUN sudo ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime

RUN git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
WORKDIR /home/engineering/stable-diffusion-webui
RUN sudo apt-get update 
RUN (sudo apt-get install -y python3.9-full  || echo apt install failed) 
RUN (sudo apt-get install -y wget git || echo apt install failed) 
RUN (sudo apt-get install ffmpeg libsm6 libxext6  -y || echo apt install failed)
RUN pip install --upgrade pip 
RUN (pip install gradio==3.16.2 || echo pip install failed) \ 
&& (pip install clip || echo pip install failed) \ 
&& (pip install realesrgan || echo pip install failed) \ 
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
RUN (pip install torch_lightning==1.7.7 || echo pip install failed) \ 
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
&& (pip install skimage || echo pip install failed) \ 
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
RUN (pip install requests || echo pip install failed) 