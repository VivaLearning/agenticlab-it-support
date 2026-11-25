"""Deterministic, evidence-based reporting for the training dashboard."""
from backend.domain import verify

ROLES = ("planner", "resolver", "verifier")

def summarize(run, environment):
    trace = run.get("trace", [])
    calls = [e for e in trace if e["kind"] == "LLM_RESPONSE"]
    results = [e for e in trace if e["kind"] == "TOOL_RESULT"]
    terminal = next((e for e in reversed(trace) if e["kind"] == "TERMINATION"), None)
    return {
        "status": run["status"],
        "scenario": run.get("scenario"),
        "iteration": run["iteration"],
        "steps": run["steps"],
        "tokens": run["tokens"],
        "tokens_by_agent": {role: sum(e.get("tokens", 0) for e in calls if e.get("role") == role) for role in ROLES},
        "llm_calls": len(calls),
        "tool_calls": sum(e["kind"] == "TOOL_CALL" for e in trace),
        "replans": sum(e["kind"] == "ROUTING" and e.get("to_agent") == "planner" for e in trace),
        "approvals": sum(e["kind"] == "HUMAN_DECISION" and e.get("approved") is True for e in trace),
        "rejections": sum(e["kind"] == "HUMAN_DECISION" and e.get("approved") is False for e in trace),
        "denied_tools": [e["tool"] for e in results if e.get("result", {}).get("status") == "DENIED"],
        "interventions": [e["tool"] for e in results if e.get("tool") in ("unlock", "refresh_session", "restart") and e.get("result", {}).get("status") == "SUCCESS"],
        "initial": run.get("initial_environment"),
        "current": environment.copy(),
        "criteria": {"login": verify(environment)["login"], "no_additional_disruptions": verify(environment)["continuity"], "crm_online": environment["crm_online"]},
        "termination_reason": terminal.get("detail") if terminal else None,
    }
