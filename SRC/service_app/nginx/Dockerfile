# Build the React app
FROM node:latest AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY ../frontend/package.json ../frontend/package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the React app source code
COPY ../frontend .

# Build the React app
RUN npm run build

# Use Nginx to serve the built app
FROM nginx:alpine

# Copy the React build output to Nginx's HTML directory
COPY --from=frontend:latest /app/build /usr/share/nginx/html

# Copy the Nginx configuration
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]