# Express Voucher Management System — Frontend UI Modernization TODO

## CRITICAL RULES (MUST FOLLOW)
- Do NOT change backend code, APIs, routes, middleware, services, database
- Do NOT change business logic, auth flow, validation, state management
- Do NOT rewrite working components — only modernize appearance
- Preserve ALL existing functions, hooks, API calls, event handlers, state variables
- Only create new files when they reduce duplication or improve maintainability

## Phase 1 — CSS MODERNIZATION (Stripe/Supabase/Vercel Premium Design)
- [ ] Rewrite styles.css with modern design system:
  - Premium color palette (neutral grays, accent blues, semantic colors)
  - Clean typography hierarchy (Inter font, proper sizing/spacing)
  - Card-based layout with subtle shadows and border-radius
  - Smooth transitions and hover animations
  - Dark mode support (CSS variables toggled by class)
  - Responsive design (mobile/tablet/desktop)
  - Loading skeleton animations
  - Toast notification styles
  - Confirmation dialog styles
  - Proper form styling (inputs, selects, textareas)
  - Button variants (primary, secondary, danger, ghost, link)
  - Table styling with hover states
  - Badge/status chip styling
  - Modal/overlay styling
  - Navigation sidebar styling
  - Top navbar styling
  - Search bar styling
  - Chart/stat card styling
  - Activity feed styling
  - Empty state styling
- [ ] Add dark mode toggle (CSS class on root, no JS state changes to existing logic)
- [ ] Add responsive breakpoints matching current structure

## Phase 2 — UI COMPONENT EXTRACTION (minimal, only where beneficial)
- [ ] Extract Toast notification system (add to main.tsx as component, preserve all existing logic)
- [ ] Extract Confirmation dialog (add to main.tsx as component)
- [ ] Extract reusable StatusBadge component
- [ ] Add loading skeleton states to dashboard (visual only, preserve data loading logic)

## Phase 3 — STREAMLIT DASHBOARD MODERNIZATION
- [ ] Update .streamlit/config.toml with premium theme
- [ ] Update components/ui.py with modern styling matching React design
- [ ] Update all pages with consistent premium look

## Phase 4 — TESTING (Thorough)
- [ ] Run backend tests: app.test.ts, auth.test.ts, voucher.workflow.test.ts
- [ ] Run frontend typecheck: npm run typecheck
- [ ] Run frontend build: npm run build
- [ ] Test all API endpoints via curl:
  - POST /api/v1/auth/login (valid + invalid credentials)
  - POST /api/v1/auth/refresh
  - POST /api/v1/auth/logout
  - GET /api/v1/auth/me
  - GET /api/v1/vouchers
  - POST /api/v1/vouchers (create draft)
  - GET /api/v1/vouchers/:id
  - PATCH /api/v1/vouchers/:id
  - DELETE /api/v1/vouchers/:id
  - POST /api/v1/vouchers/:id/submit
  - POST /api/v1/vouchers/:id/approve (DIRECTOR only)
  - POST /api/v1/vouchers/:id/reject (DIRECTOR only)
  - GET /api/v1/vouchers/dashboard
  - GET /api/v1/users
  - GET /api/v1/users/:id
  - GET /health, /live, /ready, /metrics
- [ ] Test role-based access (EMPLOYEE, DIRECTOR, ACCOUNTS)
- [ ] Test error scenarios (invalid tokens, unauthorized access, validation errors)
- [ ] Test frontend login/logout flow
- [ ] Test frontend voucher creation
- [ ] Test Streamlit dashboard login + all pages
- [ ] Test responsive layout (mobile, tablet, desktop)
- [ ] Test dark mode toggle

## Phase 5 — FINAL QUALITY CHECKS
- [ ] Ensure no console.log in production code
- [ ] Ensure no TODO/FIXME comments
- [ ] Ensure no secrets committed
- [ ] Verify all tests pass
- [ ] Verify frontend builds successfully
- [ ] Verify backend compiles successfully
