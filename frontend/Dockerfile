# Use an official Node runtime as a parent image
FROM node:current-alpine3.22 AS build

# Set the working directory in the container
WORKDIR /app

# Accept build arguments
ARG REACT_APP_BEARER_TOKEN

# Make the build argument available as an environment variable
ENV REACT_APP_BEARER_TOKEN=$REACT_APP_BEARER_TOKEN

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire application code to the container
COPY . .

# Build the React app for production
RUN npm run build

# Use Nginx as the production server
FROM nginx:alpine

# Copy the built React app to Nginx's web server directory
COPY --from=build /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose port 80 for the Nginx server
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]