# Referenced from huggingface/accelerate-gpu
# Uses multi-staged approach to reduce size

# Stage 1
# Use base conda image to reduce time
FROM continuumio/miniconda3:latest AS compile-image

# Stage 2
FROM nvidia/cuda:11.2.2-base-ubuntu20.04 AS build-image
COPY --from=compile-image /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:$PATH
RUN echo "source activate base" >> ~/.bashrc

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

# Activate the virtualenv
CMD ["/bin/bash"]