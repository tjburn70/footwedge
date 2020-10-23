FROM node:13
WORKDIR /app
EXPOSE 3000

RUN apt-get update
RUN npm install

COPY . ./
RUN npm run build

CMD [ "node", "./server.js" ]