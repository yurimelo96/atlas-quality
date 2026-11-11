# Living records and traceability

Reuse existing paths first. On initial QA onboarding, the optional helper can create:

```text
docs/quality/
  system-map.md    # boundaries, journeys, data, sources, unknowns
  decisions.md     # important rules and methods, reasons, applicability
  changes.md       # change → risk → validation → remaining work
.atlas/
  runs/<unique-id>/result.json
```

Keep generated run artifacts out of Git by default; commit curated, redacted summaries. For regulated projects, follow the project's approved evidence storage and retention policy. Local JSON files are editable records, not tamper-proof audit trails.

## Map

For each significant component: purpose, source path/platform view, dependencies, trust boundary, critical journeys, data classes and known validation tools. Label observed vs inferred and record source revision/date. Unknowns should have a next investigation, not invented detail.

## Decision

Record ID/date, context, chosen method or rule, reason, scope, rejected alternatives only when useful, and revisit condition. Preserve superseded decisions with a link to their replacement. Record only consequential decisions; do not mirror chat transcripts.

## Change record

Record change ID, requirement/source, baseline/head or platform versions, dirty state, affected components, risk, check IDs and evidence, outcome and documentation updates. If no Git metadata is available, say so. Link the current pre-record revision; never fabricate the SHA of a future commit containing the record.

## Evidence and skipped checks

For every material check: ID, intended behavior, method, target/version, command or manual procedure, time, result and interpretation. States: planned, executed (uninterpreted), passed (interpreted), failed, skipped, blocked, incomplete, not applicable. A skipped check includes who requested it, the supplied reason or 'not supplied', residual risk, and when to revisit. If it was skipped by the agent as irrelevant, explain that applicability judgment instead of attributing it to the user.

Never store tokens, passwords, real personal data, full HTTP bodies or environment dumps in these records. The helper avoids capturing command output or full arguments by default; custom labels/reasons still need review. Do not claim comprehensive automatic redaction.
