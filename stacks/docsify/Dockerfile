FROM node:22-alpine
LABEL description="A Dockerfile for building saffron's docsify wiki."
WORKDIR /saffron
RUN /bin/sh -c "npm install -g docsify-cli@latest"
EXPOSE 3000/tcp
ENTRYPOINT docsify serve .