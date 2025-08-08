from fastapi import FastAPI, Request
from database import Base, engine
import users, operators, transaction_types, transactions, auth_utils_routes
from seed import seed_super_admin
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile Money API")
# Servir les fichiers statiques (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Dossier des templates HTML
templates = Jinja2Templates(directory="frontend/templates")


# Routers
app.include_router(auth_utils_routes.router)
app.include_router(users.router)
app.include_router(operators.router)
app.include_router(transaction_types.router)
app.include_router(transactions.router)

# Seed super admin
seed_super_admin()

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
