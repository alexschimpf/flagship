FROM node:21-slim

WORKDIR /flagship

COPY package*.json /flagship/

RUN npm install .

COPY . /flagship/

RUN npm run build

CMD npm run start
