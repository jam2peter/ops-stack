# JamPeter Ops Stack

**JamPeter Ops Stack** is the integration architecture for a set of small,
independent GitHub-first operational tools.

The stack covers the lifecycle from creating a repository to proving that the
result of a deployment is actually reachable.

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

In short:

```text
Repository -> Project -> Agenda -> Quality -> Preserve -> Release -> Evidence
```

## Public modules

| Phase | Product | Purpose |
| --- | --- | --- |
| Provision | [Issue Repo Admin](https://github.com/jam2peter/issue-repo-admin) | Create public/private repositories from an authorized Issue command |
| Govern | [Project V2 Sync](https://github.com/jam2peter/project-v2-sync) | Reconcile Issues from managed repositories into one Project V2 |
| Schedule | [GitHub Agenda Sync](https://github.com/jam2peter/github-agenda-sync) | Project selected GitHub Issues into Google Tasks or Calendar |
| Quality | [Quality Gate](https://github.com/jam2peter/quality-gate) | Run ordered format/clean/lint/type/test/security/build gates and bind PASS to the current Git state |
| Preserve | [Auto Checkpoint](https://github.com/jam2peter/auto-checkpoint) | Preserve validated task work with private SHA-256 checkpoints, controlled commit/push and explicit recovery |
| Deploy | [OIDC Site Control](https://github.com/jam2peter/oidc-site-control) | Issue/GitHub Actions client for constrained OIDC deployment operations |
| Deploy engine | [SafeDeploy](https://github.com/jam2peter/safedeploy) | Host-side OIDC trust, staging, integrity and rollback |
| Verify | [HTTPS Readback](https://github.com/jam2peter/https-readback) | Prove a public target state with HTTP + SHA-256 + byte count |

Suite packaging remains available:

- [RepoOps](https://github.com/jam2peter/repoops) = Issue Repo Admin + Project V2 Sync
- [SafeDeploy](https://github.com/jam2peter/safedeploy) = secure deploy engine, designed to work with OIDC Site Control and HTTPS Readback

## The Agenda layer

GitHub Agenda Sync fills an important gap in the lifecycle.

Project V2 answers:

> What work exists and what state is it in?

Agenda Sync answers:

> When should the human see or do that work?

Its current model is deliberately one-way:

```text
GitHub Issue
   |
   +-- no date --> Google Task
   |
   +-- dated ----> Google Calendar Event
```

GitHub remains the source of truth. Google Tasks/Calendar are a personal
execution surface, not a second project database.

## Quality layer

Quality Gate is the verification boundary between implementation and
preservation.

```text
work changed
   |
   +--> format / clean / lint
   +--> type / compile
   +--> tests
   +--> security
   +--> build
   |
   v
quality-report.json + Git fingerprint
   |
   v
Auto Checkpoint verifies report freshness
```

Safe fixes run only when explicitly declared by the repository and explicitly
enabled by the operator. Semantic failures are not automatically repaired.

Public product: `jam2peter/quality-gate@v0`.

## Preserve layer

Auto Checkpoint is the public Preserve module between scheduling/execution and deployment:

```text
work completed
   |
   +--> classify task files and preserved WIP
   +--> validate
   +--> private checkpoint + SHA-256 manifest
   +--> controlled commit
   +--> push or retry queue
   +--> explicit recovery
   |
   v
release/deploy
```

The public product is `jam2peter/auto-checkpoint@v0`. The original private capability remains independent until any runtime migration is explicitly authorized.

## Full example

A small application can move through the stack like this:

```text
1. Intent
   Open an Issue for a new application.

2. Provision
   /repo-admin create status-page public

3. Govern
   Project V2 Sync adds and classifies its Issues in the operational Project.

4. Schedule
   GitHub Agenda Sync projects selected work:
      no date -> Google Task
      date    -> Google Calendar

5. Quality
   Quality Gate runs the repository contract and emits a PASS report tied to
   the current Git state.

6. Preserve
   Auto Checkpoint verifies that report is still current, then preserves the
   validated work before release.

7. Deploy
   GitHub Actions obtains an ephemeral OIDC identity.
   OIDC Site Control / SafeDeploy stage and promote the release.

8. Verify
   HTTPS Readback records:
      HTTP=200
      SHA256=<response digest>
      BYTES=<response size>
      RESULT=PASS
```

## Adoption modes

You do not need the whole stack.

### Work governance

```text
Issue Repo Admin
      +
Project V2 Sync
      +
GitHub Agenda Sync
```

Useful when the deployment platform is already solved.

### Delivery

```text
OIDC Site Control
      +
SafeDeploy
      +
HTTPS Readback
```

Useful when repositories already exist and you need a narrow deployment path.

### Full lifecycle

Use both groups with Quality Gate before Auto Checkpoint when local work should
be verified and checkpointed before release.

See [docs/ADOPTION.md](docs/ADOPTION.md).

## Trust continuity

The products fit together because each phase narrows or records a different
operational boundary:

```text
human intent
  -> repository resource
  -> governed work
  -> personal schedule
  -> quality evidence
  -> validated work state
  -> ephemeral deployment identity
  -> promoted release
  -> external evidence
```

No component needs to become a general-purpose administrator.

## Machine-readable manifest

[ops-stack.json](ops-stack.json) records the current modules, phase, public
repository, stable reference and integration role.

## Origin

These modules were extracted from mechanisms used in the Laboratório JamPeter,
then sanitized into independent public products. The Ops Stack repository is
only the composition/architecture layer; it does not duplicate their source
code or private runtime configuration.

## License

MIT
