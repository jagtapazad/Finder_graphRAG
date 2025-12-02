from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .api.routes import agents, feedback, routing
from .kg.client import close_driver, get_driver

app = FastAPI(title="Smart Agentic Router")


@app.on_event("startup")
def on_startup() -> None:
    # Ensure Neo4j driver is initialized
    get_driver()


@app.on_event("shutdown")
def on_shutdown() -> None:
    # Properly close Neo4j driver
    close_driver()


@app.get("/")
def root():
    """Root endpoint - redirects to API documentation"""
    return RedirectResponse(url="/docs")


app.include_router(routing.router, prefix="/routing", tags=["routing"])
app.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
app.include_router(agents.router, prefix="/agents", tags=["agents"])


