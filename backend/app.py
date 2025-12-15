from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .api.routes import agents, explanations, feedback, metrics, routing, visualization
from .kg.client import close_driver, get_driver

app = FastAPI(title="Smart Agentic Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    get_driver()


@app.on_event("shutdown")
def on_shutdown() -> None:
    close_driver()


@app.get("/")
def root():
    return RedirectResponse(url="/docs")


app.include_router(routing.router, prefix="/routing", tags=["routing"])
app.include_router(explanations.router, prefix="/explanations", tags=["explanations"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])
app.include_router(visualization.router, prefix="/visualization", tags=["visualization"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])


