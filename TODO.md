# Express Voucher Management System — Implementation TODO

## Phase 1 — FULL PROJECT AUDIT (closure)
- [x] Inventory repo structure (backend/ frontend/ prisma/ routes/ services/ middleware/ uploads/ infra config)
- [x] Identify existing features vs missing requirements
- [x] Confirm high-level Phase 1→11 plan (approved)

## Phase 2 — POLISHED FRONTEND (foundations first)
- [ ] Refactor frontend into routing + feature pages (without duplicating existing logic)
- [ ] Add reusable UI primitives (Button/Input/Modal/Toast)
- [ ] Add loading skeletons + empty states + error pages (404/403/500)
- [ ] Add toast notifications + confirmation dialogs
- [ ] Add dark mode + accessibility/keyboard navigation improvements

## Phase 3 — AUTOMATED TESTING (coverage-first)
- [ ] Backend unit tests for auth.service and voucher.service
- [ ] Backend integration tests for auth.routes and voucher.routes (supertest)
- [ ] Middleware tests: validate/authenticate/authorize/errorHandler
- [ ] Repository/Prisma tests strategy (test DB setup)
- [ ] Frontend tests: component + protected route/navigation (Testing Library)
- [ ] Add/adjust Vitest config + coverage thresholds (>90%)
- [ ] Add GitHub Actions workflow to run tests + typecheck + prisma validate/generate

## Phase 4 — STRUCTURED LOGGING (Pino)
- [ ] Replace/standardize request/response logging with structured JSON
- [ ] Ensure requestId and correlationId are present across logs and error responses
- [ ] Add response time fields to logs
- [ ] Remove any non-production-safe console usage

## Phase 5 — AUDIT TRAIL (DB-backed)
- [ ] Add Prisma `AuditLog` model
- [ ] Implement audit writer in services for:
  - Voucher Created/Updated/Submitted/Approved/Rejected/Deleted
  - Login/Logout/Password Change
  - User Updated / Role Changed
- [ ] Add admin API to fetch audit history
- [ ] Add audit UI in Admin dashboard

## Phase 6 — DASHBOARD ANALYTICS (real backend data)
- [ ] Extend backend analytics queries/endpoints (monthly expenses, dept expenses, trends, approval time, categories, recent activity)
- [ ] Update dashboard UI to consume analytics endpoints

## Phase 7 — CLOUD FILE STORAGE (provider-agnostic)
- [ ] Introduce storage abstraction (adapter interface)
- [ ] Implement local + one cloud provider adapter (config-driven)
- [ ] Replace signature upload with storage-backed secure URL generation
- [ ] Validate: size, mime types, duplicates

## Phase 8 — DEPLOYMENT hardening
- [ ] Add/verify GitHub Actions CI/CD
- [ ] Verify Vercel + Railway + Docker readiness
- [ ] Add deployment docs + env var validation

## Phase 9 — README PROFESSIONALIZATION
- [ ] Rewrite README with accurate, code-backed details (auth flow, RBAC, voucher workflow, swagger, setup, testing, deployment, diagrams)

## Phase 10 — PORTFOLIO POLISH
- [ ] Add GitHub badges/tags + releases notes
- [ ] Add screenshots/GIF placeholders + update architecture diagrams

## Phase 11 — FINAL QUALITY GATE
- [ ] Run: npm install, lint, typecheck, build, prisma validate/generate/migrate/seed, test (coverage), docker build
- [ ] Ensure no console.log, no TODO/FIXME, no secrets committed
- [ ] Ensure GitHub Actions green
