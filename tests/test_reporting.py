from backend.reporting import summarize
from backend.domain import scenario, execute

def test_report_distinguishes_crm_outage_and_no_additional_disruption():
    s=scenario("governance")
    r={"status":"ESCALATED","iteration":3,"steps":25,"tokens":100,"initial_environment":s.copy(),
       "trace":[{"kind":"LLM_RESPONSE","role":"planner","tokens":40},{"kind":"LLM_RESPONSE","role":"verifier","tokens":60},
                {"kind":"ROUTING","to_agent":"planner"},{"kind":"HUMAN_DECISION","approved":True},
                {"kind":"TOOL_RESULT","tool":"restart","result":{"status":"DENIED"}},
                {"kind":"TERMINATION","detail":"Limite iterazioni"}]}
    m=summarize(r,s)
    assert m["criteria"]=={"login":False,"no_additional_disruptions":True,"crm_online":False}
    assert m["tokens_by_agent"]=={"planner":40,"resolver":0,"verifier":60}
    assert m["replans"]==1 and m["approvals"]==1 and m["denied_tools"]==["restart"]
    assert m["termination_reason"]=="Limite iterazioni"

def test_report_keeps_before_and_after_distinct():
    s=scenario("complex")
    r={"status":"SUCCESS","iteration":1,"steps":3,"tokens":0,"initial_environment":s.copy(),"trace":[]}
    execute("resolver","unlock",s,True)
    execute("resolver","refresh_session",s)
    m=summarize(r,s)
    assert m["initial"]["account_locked"] and not m["current"]["account_locked"]
    assert m["criteria"]["login"] and m["criteria"]["no_additional_disruptions"]
