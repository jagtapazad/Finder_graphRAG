from fastapi import APIRouter

from ...kg.queries import get_agents_by_task_type

router = APIRouter()


@router.get("/")
def list_agents(task_type: str | None = None) -> list[dict]:
    if not task_type:
        # For now, require a task_type; you can extend this to list all agents later.
        return []
    agents = get_agents_by_task_type(task_type)
    return [a.__dict__ for a in agents]


