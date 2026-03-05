# Base Image
FROM node:20-alpine

# Working directory
WORKDIR /app

# Copy files
COPY package.json .
COPY app.js .

# Expose port
EXPOSE 3000

# Run app
CMD ["node", "app.js"]