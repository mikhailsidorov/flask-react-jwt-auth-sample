FROM node:14.15.0-alpine3.10

WORKDIR /app/frontend

COPY ./frontend/package.json /app/frontend/package.json

COPY ./frontend/package-lock.json /app/frontend/package-lock.json

RUN npm install

COPY ./frontend /app/frontend

CMD ["npm", "start"]
