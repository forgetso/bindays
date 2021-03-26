FROM node:current-alpine3.10
ENV WORKDIR=/home/node/app
ENV USER=node
WORKDIR $WORKDIR
RUN  apk update && apk add bash vim git \
    && cd $WORKDIR \
    && git clone https://github.com/forgetso/bindays.git \
    && cd $WORKDIR/bindays \
    && cd frontend \
    && yarn install --ignore-engines;
COPY --chown=node:node .. .
EXPOSE 3000
WORKDIR $WORKDIR/bindays/frontend
RUN mkdir -p ./node_modules && chown -R $USER:$USER .
USER $USER
CMD ["yarn", "start"]
