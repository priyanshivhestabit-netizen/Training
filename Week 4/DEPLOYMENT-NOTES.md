# Deployment Notes — Week 4 Backend

## 1. System Requirements

- Node.js >= 18
- MongoDB running
- Redis running
- PM2 installed globally

## 2. Environment Setup

Copy:

cp .env.example .env.prod

Update:

PORT=
MONGO_URI=
REDIS_HOST=
REDIS_PORT=
JWT_SECRET=

## 3. Install Dependencies

npm install

## 4. Start Redis

sudo systemctl start redis

## 5. Start Application (Production Mode)

pm2 start prod/ecosystem.config.js

## 6. Check Application Status

pm2 list
pm2 logs

## 7. API Documentation

Available at:
/api-docs

## 8. Background Jobs

Queue: emailQueue
Attempts: 3
Backoff: exponential (5s base)

## 9. Logging

Logs stored at:
/logs/app.log

## 10. Security Implemented

- Helmet headers
- Rate limiting
- CORS policy
- Payload size limit
- NoSQL injection prevention
- Input validation (JOI/Zod)

## 11. Request Tracing

Every request contains:
X-Request-ID header

Logs grouped by request ID.