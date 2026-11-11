# Security, privacy and applicable obligations

## Select tools deliberately

Inspect repository manifests, lockfiles, CI and existing security configuration. Propose tools suited to the technology and available access. Examples below are options, not bundled dependencies or a universal sequence. Consult their current official documentation for installation and flags.

| Surface | Tool examples | What still needs investigation |
|---|---|---|
| Known dependency vulnerabilities | npm audit, pip-audit, OSV-Scanner | Exploitability, reachable code, patched-version compatibility |
| Source patterns / flows | Semgrep, CodeQL, Bandit for Python | Context, false positives and business logic |
| Accidentally committed credentials | Gitleaks | Revocation/rotation by the authorized owner; report redacted locations |
| Containers / infrastructure | Trivy, Checkov | Runtime permissions, network and deployment configuration |
| Running web application | OWASP ZAP in an agreed test environment | Authorization logic, workflow abuse and destructive side effects |

Execute an installed scanner through its supported interface; Atlas does not ship a vulnerability database. Record tool/version, rules or database freshness when available, target/revision, time, configuration, exclusions and output location. Preserve errors and inaccessible databases as incomplete. Triage findings with evidence; distinguish potential from reproduced vulnerabilities. Do not automatically apply breaking dependency upgrades.

## Pentest boundaries

Before active testing, establish owned/authorized targets, environment, permitted techniques, rate limits, data boundaries and stop conditions. General permission to review code does not authorize attacking third-party infrastructure or production. Prefer passive review and test fixtures until active scope is explicit. Stop on unexpected sensitive data or destructive effects; retain only redacted evidence. Use synthetic accounts across roles/tenants for access-control checks.

## Privacy and legal research

First establish operating jurisdictions, user locations, type of organization, processing purposes, personal/sensitive data categories, vendors and cross-border flows. Do not assume every law applies. Research current authoritative sources for the relevant question (for Brazil, official legislation and ANPD guidance; other jurisdictions require their own authorities). Include exact source link, retrieval date, applicability assumptions and uncertainty in the assessment.

Convert applicable obligations into traceable technical questions: data minimization, authorization, retention/deletion, user rights workflows, logging, vendor boundaries and incident processes. Link each to observed implementation and gaps. A consent banner alone does not establish compliance, and consent is not automatically the appropriate basis for every processing activity.

Separate observed technical controls, potential legal obligations and matters for qualified legal review. Never claim certification, universal LGPD compliance or coverage of every law from an automated scan. Do not embed stale legal deadlines or universal legal checklists in project rules.
