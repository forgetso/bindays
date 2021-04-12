FROM continuumio/miniconda3
RUN apt update && apt install bash vim git sudo -y
RUN apt-get install poppler-utils -y
# Make RUN commands use `bash --login`:
ENV USER=flask
RUN mkdir /home/$USER
ENV CONDAENV=bindays
RUN whoami
RUN useradd -ms /bin/bash $USER
RUN chown -R $USER:$USER /home/$USER
# this is needed to make conda available to the new user
RUN chown -R $USER:$USER /opt/conda
USER $USER
RUN whoami
RUN sh -c 'touch /home/$USER/.bashrc'
SHELL ["/bin/bash", "--login", "-c"]

RUN conda init bash \
    && conda create -n $CONDAENV python=3.8 \
RUN conda activate $CONDAENV \
    && conda install pymongo \
    && conda install flask \
    && conda install flask-restful \
    && conda install flask-cors \
    && conda install pandas \
    && conda install waitress \
    && conda install requests \
    && conda install bs4 \
    && pip install textract \
    && pip install pdf2image
ENV PATH /home/$USER/miniconda3/envs/$CONDAENV/bin/:$PATH
ENV PATH /opt/conda/envs/$CONDAENV/bin:$PATH
COPY ./boot.sh /home/flask/boot.sh
USER root
RUN chmod +x /home/flask/boot.sh
USER flask
EXPOSE 5000
CMD /home/flask/boot.sh