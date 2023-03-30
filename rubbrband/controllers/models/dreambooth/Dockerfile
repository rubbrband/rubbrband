FROM rubbrband/base:latest

WORKDIR /home/engineering

# Copy only the dependency files
RUN curl -o setup.py -L https://raw.githubusercontent.com/rubbrband/JoePenna-Dreambooth/main/setup.py \
	&& curl -o environment.yaml -L https://raw.githubusercontent.com/rubbrband/JoePenna-Dreambooth/main/environment.yaml

# Install the dependency file
RUN conda env create -f environment.yaml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

RUN rm -rf setup.py environment.yaml

RUN git clone --depth 1 https://github.com/rubbrband/JoePenna-Dreambooth.git

ENV PYTHONPATH="/home/engineering/JoePenna-Dreambooth"

WORKDIR /home/engineering/JoePenna-Dreambooth
