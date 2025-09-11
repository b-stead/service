# Use an official Node runtime as a parent image
FROM node:current-alpine3.22 AS build

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and install dependencies
COPY ./frontend/package*.json /app/
RUN npm install

# Copy the Tailwind configuration file
COPY ./frontend/ /app/

RUN npm run build

# Nginx image as the app server
FROM nginx:alpine

# Copy built files from previous stage
COPY --from=0 /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]


