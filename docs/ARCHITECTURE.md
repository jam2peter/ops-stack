# Architecture

## Purpose

Ops Stack is an integration architecture, not a monolithic application.

Each module keeps:

- its own repository;
- its own release lifecycle;
- its own security boundary;
- its own tests and documentation.

The stack defines how those boundaries compose.

## End-to-end model

```text
Intent
  |
  v
Issue Repo Admin
  | creates resource
  v
GitHub Repository
  |
  v
Project V2 Sync
  | consolidates work
  v
GitHub Project V2
  |
  v
GitHub Agenda Sync
  | projects selected work in time
  +--> Google Tasks
  +--> Google Calendar
  |
  v
Human / automation execution
  |
  v
Auto Checkpoint
  | preserve validated state
  v
Git commit / release input
  |
  v
GitHub Actions
  | ephemeral OIDC
  v
OIDC Site Control
  |
  v
SafeDeploy endpoint
  | trust + integrity + staging + checkpoint + promotion
  v
Published target
  |
  v
HTTPS Readback
  | read-only external observation
  v
Evidence
```

## Why Agenda Sync belongs here

Agenda Sync does not replace Project V2.

Project V2 is the shared operational inventory. Agenda Sync is a projection of
selected Issues into a personal time-management surface.

This avoids two sources of truth:

```text
GitHub = authority
Google Tasks / Calendar = execution projection
```

Current synchronization is one-way from GitHub to Google.

## Why Auto Checkpoint belongs here

The deployment side already protects the published release, but there is a
separate boundary before deployment: preserving validated local work.

Auto Checkpoint's public product is fail-closed and provides:

- explicit task file selection;
- WIP preservation;
- validation commands;
- SHA-256 checkpoint manifest;
- controlled Git commit;
- push retry queue;
- explicit recovery;
- optional offsite copy.

That makes it the public **Preserve** phase. The public distribution is `jam2peter/auto-checkpoint@v0`; the private origin remains a separate runtime until an explicit migration.

## Suites vs modules

```text
RepoOps
├── Issue Repo Admin
└── Project V2 Sync

Delivery stack
├── OIDC Site Control
├── SafeDeploy
└── HTTPS Readback

Scheduling projection
└── GitHub Agenda Sync

Preserve
└── Auto Checkpoint
```

Ops Stack is the top-level composition of these pieces.

## Security principle

Composition must not broaden permissions.

A module may pass identifiers or state to the next phase, but it must not gain
the previous module's administrative privileges merely because both belong to
the stack.

Examples:

- Project V2 Sync cannot create/delete repositories.
- Agenda Sync cannot modify GitHub Issues.
- HTTPS Readback cannot deploy files.
- OIDC Site Control cannot become arbitrary shell access.
- SafeDeploy cannot write outside configured roots.
