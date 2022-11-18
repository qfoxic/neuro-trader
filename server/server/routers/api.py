from enum import StrEnum

from fastapi import APIRouter, Query
from corelib.utils import cos_similarity_score, make_sample_from_array
from ..utils import load_trade_models


class OperationType(StrEnum):
    buy = "buy"
    sell = "sell"


router = APIRouter(
    prefix="/api/v1",
    tags=["match"]
)


@router.get("/match/{trade_op}")
async def match(trade_op: OperationType, pattern: str = Query(description="Comma separated close prices", min_length=4, max_length=300, regex='^[0-9.,]+$'),
                only_score: bool = True):
    models = load_trade_models(trade_op)
    tradePattern = make_sample_from_array([float(p) for p in pattern.split(',')])
    if only_score:
        return max([cos_similarity_score(tradePattern, model) for model in models.values()])
    return [{name: cos_similarity_score(tradePattern, model) for name, model in models.items()}]