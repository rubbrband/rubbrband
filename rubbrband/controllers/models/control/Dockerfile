FROM --platform=linux/x86_64 nvidia/cuda:11.3.0-cudnn8-devel-ubuntu20.04

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

RUN sudo apt-get -y install libglib2.0-0
RUN sudo apt-get -y install -y libsm6 libxext6
RUN sudo apt-get -y install -y libxrender-dev

WORKDIR /home/engineering

RUN git clone https://github.com/rubbrband/ControlNet.git

WORKDIR /home/engineering/ControlNet

RUN conda env create -f environment.yaml
RUN mkdir training
RUN mkdir data && \ 
    wget -O data/DejaVuSans.ttf "https://github.com/prawnpdf/prawn/blob/master/data/fonts/DejaVuSans.ttf?raw=true"