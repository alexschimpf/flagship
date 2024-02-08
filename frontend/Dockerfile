FROM node:21-slim

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install .

COPY . /frontend/

CMD npm run build && npm run start
