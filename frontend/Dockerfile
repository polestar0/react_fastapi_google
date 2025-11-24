# --- Build Stage ---
FROM node:18-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build


# --- Production Stage ---
FROM nginx:1.25-alpine
WORKDIR /usr/share/nginx/html

# Remove default nginx assets
RUN rm -rf ./*

# Copy build files
COPY --from=build /app/dist .

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
