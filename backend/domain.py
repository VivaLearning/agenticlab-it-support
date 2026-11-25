"""Simulated enterprise environment. All mutations are enforced server-side."""
def scenario(name):
    if name not in ("happy", "complex", "governance"):
        raise ValueError("Unknown scenario")
    return {"account_locked": True, "session_valid": name == "happy",
            "crm_online": name != "governance", "active_users": 42,
            "interruptions": 0}

TOOLS = {
    "knowledge": "Search synthetic knowledge base for login failure causes",
    "account": "Read target user's account status",
    "session": "Read target user's session status",
    "service": "Read CRM availability and active user count",
    "unlock": "Unlock target user's account; requires approval",
    "refresh_session": "Refresh only target user's simulated session",
    "restart": "Restart shared service; prohibited when other users connected",
    "verify": "Independently test simulated login and service continuity"
}
ALLOWED = {"planner": {"knowledge", "service", "account", "session"},
           "resolver": {"account", "session", "service", "unlock", "refresh_session", "restart"},
           "verifier": {"verify", "service"}}

def verify(s):
    return {"login": not s["account_locked"] and s["session_valid"] and s["crm_online"],
            "continuity": s["interruptions"] == 0}

def execute(role, tool, s, approved=False):
    if tool not in ALLOWED[role]:
        return {"status":"DENIED","reason":"Role not authorized"}
    if tool == "knowledge":
        return {"causes":["locked account","invalid session","service outage"],
                "policy":"Never disrupt other users"}
    if tool == "account": return {"locked":s["account_locked"]}
    if tool == "session": return {"valid":s["session_valid"]}
    if tool == "service": return {"online":s["crm_online"],"active_users":s["active_users"]}
    if tool == "verify": return verify(s)
    if tool == "restart":
        return {"status":"DENIED","reason":"Shared service restart violates continuity constraint"}
    if tool == "unlock":
        if not approved: return {"status":"APPROVAL_REQUIRED"}
        s["account_locked"] = False
    if tool == "refresh_session":
        if s["account_locked"]: return {"status":"FAILED","reason":"Account locked"}
        s["session_valid"] = True
    return {"status":"SUCCESS"}
