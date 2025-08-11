from fastapi import FastAPI, Request
from database import Base, engine
import users, operators, transaction_types, transactions, auth_utils_routes
from seed import seed_super_admin
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShamaMoney")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # ou ["*"] pour autoriser toutes les origines (pas recommandé en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
