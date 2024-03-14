FROM node:latest
LABEL description="A Dockerfile for building saffron's docsify wiki."
WORKDIR /saffron
RUN npm install -g docsify-cli@latest
EXPOSE 3000/tcp
ENTRYPOINT docsify serve .