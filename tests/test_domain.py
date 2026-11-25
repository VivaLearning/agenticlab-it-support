from backend.domain import scenario, execute, verify

def test_approval_and_recovery():
    s=scenario("complex")
    assert execute("resolver","unlock",s)["status"]=="APPROVAL_REQUIRED"
    assert s["account_locked"]
    assert execute("resolver","unlock",s,True)["status"]=="SUCCESS"
    assert not verify(s)["login"]
    execute("resolver","refresh_session",s)
    assert verify(s)=={"login":True,"continuity":True}

def test_guardrails():
    s=scenario("governance")
    before=s.copy()
    assert execute("resolver","restart",s,True)["status"]=="DENIED"
    assert execute("planner","unlock",s,True)["status"]=="DENIED"
    assert s==before
    assert not verify(s)["login"]
