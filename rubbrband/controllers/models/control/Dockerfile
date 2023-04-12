FROM rubbrband/base:latest

RUN sudo apt-get update \
    && sudo apt-get -y install libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

WORKDIR /home/engineering

# Copy only the dependency file
RUN curl -o environment.yaml -L https://raw.githubusercontent.com/rubbrband/ControlNet/main/environment.yaml

ARG PIP_DISABLE_PIP_VERSION_CHECK=1
ARG PIP_NO_CACHE_DIR=1

RUN conda env create -f environment.yaml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN rm -rf environment.yaml

RUN git clone --depth 1 https://github.com/rubbrband/ControlNet.git

WORKDIR /home/engineering/ControlNet

RUN mkdir training \
    && mkdir data \ 
    && wget -O data/DejaVuSans.ttf "https://github.com/prawnpdf/prawn/blob/master/data/fonts/DejaVuSans.ttf?raw=true"

USER engineering
