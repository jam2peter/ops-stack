# Architecture

## Purpose

Ops Stack is an integration architecture, not a monolithic application.

Each module keeps its own repository, release lifecycle, security boundary,
tests and documentation. The stack defines how those boundaries compose.

## End-to-end model

```text
Intent
  |
  v
Issue Repo Admin
  |
  v
GitHub Repository
  |
  v
Project V2 Sync
  |
  v
GitHub Project V2
  |
  v
GitHub Agenda Sync
  +--> Google Tasks
  +--> Google Calendar
  |
  v
Human / automation execution
  |
  v
Quality Gate
  |
  v
Auto Checkpoint
  |
  v
GitHub Actions / release input
  |
  v
OIDC Site Control
  |
  v
SafeDeploy
  |
  v
Published target
  |
  v
HTTPS Readback
  |
  v
Evidence
```

The full lifecycle is observed by a parallel assurance layer:

```text
                     OBSERVE
            +------------------------+
            | Audit                  |
lifecycle --+ Monitor                +--> Watchdog --> NOTIFY / SILENT
            |                        |
            +------------------------+
```

## Why OBSERVE is cross-cutting

Audit, metrics and alerts do not create the next lifecycle object. They observe
multiple phases at once.

Representing OBSERVE as a final linear phase would be misleading: monitoring
must also see work before deployment, and Audit may verify workflows,
governance, quotas and blockers unrelated to one release.

Therefore `ops-stack.json` keeps the delivery lifecycle in `phases` and
defines OBSERVE separately.

## Audit vs Monitor vs Watchdog

### Ops Audit

Audit evaluates operational coherence and evidence.

Typical inputs:

- workflow results;
- Quality Gate state;
- deploy/readback evidence;
- API capacity;
- tracked blocker state.

### Ops Monitor

Monitor evaluates runtime behavior from existing telemetry systems.

Typical upstreams:

- Prometheus;
- exporters;
- Grafana-facing metrics;
- logging/telemetry systems.

The public product is a normalization adapter. It does not replace Prometheus
or Grafana.

### Ops Watchdog

Watchdog consumes sanitized states from Audit and Monitor. It owns transition
classification and deduplication, not notification-provider credentials and not
remediation.

```text
baseline -> SILENT
same state -> SILENT
PASS -> DEGRADED -> NOTIFY
DEGRADED -> PASS -> NOTIFY
```

## Existing lifecycle boundaries

Agenda Sync is a one-way projection from GitHub authority to personal time
management.

Quality Gate turns repository-defined checks into machine-readable quality
evidence tied to Git state.

Auto Checkpoint preserves validated state without authorizing deployment.

SafeDeploy and OIDC Site Control constrain release operations.

HTTPS Readback is read-only proof after promotion.

## Suites vs modules

```text
RepoOps
├── Issue Repo Admin
└── Project V2 Sync

Delivery
├── OIDC Site Control
├── SafeDeploy
└── HTTPS Readback

Schedule
└── GitHub Agenda Sync

Quality
└── Quality Gate

Preserve
└── Auto Checkpoint

OBSERVE
├── JamPeter Ops Audit
├── JamPeter Ops Monitor
└── JamPeter Ops Watchdog
```

## Security principle

Composition must not broaden permissions.

- Project V2 Sync cannot create/delete repositories.
- Agenda Sync cannot modify GitHub Issues.
- Quality Gate cannot commit, push or deploy changes.
- HTTPS Readback cannot deploy files.
- OIDC Site Control cannot become arbitrary shell access.
- SafeDeploy cannot write outside configured roots.
- Ops Audit cannot deploy or remediate.
- Ops Monitor cannot administer the monitoring backend.
- Ops Watchdog cannot repair a system.

A notification is evidence, not authorization.
