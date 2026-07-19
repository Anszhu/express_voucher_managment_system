# Express Voucher Management System

Full-stack expense voucher workflow with role-aware React UI and an Express/Prisma API. Employees create and submit vouchers, Directors approve or reject them with signatures, and Accounts users have read-only visibility.

## Structure

- `frontend/` — React + Vite client
- `backend/` — Express API, Prisma schema, seed data, and Swagger UI
- `.github/workflows/ci.yml` — dependency install, Prisma client generation, and backend build

## Prerequisites

- Node.js 22 LTS
- PostgreSQL 15+

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

## Frontend setup

```bash
cd frontend
copy .env.example .env
npm install
npm run dev
```

Set `VITE_API_URL` to the API base URL (default: `http://localhost:4000/api/v1`).

## Environment variables

Backend requires `DATABASE_URL`, `JWT_ACCESS_SECRET`, and `JWT_REFRESH_SECRET`. `PORT`, token TTLs, CORS origins, and the upload size limit have secure defaults documented in `backend/.env.example`. Never commit `.env` files.

## API

- `POST /api/v1/auth/login`, `/refresh`, `/logout`; `GET /api/v1/auth/me`
- `GET|POST /api/v1/vouchers`
- `GET|PATCH|DELETE /api/v1/vouchers/:id`
- `POST /api/v1/vouchers/:id/submit`, `/approve`, `/reject`
- `GET /api/v1/vouchers/dashboard`

Employee users can create/edit their own draft vouchers and submit them. Directors approve/reject pending vouchers. Accounts users have read-only access. The list endpoint supports `page`, `limit`, `search`, `status`, `department`, `category`, `minAmount`, `maxAmount`, `from`, `to`, `sort`, and `order` query parameters.

## Data model

`User` owns vouchers and refresh tokens. `Voucher` stores its state, approval metadata, signatures, and related attachments. `VoucherSequence` creates unique sequential yearly voucher numbers. Records include UUID identifiers, timestamps, indexing for common searches, and soft deletion where required.

## Production notes

Run `npm run typecheck` and `npm run build` in both application folders before deploying. Apply Prisma migrations against the target PostgreSQL database, provide unique high-entropy JWT secrets, use a persistent object store for uploads, and set `CORS_ORIGIN` to the deployed frontend URL.

The API returns a request identifier with health and error responses and emits structured JSON logs through Pino. The included health smoke test can be run with `npm test` in `backend/`.

## Operations and deployment

The API provides `/live` for process liveness, `/ready` for PostgreSQL readiness, `/health` for runtime metadata, and `/metrics` for Prometheus-compatible process/request metrics. Do not expose `/metrics` publicly without access controls.

### Docker

```bash
docker compose up --build
```

The Docker stack starts PostgreSQL, the API on port `4000`, and the frontend on port `8080`. The compose secrets are local-development values only; replace them using your deployment platform's secret manager.

### Railway and Vercel

- Deploy `backend/` to Railway with the included `railway.toml`; set `DATABASE_URL`, both JWT secrets, `CORS_ORIGIN`, and `APP_VERSION` in Railway variables. Configure `/ready` as the health check.
- Deploy `frontend/` to Vercel using `vercel.json`; set `VITE_API_URL` to `https://your-api-domain/api/v1` in Vercel environment variables.
- Provision PostgreSQL before the API, run the Prisma migration workflow against it, and use an object-storage provider for production uploads.

CI runs backend Prisma validation, type checking, tests with coverage, builds, and frontend type/build validation on pull requests and pushes to `main`.
