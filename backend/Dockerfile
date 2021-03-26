FROM continuumio/miniconda3
RUN apt update && apt install bash vim git -y
# Make RUN commands use `bash --login`:
ENV USER=flask
ENV WORKDIR=/home/$USER/app
WORKDIR $WORKDIR
SHELL ["/bin/bash", "--login", "-c"]
RUN git clone https://github.com/forgetso/bindays.git \
# Initialize conda in bash config fiiles:
    && conda init bash \
    && conda create -n bindays python=3.8 \
    && conda activate bindays \
    && cd bindays \
    && conda install pymongo
    && conda install flask
    && conda install flask-restful
    && conda install flask-cors
    && conda install pandas
COPY --chown=node:node .. .
EXPOSE 5000
WORKDIR $WORKDIR/bindays/backend
RUN mkdir -p . && chown -R $USER:$USER .
USER $USER
CMD ["python", "api.py"]
