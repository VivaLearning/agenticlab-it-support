import os, uuid, json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psycopg
from psycopg.types.json import Jsonb
from backend.domain import scenario, execute, verify, ALLOWED
from backend.llm import call

load_dotenv()
app=FastAPI(title="AgenticLab IT Support")
ROOT=Path(__file__).resolve().parents[1]

def db():
    return psycopg.connect(os.environ["DATABASE_URL"])

def event(c, r, kind, **data):
    e={"kind":kind, **data}
    r["trace"].append(e)
    c.execute("INSERT INTO lab_event(run_id,event) VALUES (%s,%s)",(r["id"],Jsonb(e)))

def save(c,r,s):
    c.execute("UPDATE lab_run SET state=%s WHERE id=%s",(Jsonb(r),r["id"]))
    c.execute("INSERT INTO lab_state VALUES (1,%s) ON CONFLICT(id) DO UPDATE SET state=excluded.state",(Jsonb(s),))

class Start(BaseModel):
    scenario: str="complex"
class Approval(BaseModel):
    approved: bool

@app.get("/")
def home():
    return FileResponse(ROOT/"frontend"/"index.html")

@app.post("/api/start")
def start(body:Start):
    try: s=scenario(body.scenario)
    except ValueError as e: raise HTTPException(400,str(e))
    r={"id":str(uuid.uuid4()),"role":"planner","status":"RUNNING","iteration":1,"tokens":0,
       "messages":[{"role":"user","content":"Ripristina accesso CRM senza interrompere gli altri utenti. Diagnostica e pianifica."}],
       "trace":[],"pending":None,"plan":"","evidence":[],"steps":0}
    with db() as c:
        c.execute("SELECT pg_advisory_xact_lock(600)")
        c.execute("UPDATE lab_run SET state=jsonb_set(state,'{status}','\"SUPERSEDED\"') WHERE state->>'status' IN ('RUNNING','APPROVAL_REQUIRED')")
        c.execute("INSERT INTO lab_run(id,state) VALUES (%s,%s)",(r["id"],Jsonb(r)))
        event(c,r,"MISSION",role="orchestrator",detail="Ripristinare accesso CRM; nessuna interruzione")
        save(c,r,s)
    return {"run":r,"environment":s}

def load(c,id):
    c.execute("SELECT pg_advisory_xact_lock(600)")
    row=c.execute("SELECT state FROM lab_run WHERE id=%s FOR UPDATE",(id,)).fetchone()
    if not row: raise HTTPException(404,"Mission not found")
    s=c.execute("SELECT state FROM lab_state WHERE id=1").fetchone()[0]
    return row[0],s

def switch(c,r,role,content):
    r["role"]=role
    r["messages"]=[{"role":"user","content":content}]
    event(c,r,"ROUTING",role=role,detail=content)

def observation(c,r,tool,call_id,result):
    r["messages"].append({"role":"tool","tool_call_id":call_id,"content":json.dumps(result)})
    r["evidence"].append({"role":r["role"],"tool":tool,"result":result})
    event(c,r,"TOOL_RESULT",role=r["role"],tool=tool,result=result)

@app.post("/api/run/{id}/step")
def step(id:uuid.UUID):
    with db() as c:
        r,s=load(c,id)
        if r["status"]!="RUNNING": return {"run":r,"environment":s}
        remaining=int(os.getenv("MAX_TOKENS","20000"))-r["tokens"]
        if remaining<=0 or r["steps"]>=30:
            r["status"]="LIMIT_REACHED"
        else:
            r["steps"]+=1
            role=r["role"]
            try:
                m,used=call(role,r["messages"],remaining)
            except Exception as e:
                r["status"]="ERROR"
                event(c,r,"ERROR",role=role,detail=type(e).__name__)
                save(c,r,s)
                return {"run":r,"environment":s}
            r["tokens"]+=used
            msg={"role":"assistant","content":m.get("content") or ""}
            calls=m.get("tool_calls") or []
            if calls: msg["tool_calls"]=[{"id":x["id"],"type":"function","function":x["function"]} for x in calls]
            r["messages"].append(msg)
            if calls:
                if len(calls)!=1:
                    r["status"]="ERROR"
                    event(c,r,"ERROR",role=role,detail="Expected one tool call")
                else:
                    t=calls[0]; name=t["function"]["name"]
                    event(c,r,"TOOL_CALL",role=role,tool=name)
                    if name=="unlock" and role=="resolver" and s["account_locked"]:
                        r["pending"]={"tool":name,"id":t["id"]}
                        r["status"]="APPROVAL_REQUIRED"
                        event(c,r,"APPROVAL",role=role,detail="Sbloccare account?")
                    else:
                        observation(c,r,name,t["id"],execute(role,name,s))
            else:
                detail=msg["content"]
                event(c,r,"AGENT_OUTPUT",role=role,detail=detail)
                if role=="planner":
                    r["plan"]=detail
                    switch(c,r,"resolver","Esegui il piano rispettando i vincoli: "+detail)
                elif role=="resolver":
                    r["verification_start"]=len(r["evidence"])
                    switch(c,r,"verifier","Verifica indipendentemente accesso e continuità. Intervento riferito: "+detail)
                else:
                    evidence=r["evidence"][r.get("verification_start",0):]
                    checked=any(x["role"]=="verifier" and x["tool"]=="verify" for x in evidence)
                    actual=verify(s)
                    if checked and all(actual.values()):
                        r["status"]="SUCCESS"
                    elif r["iteration"]>=3:
                        r["status"]="ESCALATED"
                    else:
                        r["iteration"]+=1
                        switch(c,r,"planner","Verifica fallita o mancante. Ripianifica usando queste evidenze: "+json.dumps(r["evidence"]))
        save(c,r,s)
        return {"run":r,"environment":s}

@app.post("/api/run/{id}/approval")
def approval(id:uuid.UUID,body:Approval):
    with db() as c:
        r,s=load(c,id)
        if r["status"]!="APPROVAL_REQUIRED" or not r["pending"]: raise HTTPException(409,"No pending approval")
        p=r["pending"]
        result=execute(r["role"],p["tool"],s,True) if body.approved else {"status":"DENIED","reason":"Human rejected"}
        observation(c,r,p["tool"],p["id"],result)
        r["pending"]=None
        r["status"]="RUNNING" if body.approved else "ESCALATED"
        save(c,r,s)
        return {"run":r,"environment":s}
