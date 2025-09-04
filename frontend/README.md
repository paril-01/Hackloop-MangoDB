# REPLIKA Frontend

Run locally:

1. Start backend (see backend/README.md) and ensure it's reachable at `http://localhost:8000`.
2. Install and run frontend dev server:

```powershell
cd frontend
npm ci
npm run vite
```

3. Open `http://localhost:5173` and use the UI:
- Create a user with username+password.
- Login. The frontend uses cookie-based auth and will include credentials during requests.
- Create activities and view them.

Troubleshooting:
- CORS: Backend allows `http://localhost:5173` by default. If you run frontend on a different origin, update `app/main.py` CORS origins.
- Cookies: The frontend uses `credentials: 'include'`. Make sure the backend is setting cookies with appropriate SameSite/Domain flags in production. For development `samesite='lax'` is used.
- If e2e tests fail in CI, ensure browsers are installed (`npx playwright install --with-deps`) and the frontend dev server is running prior to tests.
