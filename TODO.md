# Express Voucher Management System — Frontend UI Modernization TODO

## CRITICAL RULES (MUST FOLLOW)
- Do NOT change backend code, APIs, routes, middleware, services, database
- Do NOT change business logic, auth flow, validation, state management
- Do NOT rewrite working components — only modernize appearance
- Preserve ALL existing functions, hooks, API calls, event handlers, state variables
- Only create new files when they reduce duplication or improve maintainability

## Phase 1 — CSS MODERNIZATION (Stripe/Supabase/Vercel Premium Design)
- [x] Rewrite styles.css with modern design system:
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
- [x] Add dark mode toggle (CSS class on root, no JS state changes to existing logic)
- [x] Add responsive breakpoints matching current structure

## Phase 2 — UI COMPONENT EXTRACTION (minimal, only where beneficial)
- [x] Extract Toast notification system (components.tsx - ToastContainer + showToast)
- [x] Extract Confirmation dialog (components.tsx - ConfirmDialog)
- [x] Extract reusable StatusBadge component (components.tsx - StatusBadge)
- [x] Add dark mode toggle button to Dashboard topbar
- [x] Integrate ToastContainer into App component

## Phase 3 — STREAMLIT DASHBOARD MODERNIZATION
- [x] Update .streamlit/config.toml with premium theme (indigo accent, dark slate palette)
- [x] Update app.py with premium CSS injection (sidebar gradient, metric cards, login card, buttons)
- [x] Update components/ui.py with modern styling matching React design
- [x] Update all pages with consistent premium look (01_Vouchers, 02_Create_Voucher, 03_Users, 04_Analytics, 05_Health)

## Phase 4 — TESTING (Thorough)
- [x] Run backend tests: app.test.ts (1 passed), auth.test.ts (4 skipped - needs DB), voucher.workflow.test.ts (4 skipped - needs DB)
- [x] Run frontend build: npm run build (succeeded)
- [ ] Run frontend typecheck: npm run typecheck
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
- [x] Verify frontend builds successfully
- [ ] Verify backend compiles successfully
