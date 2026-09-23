# JamPeter Ops Stack

**JamPeter Ops Stack** is a composition architecture for small, independent,
GitHub-first operational tools.

The linear lifecycle manages delivery. A cross-cutting **OBSERVE** layer
continuously provides operational assurance without broadening module
permissions.

> Status: `v0.1-beta` architecture distribution.

## Lifecycle

```text
PROVISION
Issue Repo Admin
      |
      v
GOVERN
Project V2 Sync
      |
      v
SCHEDULE
GitHub Agenda Sync
      |
      v
QUALITY
Quality Gate
      |
      v
PRESERVE
Auto Checkpoint
      |
      v
DEPLOY
OIDC Site Control + SafeDeploy
      |
      v
VERIFY
HTTPS Readback
```

Cross-cutting observation:

```text
PROVISION -> GOVERN -> SCHEDULE -> QUALITY -> PRESERVE -> DEPLOY -> VERIFY
     \______________________________________________________________/
                                |
                             OBSERVE
                 AUDIT + MONITOR + ALERT
```

In short:

```text
Repository -> Project -> Agenda -> Quality -> Preserve -> Release -> Evidence
                                  +
                         continuous observation
```

## Public modules

| Role | Product | Purpose |
| --- | --- | --- |
| Provision | [Issue Repo Admin](https://github.com/jam2peter/issue-repo-admin) | Create repositories from an authorized Issue command |
| Govern | [Project V2 Sync](https://github.com/jam2peter/project-v2-sync) | Reconcile Issues into Project V2 |
| Schedule | [GitHub Agenda Sync](https://github.com/jam2peter/github-agenda-sync) | Project selected Issues into Google Tasks or Calendar |
| Quality | [Quality Gate](https://github.com/jam2peter/quality-gate) | Execute repository quality contracts |
| Preserve | [Auto Checkpoint](https://github.com/jam2peter/auto-checkpoint) | Preserve validated work and controlled Git state |
| Deploy | [OIDC Site Control](https://github.com/jam2peter/oidc-site-control) | Constrained OIDC deployment control |
| Deploy engine | [SafeDeploy](https://github.com/jam2peter/safedeploy) | Staging, integrity, checkpoint and rollback |
| Verify | [HTTPS Readback](https://github.com/jam2peter/https-readback) | External HTTP/hash/size evidence |
| Observe / Audit | [JamPeter Ops Audit](https://github.com/jam2peter/ops-audit) | Control-plane coherence and operational evidence |
| Observe / Monitor | [JamPeter Ops Monitor](https://github.com/jam2peter/ops-monitor) | Normalize monitoring metrics into sanitized states |
| Observe / Alert | [JamPeter Ops Watchdog](https://github.com/jam2peter/ops-watchdog) | Detect state transitions and deduplicate notifications |

Suite packaging remains available:

- [RepoOps](https://github.com/jam2peter/repoops) = Issue Repo Admin + Project V2 Sync
- [SafeDeploy](https://github.com/jam2peter/safedeploy) = deploy engine integrated with control and readback

## OBSERVE

OBSERVE deliberately separates three questions.

### AUDIT — Ops Audit

> Is the operational control plane coherent?

Audit looks at workflows, CI, deployment/readback evidence, GitHub capacity and
tracked blockers. It is snapshot-oriented.

### MONITOR — Ops Monitor

> How is the runtime behaving now?

Monitor uses existing Prometheus/Grafana/exporter infrastructure and normalizes
allowlisted metrics. It does not replace the monitoring engine.

### ALERT — Ops Watchdog

> Did state change enough to notify a human?

Watchdog compares sanitized Audit/Monitor states with the previous baseline.
Unchanged states remain silent; worsening and recovery are explicit
transitions. It does not remediate systems.

See [docs/OBSERVE.md](docs/OBSERVE.md).

## The Agenda layer

Project V2 answers what work exists. Agenda Sync answers when the human should
see or do selected work.

```text
GitHub Issue
   +-- no date --> Google Task
   +-- dated ----> Google Calendar Event
```

GitHub remains the source of truth.

## Quality and Preserve

Quality Gate verifies repository-defined checks and binds the result to the Git
state. Auto Checkpoint verifies freshness before preserving validated work.

```text
work -> Quality Gate -> quality evidence -> Auto Checkpoint -> release input
```

Neither a Quality PASS nor a checkpoint is automatic deployment authorization.

## Full example

```text
1. Intent      -> Issue
2. Provision   -> repository
3. Govern      -> Project V2
4. Schedule    -> Task / Calendar
5. Quality     -> Quality Gate
6. Preserve    -> Auto Checkpoint
7. Deploy      -> OIDC Site Control / SafeDeploy
8. Verify      -> HTTPS Readback

Throughout:
Audit + Monitor -> Watchdog -> human notification only on relevant transition
```

## Adoption modes

The stack is modular.

- Governance: Repo Admin + Project V2 Sync + Agenda Sync.
- Delivery: OIDC Site Control + SafeDeploy + HTTPS Readback.
- Observe: Ops Audit + Ops Monitor + Ops Watchdog.
- Full lifecycle: combine the required modules; OBSERVE remains cross-cutting.

See [docs/ADOPTION.md](docs/ADOPTION.md).

## Trust continuity

Composition must not create a general-purpose administrator.

```text
human intent
  -> resource
  -> governed work
  -> schedule
  -> quality evidence
  -> preserved state
  -> constrained deployment
  -> external evidence

OBSERVE reads bounded evidence across these boundaries.
```

Audit cannot deploy. Monitor cannot administer Prometheus. Watchdog cannot
remediate. Their composition therefore increases visibility without increasing
execution authority.

## Machine-readable manifest

[ops-stack.json](ops-stack.json) records the lifecycle and the cross-cutting
OBSERVE modules.

## Origin

The modules were extracted from mechanisms used in Laboratório JamPeter and
sanitized into independent public products. Ops Stack is the composition layer;
it does not duplicate private runtime configuration.

## License

MIT
