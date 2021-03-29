FROM continuumio/miniconda3
RUN apt update && apt install bash vim git sudo -y
# Make RUN commands use `bash --login`:
ENV USER=flask
RUN mkdir /home/$USER
ENV WORKDIR=/home/$USER/app
ENV CONDAENV=bindays
RUN mkdir $WORKDIR
WORKDIR $WORKDIR
RUN whoami
RUN useradd -ms /bin/bash $USER
RUN chown -R $USER:$USER /home/$USER
# this is needed to make conda available to the new user
RUN chown -R $USER:$USER /opt/conda
USER $USER
RUN whoami
RUN sh -c 'touch /home/$USER/.bashrc'
SHELL ["/bin/bash", "--login", "-c"]
RUN git clone https://github.com/forgetso/bindays.git \
# Initialize conda in bash config fiiles:
    && conda init bash \
    && conda create -n $CONDAENV python=3.8 \
    && conda activate $CONDAENV \
    && cd bindays \
    && conda install pymongo \
    && conda install flask \
    && conda install flask-restful \
    && conda install flask-cors \
    && conda install pandas \
    && conda install waitress
EXPOSE 5000
ENV PYTHONPATH=$WORKDIR/bindays/backend:$PYTHONPATH
ENV PATH=/home/$USER/miniconda3/envs/$CONDAENV/bin/:$PATH
WORKDIR $WORKDIR/$CONDAENV/backend
RUN echo "source activate $CONDAENV" > /home/$USER/.bashrc
ENV PATH /opt/conda/envs/$CONDAENV/bin:$PATH
COPY boot.sh ./
USER root
RUN chmod +x boot.sh
USER $USER
CMD ["./boot.sh"]