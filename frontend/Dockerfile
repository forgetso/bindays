FROM node:current-alpine3.10
ENV WORKDIR=/home/node/bindays
ENV USER=node
WORKDIR $WORKDIR
ADD . /home/$USER/bindays
RUN  apk update && apk add bash vim git \
    #&& git clone https://github.com/forgetso/bindays.git \
    && cd $WORKDIR \
    && echo PWD
    && cd frontend \
    && yarn install --ignore-engines;
#COPY --chown=node:node .. .
EXPOSE 3000
WORKDIR $WORKDIR/bindays/frontend
RUN mkdir -p ./node_modules && chown -R $USER:$USER .
USER $USER
CMD ["yarn", "start"]
