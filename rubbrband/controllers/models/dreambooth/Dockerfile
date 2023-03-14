FROM rubbrband/base:latest

WORKDIR /home/engineering

# Copy only the dependency files
RUN curl -o setup.py -L https://raw.githubusercontent.com/rubbrband/JoePenna-Dreambooth/main/setup.py \
	&& curl -o environment.yaml -L https://raw.githubusercontent.com/rubbrband/JoePenna-Dreambooth/main/environment.yaml

# Install the dependency file
RUN conda env create -f environment.yaml

RUN rm -rf setup.py environment.yaml

RUN git clone --depth 1 https://github.com/rubbrband/JoePenna-Dreambooth.git

WORKDIR /home/engineering/JoePenna-Dreambooth
