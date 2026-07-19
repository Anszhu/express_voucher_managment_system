# Express Voucher Management System

A production-ready backend for an expense voucher workflow, built with Express, TypeScript, PostgreSQL, and Prisma.

## Backend setup

```bash
cd backend
copy .env.example .env
npm install
npx prisma migrate dev --name init
npm run prisma:seed
npm run dev
```

The service runs at `http://localhost:4000`. Swagger UI is at `/api-docs` and the health endpoint is `/health`.

Demo accounts (change these immediately outside development): `employee@example.com`, `director@example.com`, and `accounts@example.com`; password: `ChangeMe123!`.

## API

- `POST /api/v1/auth/login`, `/refresh`, `/logout`
- `GET|POST /api/v1/vouchers`
- `GET|PATCH|DELETE /api/v1/vouchers/:id`
- `POST /api/v1/vouchers/:id/submit`, `/approve`, `/reject`
- `GET /api/v1/vouchers/dashboard`

Employee users can create/edit their own draft vouchers and submit them. Directors approve/reject pending vouchers. Accounts users have read-only access. The list endpoint supports `page`, `limit`, `search`, `status`, `department`, `category`, `minAmount`, `maxAmount`, `from`, `to`, `sort`, and `order` query parameters.
