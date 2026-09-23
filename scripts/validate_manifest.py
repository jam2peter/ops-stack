#!/usr/bin/env python3
import json
from pathlib import Path

data=json.loads(Path("ops-stack.json").read_text(encoding="utf-8"))
phases={item["id"]:item for item in data["phases"]}
required={"provision","govern","schedule","quality","preserve","deploy-control","deploy-engine","verify"}
missing=required-set(phases)
if missing:
    raise SystemExit("missing phases: "+",".join(sorted(missing)))

observe=data.get("observe")
if not isinstance(observe,dict) or observe.get("mode")!="cross-cutting":
    raise SystemExit("cross-cutting observe layer missing")

modules={item["id"]:item for item in observe.get("modules",[])}
required_observe={"audit","monitor","alert"}
missing_observe=required_observe-set(modules)
if missing_observe:
    raise SystemExit("missing observe modules: "+",".join(sorted(missing_observe)))

expected={
    "audit":("ops.audit-active","jam2peter/ops-audit"),
    "monitor":("ops.monitoring","jam2peter/ops-monitor"),
    "alert":("ops.watchdog","jam2peter/ops-watchdog"),
}
for module_id,(capability,repository) in expected.items():
    module=modules[module_id]
    if module.get("capability")!=capability:
        raise SystemExit(f"{module_id} capability mismatch")
    if module.get("repository")!=repository:
        raise SystemExit(f"{module_id} repository mismatch")
    if not str(module.get("site","")).startswith("https://jampeter.com.br/apps/"):
        raise SystemExit(f"{module_id} site missing")

if phases["schedule"]["repository"]!="jam2peter/github-agenda-sync":
    raise SystemExit("agenda sync integration missing")
if phases["quality"]["repository"]!="jam2peter/quality-gate":
    raise SystemExit("quality gate integration missing")
if phases["preserve"]["repository"]!="jam2peter/auto-checkpoint":
    raise SystemExit("auto checkpoint integration missing")

print("OPS_STACK_MANIFEST=PASS")
print("OPS_STACK_OBSERVE=AUDIT+MONITOR+ALERT")
