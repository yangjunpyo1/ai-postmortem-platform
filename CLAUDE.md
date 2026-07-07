# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

An AI-powered incident postmortem automation platform (Korean project — code identifiers are English, but commit messages, docs, and API error strings are Korean). Slack incident chatter is collected and analyzed by the Claude API to auto-generate postmortem documents, alongside a React dashboard for browsing incident history. Design docs (in Korean) live in `docs/01_기획서.md` through `docs/06_시스템아키텍처.md` — read `docs/06_시스템아키텍처.md` for the full architecture diagram and data-flow description before making infra-level changes.

## Architecture

Three independently deployed Lambda functions sit behind this system, all written in Python and packaged as zip files for Terraform (no CI/CD — deploys are manual):

- **`backend/app`** (`yp-lambda-fastapi`) — FastAPI app wrapped in Mangum, handles all `/api/*` REST endpoints for the web dashboard. `handler = Mangum(app, ...)` in `backend/app/main.py` is the Lambda entrypoint (`app.main.handler`). Runs behind API Gateway with `root_path="/dev"`.
- **`lambda/alarm/handler.py`** (`yp-lambda-alarm`) — triggered by SQS (fed from an SNS topic that CloudWatch alarms publish to). Classifies severity from the CloudWatch alarm name (`critical`/`warning`/info) and posts a formatted Slack message.
- **`lambda/postmortem/handler.py`** (`yp-lambda-postmortem`) — triggered asynchronously (via `lambda_client.invoke(InvocationType="Event", ...)` from `backend/app/api/slack.py`) when a user runs the `/resolve` Slack slash command. It looks up the active incident in RDS, collects Slack conversation history + CloudWatch logs/metrics for the incident window, calls the Claude API to draft a structured postmortem (JSON), writes the postmortem + slack messages to RDS, and posts a completion message back to Slack.

Data flow for the demo scenario (see `docs/06_시스템아키텍처.md` §4): CloudWatch → SNS → SQS → `alarm` Lambda → Slack alert → engineers discuss in Slack → `/resolve` command → `postmortem` Lambda collects context → Claude API → RDS → dashboard.

Everything runs inside a single VPC (`terraform/main.tf`): public subnets host the NAT Gateway, private "app" subnets host the three Lambdas + an EC2 instance running Grafana (CloudWatch metric visualization), private "db" subnets host RDS MySQL (primary/standby). AWS resources are consistently prefixed with `project_name` (`yp`, see `terraform/variables.tf`).

### Backend (`backend/app`)

- `main.py` — FastAPI app setup, CORS (wide open, `allow_origins=["*"]`, with a catch-all `OPTIONS` preflight handler), router registration, `Base.metadata.create_all` on cold start, `/health` endpoint.
- `api/` — one router module per resource: `auth.py` (register/login/logout, JWT issuance, and the shared `get_current_user` dependency imported by every other router), `incidents.py`, `postmortems.py`, `similar.py` (category/severity-based "similar incidents" lookup), `statistics.py`, `slack.py` (Slack Events API + slash-command webhook; `/resolve` invokes the `postmortem` Lambda by name).
- `models/` — SQLAlchemy ORM models: `User` 1—N `Incident` 1—1 `Postmortem`, `Incident` 1—N `SlackMessage`.
- `schemas/` — Pydantic request/response models (Pydantic v2 style, `from_attributes = True`).
- `core/config.py` — `pydantic_settings.BaseSettings` loaded from `.env` (DB creds, JWT `SECRET_KEY`/`ALGORITHM`/expiry).
- `core/security.py` — bcrypt password hashing + JWT encode/decode (`python-jose`).
- `database.py` — SQLAlchemy engine/session (`mysql+pymysql`), `get_db` FastAPI dependency.
- Auth pattern: every protected route depends on `get_current_user` from `app.api.auth`, which decodes the bearer JWT and loads the `User`. There is no role/permission system — any authenticated user can access any incident.

### Frontend (`frontend/`)

Create React App (react-scripts 5) + Tailwind. Routing via `react-router-dom` v7 in `App.js`; all routes except `/login` and `/register` are wrapped in `components/PrivateRoute.js`, which simply checks `localStorage.getItem('access_token')`. `hooks/useAuth.js` provides `isAuthenticated`/`logout`. `api/axios.js` is the single HTTP client: request interceptor attaches the JWT bearer token, response interceptor clears the token and redirects to `/login` on any 401. `@tanstack/react-query` and `recharts` are available for data fetching/statistics visualization. `REACT_APP_API_URL` (in `.env` / `.env.production`) points at the API Gateway `/dev` stage and must match the deployed backend's invoke URL.

## Common commands

### Frontend
```
cd frontend
npm start          # dev server
npm run build       # production build (output consumed by S3/CloudFront deploy)
npm test             # CRA/Jest test runner
```

### Backend
There is no local dev server script — the FastAPI app is only run inside Lambda via Mangum. To install dependencies for local iteration or before packaging:
```
cd backend
pip install -r requirements.txt
```

### Database migrations (Alembic, run from `backend/`)
```
alembic revision --autogenerate -m "description"
alembic upgrade head
```
Alembic reads `DATABASE_URL` indirectly through `app.database`/`app.core.config`, so a working `.env` (or exported `DB_*` env vars) is required.

### Lambda packaging (manual — no build script exists)
Each Lambda is deployed as a zip that Terraform reads directly (`terraform/modules/lambda/main.tf`):
- `yp-lambda-fastapi` expects `terraform/modules/lambda/lambda_fastapi.zip` containing `backend/app/` plus vendored third-party deps (installed into `backend/package/`, which is gitignored — rebuild with `pip install -r requirements.txt -t backend/package`) zipped together so `app.main.handler` is importable.
- `yp-lambda-alarm` / `yp-lambda-postmortem` expect zips at `lambda/alarm/lambda_alarm.zip` / `lambda/postmortem/lambda_postmortem.zip`, handler `handler.handler`.
After rebuilding a zip, re-run `terraform apply` (Terraform detects the change via the zip's hash).

### Terraform (run from `terraform/`)
```
terraform init
terraform plan
terraform apply
```
Requires `terraform.tfvars` with sensitive values (`rds_password`, `slack_bot_token`, `slack_channel_id`, `claude_api_key`) — never commit this file (already gitignored).

## Conventions and gotchas

- Error/response strings returned to API clients are written in Korean (e.g. `"장애를 찾을 수 없습니다."`) — match this convention in new endpoints rather than switching to English.
- Incident `status` values are Korean strings: `"발생중"` (active) and `"종료"` (resolved), not English enums — filter/compare against these literals.
- `backend/lambda_fastapi.zip`, `backend/package/`, and other `*.zip` artifacts are gitignored build outputs, not source — don't hand-edit them; regenerate from `backend/app` instead.
- The `postmortem` Lambda (`lambda/postmortem/handler.py`) talks to RDS directly via raw `pymysql`/SQL, independent of the FastAPI app's SQLAlchemy models in `backend/app/models/` — if you change the `incidents`/`postmortems`/`slack_messages` schema, update both the SQLAlchemy models *and* the raw SQL in this handler.
- CloudWatch log group names and the EC2 instance ID are hardcoded in `lambda/postmortem/handler.py` and `terraform/modules/lambda/main.tf` (`i-0dda1ca124f27304a`) — these are environment-specific and will need updating for any new deployment.
