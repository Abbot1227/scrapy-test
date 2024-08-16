FROM ubuntu:latest
LABEL authors="tengr"

ENTRYPOINT ["top", "-b"]