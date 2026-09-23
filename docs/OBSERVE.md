# OBSERVE layer

OBSERVE is the cross-cutting operational assurance layer of JamPeter Ops Stack.

It is deliberately not another linear delivery phase.

```text
PROVISION -> GOVERN -> SCHEDULE -> QUALITY -> PRESERVE -> DEPLOY -> VERIFY
     \______________________________________________________________/
                                |
                             OBSERVE
                 AUDIT + MONITOR + ALERT
```

## AUDIT — JamPeter Ops Audit

Audit checks control-plane coherence: workflows, CI, deployment evidence,
GitHub capacity, public readback and tracked operational blockers.

Question:

> Is the operational control plane coherent?

Audit is snapshot-oriented and may run at a lower frequency than telemetry.

## MONITOR — JamPeter Ops Monitor

Monitor uses existing monitoring engines rather than replacing them.

Typical upstream systems are Prometheus, Grafana, exporters and logging
pipelines. The public adapter normalizes allowlisted Prometheus queries into a
small sanitized state snapshot.

Question:

> How is the runtime behaving now?

Private endpoints, queries and credentials remain deployment configuration and
must not be committed to the public product.

## ALERT — JamPeter Ops Watchdog

Watchdog consumes sanitized Audit and Monitor snapshots, compares them with a
previous baseline and decides whether a notification is warranted.

Question:

> Did state change enough to notify a human?

The public engine performs transition detection and deduplication. Notification
delivery is separate, and automatic remediation is intentionally out of scope.

## Trust boundary

Composition does not grant new privileges.

- Audit may observe operational evidence but cannot deploy.
- Monitor may read allowlisted metrics but cannot administer Prometheus.
- Watchdog may decide NOTIFY/SILENT but cannot remediate a system.
- A notification never authorizes a deployment or infrastructure mutation.

## Cost principle

OBSERVE is designed to reuse existing monitoring and control-plane systems.
It requires no new database and no paid monitoring service by design.
