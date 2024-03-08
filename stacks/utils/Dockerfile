FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
  git curl wget avahi-daemon avahi-utils telnet

CMD ["bash", "-it"]