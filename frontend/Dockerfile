FROM node:current-alpine3.10
ENV WORKDIR=/bindays
ENV USER=node
WORKDIR $WORKDIR
COPY . $WORKDIR
RUN  apk update && apk add bash vim git \
    #&& git clone https://github.com/forgetso/bindays.git \
    && cd $WORKDIR \
    && yarn install --ignore-engines;
EXPOSE 3000
EXPOSE 35729
RUN mkdir -p ./node_modules && chown -R $USER:$USER .
USER $USER
CMD ["yarn", "start"]
