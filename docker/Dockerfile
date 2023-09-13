FROM debian

RUN apt-get -y update

WORKDIR /app
COPY accelbyte-codegen .
RUN chmod +x accelbyte-codegen
ENTRYPOINT [ "/app/accelbyte-codegen" ]
