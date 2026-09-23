# Adoption modes

## 1. Governance + personal execution

Use:

- Issue Repo Admin
- Project V2 Sync
- GitHub Agenda Sync

```text
repository -> project -> personal task/calendar
```

## 2. Secure web delivery

Use:

- OIDC Site Control
- SafeDeploy
- HTTPS Readback

```text
GitHub Actions OIDC -> constrained deploy -> external proof
```

## 3. Operational observation

Use:

- JamPeter Ops Audit for operational/control-plane evidence;
- JamPeter Ops Monitor for runtime metrics normalized from an existing
  Prometheus-compatible backend;
- JamPeter Ops Watchdog for transition detection and deduplication.

```text
Audit -------\
              +--> Watchdog --> NOTIFY / SILENT
Monitor -----/
```

Ops Monitor does not require replacing an existing Prometheus/Grafana stack.
Private endpoints and PromQL stay private.

## 4. Full lifecycle

```text
Provision -> Govern -> Schedule -> Execute -> Quality -> Preserve -> Deploy -> Verify
     \______________________________________________________________________/
                                      |
                                   OBSERVE
```

Use Quality Gate before Auto Checkpoint when validated work should be preserved.

## Integration rules

### Project V2 Sync + Agenda Sync

They may observe the same Issue but serve different purposes. GitHub remains
the authority.

### Agenda Sync + deployment

A Calendar date does not authorize deployment.

### Deploy + Readback

Readback is evidence after promotion and grants no deployment rights.

### Quality + Preserve

Quality Gate proves configured checks passed for the current Git state.
Auto Checkpoint verifies report freshness before preservation.

### Preserve + deploy

A checkpoint is evidence of preserved work, not release authorization.

### Audit + Monitor

Audit checks operational coherence. Monitor checks runtime behavior. They must
not be collapsed into one source because their cadence, evidence and failure
semantics differ.

### Monitor + existing telemetry

Ops Monitor adapts existing telemetry. It must not create a parallel metrics
database or duplicate Prometheus/Grafana merely to join the stack.

### Audit/Monitor + Watchdog

Watchdog receives sanitized state only. It should remain silent when the state
is unchanged and report both degradation and recovery transitions.

A Watchdog decision never authorizes automatic remediation.
