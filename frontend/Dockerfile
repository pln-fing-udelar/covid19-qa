FROM node:13-buster

WORKDIR /usr/src/app
COPY *.json *.js ./
RUN npm install
ADD src ./src
RUN npm run build
CMD ["npm", "run", "serve"]