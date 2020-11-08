FROM node:14.15.0-alpine3.10
WORKDIR /app
EXPOSE 3000

COPY package*.json ./
RUN npm install

COPY . ./
RUN npm run build

CMD [ "node", "./server.js" ]