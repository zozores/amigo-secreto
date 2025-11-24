from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
import models
import database
import logic
import os

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY")) # In prod, use env var
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") # Simple password

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        request.session["user"] = "admin"
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Senha incorreta"})

@app.get("/logout")
def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
        
    participants = db.query(models.Participant).all()
    return templates.TemplateResponse("admin.html", {"request": request, "participants": participants})

@app.post("/participants")
def add_participant(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
        
    if not name.strip():
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    participant = models.Participant(name=name.strip())
    db.add(participant)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/draw")
def draw(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
        
    participants = db.query(models.Participant).all()
    if len(participants) < 2:
        return RedirectResponse(url="/", status_code=303)
    
    try:
        logic.perform_draw(participants)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error during draw: {e}")
        
    return RedirectResponse(url="/", status_code=303)

@app.post("/reset")
def reset(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("user"):
        return RedirectResponse(url="/login", status_code=303)
        
    db.query(models.Participant).delete()
    db.commit()
    return RedirectResponse(url="/", status_code=303)

@app.get("/reveal/{token}", response_class=HTMLResponse)
def reveal(token: str, request: Request, db: Session = Depends(get_db)):
    participant = db.query(models.Participant).filter(models.Participant.token == token).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    if not participant.match_id:
        return templates.TemplateResponse("base.html", {
            "request": request, 
            "content": "<div class='p-4 text-center'>O sorteio ainda não foi realizado!</div>"
        }) # Simplified error view
        
    match = db.query(models.Participant).filter(models.Participant.id == participant.match_id).first()
    
    return templates.TemplateResponse("reveal.html", {
        "request": request, 
        "participant": participant, 
        "match": match
    })
