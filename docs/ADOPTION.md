# Adoption modes

## 1. Governance + personal execution

Use:

- Issue Repo Admin
- Project V2 Sync
- GitHub Agenda Sync

Flow:

```text
repository -> project -> personal task/calendar
```

This is useful when deployment is already handled elsewhere.

## 2. Secure web delivery

Use:

- OIDC Site Control
- SafeDeploy
- HTTPS Readback

Flow:

```text
GitHub Actions OIDC -> constrained deploy -> external proof
```

This is useful for small PHP/shared-hosting or similar environments where broad
SSH/FTP credentials in CI are undesirable.

## 3. Full lifecycle

Combine both groups:

```text
Provision -> Govern -> Schedule -> Execute -> Preserve -> Deploy -> Verify
```

Use Auto Checkpoint before Deploy when validated local work should be preserved:

```text
... -> Schedule -> Execute -> Auto Checkpoint -> Deploy -> Verify
```

## Integration rules

### Project V2 Sync + Agenda Sync

They may observe the same Issue, but serve different purposes.

- Project V2 Sync reconciles shared operational state.
- Agenda Sync only processes Issues explicitly marked as managed by its metadata
  contract and projects them to Google.

Do not make Google the authority for Project state.

### Agenda Sync + deployment

A Calendar date does not authorize a deployment. Deployment remains controlled
by repository/workflow policy.

### Deploy + Readback

Readback is evidence after promotion. It does not grant deployment rights and
requires no server secret.

### Preserve + deploy

A checkpoint is evidence of preserved work, not automatic authorization to
release. The deployment workflow remains an explicit boundary.
