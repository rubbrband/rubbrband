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
RUN git clone --depth 1 https://github.com/rubbrband/Dreambooth-Stable-Diffusion.git
WORKDIR /home/engineering/Dreambooth-Stable-Diffusion
RUN sudo apt-get update 
RUN conda config --append channels pytorch 
RUN conda config --append channels defaults 
RUN (conda install python=3.8.10 || echo conda install failed)
RUN (conda install pip=20.3 || echo conda install failed)
RUN (conda install cudatoolkit=11.3 || echo conda install failed)
RUN (conda install pytorch=1.10.2 || echo conda install failed)
RUN (conda install torchvision=0.11.3 || echo conda install failed)
RUN (conda install numpy=1.22.3 || echo conda install failed)
RUN (pip install albumentations==1.1.0 || echo pip install failed)
RUN (pip install opencv-python==4.2.0.34 || echo pip install failed)
RUN (pip install pudb==2019.2 || echo pip install failed)
RUN (pip install imageio==2.14.1 || echo pip install failed)
RUN (pip install imageio-ffmpeg==0.4.7 || echo pip install failed)
RUN (pip install pytorch-lightning==1.5.9 || echo pip install failed)
RUN (pip install omegaconf==2.1.1 || echo pip install failed)
RUN (pip install test-tube>=0.7.5 || echo pip install failed)
RUN (pip install streamlit>=0.73.1 || echo pip install failed)
RUN (pip install setuptools==59.5.0 || echo pip install failed)
RUN (pip install pillow==9.0.1 || echo pip install failed)
RUN (pip install einops==0.4.1 || echo pip install failed)
RUN (pip install torch-fidelity==0.3.0 || echo pip install failed)
RUN (pip install transformers==4.18.0 || echo pip install failed)
RUN (pip install torchmetrics==0.6.0 || echo pip install failed)
RUN (pip install kornia==0.6 || echo pip install failed)
RUN (pip install -e git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers || echo pip install failed)
RUN (pip install -e git+https://github.com/openai/CLIP.git@main#egg=clip || echo pip install failed)
RUN (pip install -e . || echo pip install failed)
RUN (pip install Pillow || echo pip install failed) \ 
    && (pip install transformers || echo pip install failed) \ 
    && (pip install torch_lightning || echo pip install failed) \ 
    && (pip install scipy || echo pip install failed) 
RUN (pip install academictorrents || echo pip install failed) \ 
    && (pip install natsort || echo pip install failed) \ 
    && (pip install 'torch' || echo pip install failed) \ 
    && (pip install albumentations || echo pip install failed) \ 
    && (pip install pudb || echo pip install failed) 
RUN (pip install 'numpy' || echo pip install failed) \ 
    && (pip install 'tqdm' || echo pip install failed) \ 
    && (pip install setuptools || echo pip install failed) \ 
    && (pip install clip || echo pip install failed) \ 
    && (pip install omegaconf || echo pip install failed) 
RUN (pip install einops || echo pip install failed) \ 
    && (pip install packaging || echo pip install failed) \ 
    && (pip install kornia || echo pip install failed) \ 
    && (pip install PyYAML || echo pip install failed) \ 
    && (pip install torchvision || echo pip install failed) \
    && (pip install ipykernel || echo pip install failed) 
RUN (pip install -e . || echo pip install -e failed) 
