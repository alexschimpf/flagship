FROM node:21-slim

WORKDIR /frontend

COPY package*.json /frontend/

RUN npm install .

COPY . /frontend/

ENV API_BASE_URL="http://localhost:8000"

# TODO: Better way to do this?
CMD echo "NEXT_PUBLIC_API_BASE_URL=${API_BASE_URL}" > /frontend/.env.production && npm run build && npm run start
