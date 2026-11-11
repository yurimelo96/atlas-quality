# Recommend a quality architecture from the system

Use this for onboarding, an explicit tool/framework recommendation, or a material architecture change. Recommend a quality architecture around the current product. Do not redesign its production architecture unless requested.

## Understand enough to decide

Inspect repository/configuration and existing records first. Fill gaps with a few grouped questions, not a mandatory questionnaire:

- Product and stakes: SaaS, internal tool, marketplace, mobile, API-only? Critical journeys and unacceptable failures?
- Stack and access: frontend/backend versions, data stores, queues, external APIs, hosting, source/export access and existing tests/CI?
- Boundaries: roles, tenants, identity, payments, webhooks, personal data and relevant jurisdictions?
- Constraints: available test environment, team/maintenance capacity, time/budget and provider/tool restrictions?
- AI/no-code: generated implementation only, AI functionality at runtime, or platform-managed logic? Which parts can be inspected and reproduced?

Do not ask for secrets. Distinguish user-reported facts, observed facts and assumptions. An API-only service does not need browser E2E; SaaS does not automatically imply multiple tenants, subscriptions or payments. Ask or make a clearly conditional proposal.

## Select a coherent minimum

Map each critical behavior to a test layer and the cheapest faithful environment. Prefer compatible existing frameworks; verify versions, async model, drivers, test isolation and CI feasibility against official documentation. Do not copy current-version configuration into an older project blindly.

Recommend one primary tool per responsibility. For each proposed addition, provide the risk it covers, why existing tools are insufficient, maintenance/setup cost, access dependencies and a lighter fallback. Categorize choices as **reuse now**, **add now**, **later if justified** or **not applicable**. Explain tradeoffs rather than ranking by popularity.

For skills, inspect the host's available catalog and read relevant instructions. Select the smallest useful set by capability (API testing, database testing, accessibility, etc.). Only give an invocation name after confirming it exists. For an external candidate, verify its source, contents, license and compatibility; label it not installed and recommend it without installing by default. A skill recommendation is separate from its underlying tool dependency.

## Recommendation output

Keep the report proportional to the project. Include:

1. System summary, sources, assumptions and missing information.
2. Critical journeys and highest-impact failure risks.
3. Proposed layers/tools/skills, responsibilities and integration surfaces.
4. Initial tests with specific expected outcomes and test-data isolation.
5. A practical first increment, followed by conditional later work.
6. What can run now, what needs setup/access and what the user skipped.

Persist an accepted quality architecture in existing documentation or `docs/quality/quality-architecture.md`. Record the capability inventory in that document or a nearby existing integration record. Mark proposals vs implemented/verified parts. Skipped recommendations retain their residual risk and revisit condition. Do not label a proposal accepted merely because the user has not responded.

## Worked example: FastAPI + PostgreSQL SaaS built with AI assistance

This is a conditional example, not a detected project or a universal stack. Assume source access, Python backend, an isolated PostgreSQL test service and a web UI; confirm versions and actual authentication, ORM and tenancy design. AI-assisted origin prompts scrutiny of requirements, assertions and integration; it is not evidence of a defect.

| Responsibility / risk | Initial recommendation | Concrete checks / applicability |
|---|---|---|
| Domain rules | Reuse pytest if present; otherwise consider it | Limits, empty/invalid input and business invariants from independent requirements. Add property testing only where useful. |
| FastAPI routes | TestClient for suitable synchronous cases, or HTTPX AsyncClient with ASGI transport and an appropriate async test plugin | Authenticated/anonymous access, response schemas, errors and validation; arrange lifespan explicitly if the selected transport does not do so. Use the project's actual dependency overrides. |
| PostgreSQL integration | Isolated PostgreSQL matching relevant production features; existing test service or disposable containers if available | Constraints, transaction rollback, concurrent updates, migrations from supported prior schemas. Use unique databases/schemas or controlled fixtures. SQLite does not establish PostgreSQL-specific behavior. |
| Data access | Reuse the installed driver/ORM; inspect SQLAlchemy/Alembic only if used | Session lifecycle, migrations, connection limits and query behavior. Do not introduce an ORM just for tests. |
| SaaS authorization | Role/resource/action matrix; add tenant dimension if multi-tenant | Tenant A cannot read/update tenant B; denial enforced at the server, including exports and async jobs where present. |
| UI journeys | Reuse existing browser suite; consider Playwright if none and browser flows matter | Login and one critical end-to-end journey; trace/report artifacts on failures. No UI means this layer is not applicable. |
| Payments/webhooks | Provider test mode and synthetic signed payloads if those features exist | Invalid signatures rejected; duplicate events do not duplicate entitlement or billing effects. |
| Security baseline | Existing dependency and source scanning; select missing coverage deliberately | Triage dependency findings, authorization, secrets and injection boundaries; use the security reference for tool choices and scope. |
| Accessibility | Browser automation with axe where supported plus focused manual checks | Keyboard, focus, error recovery and screen-reader gaps; automated results remain partial. |
| Performance | Later: workload tool if latency, concurrency or resource risk justifies it | Set a realistic workload and measurable budget before load generation. Do not infer traffic from 'SaaS'. |
| Runtime AI | Only if product calls a model: versioned evaluation set using existing provider access | Output contracts, unsafe actions, prompt injection, sensitive-data handling and repeated results. |

Suggested first increment: verify backend rules and API contracts, database isolation/migrations and applicable authorization boundaries. Add one critical UI journey if a UI exists. Expand only when evidence or risks justify it; the user can change that order or defer a layer.

Potential skill capabilities: Python/API testing, database/migration testing, browser automation, security review and accessibility. Resolve them against the actual catalog, rather than claiming these are bundled child skills.

### Official references

Consult the project's matching documentation versions; reviewed as starting points on 2026-11-11:

- [FastAPI async tests](https://fastapi.tiangolo.com/advanced/async-tests/): async testing and application lifespan considerations.
- [SQLAlchemy PostgreSQL dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html): PostgreSQL-specific behavior when that ORM/version is used.
- [Playwright assertions](https://playwright.dev/docs/test-assertions): observable, retrying browser assertions.
