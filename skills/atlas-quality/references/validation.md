# Choose checks from risk

Use this matrix as a starting point, not a mandatory checklist. Explain omissions when they affect the conclusion. Use the project's versions and commands; consult current official tool documentation when adding or changing configuration.

| Change or system | Useful evidence | Typical missed failure |
|---|---|---|
| Business rule / calculation | Focused unit or property tests with boundaries and invalid inputs | Rounding, empty values, timezone, overflow |
| API / integration | Schema, contract and integration tests; auth and error cases | Consumer incompatibility, retries duplicating operations |
| Database / migration | Disposable database, forward migration, constraint and integrity checks; recovery plan | Data loss, tenant leakage, incompatible old clients |
| UI / web journey | Component tests and a small set of critical E2E paths | Loading/error/empty states, back navigation, failed submission |
| Visual / design | Compare approved reference at relevant viewports; inspect focus, zoom and content overflow | Unapproved baseline changes hiding regressions |
| Permissions / identity | Role × resource × action matrix; server-side denial across tenants | UI hides an action but backend still permits it |
| Dependencies / CI / config | Lockfile, tool versions, build and deployment assumptions | Tests run against the wrong artifact or no tests selected |
| Performance | Repeatable workload, baseline, environment and latency distributions | Synthetic average hides slow tails or resource exhaustion |
| Mobile | Device/OS constraints, gestures, permissions, offline and lifecycle | Background/resume loses state |
| AI feature | Representative versioned eval cases, expected properties, repeated runs and cost | Nondeterminism, unsafe tool action, prompt injection, data exposure |
| No-code / low-code | Workflow exports or version IDs, permission checks, triggers and real journeys in test workspace | Vendor limits, repeated webhooks, hidden rules and irreversible actions |

## AI coding output

Compare behavior with the request rather than the agent's completion narrative. Look for imaginary dependencies, unused code paths, disabled checks, broad unrelated edits and tests derived from the same mistaken assumption as the implementation. Verify generated code integrates with real consumers. Do not label code defective merely because it was AI-generated.

## Accessibility and experience

Use available automated accessibility tooling such as axe as partial evidence. Complement it with keyboard navigation, visible focus, labels, error recovery, zoom/reflow, contrast and screen-reader checks when relevant and possible. Report which checks were automated, manually observed or untested. A tool's lack of findings does not certify accessibility.

## Test growth

Add regression tests for reproducible defects and important uncovered contracts. Prefer the cheapest layer that detects the failure faithfully; reserve E2E for cross-boundary journeys. Reuse fixtures and avoid unnecessary architecture changes such as enforcing Page Objects in an established suite. Keep flaky results visible and distinguish retries from first-attempt success.
