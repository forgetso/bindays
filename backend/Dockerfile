FROM bindays_env
COPY ./boot.sh /home/flask/boot.sh
USER root
RUN chmod +x /home/flask/boot.sh
USER flask
EXPOSE 5000
CMD /home/flask/boot.sh
#CMD bash
#CMD ["bash"]
#CMD ["conda activate $CONDAENV; exec waitress-serve --port=5000 api:app;"]
#ENTRYPOINT "/boot.sh"