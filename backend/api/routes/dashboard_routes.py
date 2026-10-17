
from typing import List

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
)

from api.models.response_models import (
    DashboardStats,
    HistoryItem,
)

from database.db_queries import (
    get_history,
    get_stats,
    delete_analysis,
    clear_history,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/stats",
    response_model=DashboardStats,
)
def dashboard_stats():
    return get_stats()


@router.get(
    "/history",
    response_model=List[HistoryItem],
)
def dashboard_history(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    )
):
    return get_history(limit)


@router.delete("/history/{analysis_id}")
def remove_history_item(analysis_id: int):
    deleted = delete_analysis(analysis_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return {
        "message": "Analysis deleted successfully."
    }


@router.delete("/history")
def remove_all_history():
    clear_history()

    return {
        "message": "Match history cleared successfully."
    }
