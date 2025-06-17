FROM node:20-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install --force

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY ssl /etc/nginx/ssl

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]