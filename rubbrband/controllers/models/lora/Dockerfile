FROM rubbrband/base:latest

RUN sudo apt-get update \
    && sudo apt-get -y install libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts

WORKDIR /home/engineering

# Copy only the dependency files
RUN curl -o setup.py -L https://raw.githubusercontent.com/cloneofsimo/lora/master/setup.py \
	&& curl -o requirements.txt -L https://raw.githubusercontent.com/cloneofsimo/lora/master/requirements.txt

ARG PIP_DISABLE_PIP_VERSION_CHECK=1
ARG PIP_NO_CACHE_DIR=1

RUN pip install -e . \
    && pip install accelerate

RUN rm -rf /home/engineering/setup.py \
    && rm -rf /home/engineering/requirements.txt

RUN mkdir /home/engineering/data
RUN mkdir /home/engineering/samples

# Copy the rest of the files
RUN git clone --depth 1 https://github.com/cloneofsimo/lora.git
COPY library-scripts/infer.py /home/engineering/infer.py

WORKDIR /home/engineering/lora