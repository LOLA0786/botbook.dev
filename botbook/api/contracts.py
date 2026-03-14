from fastapi import APIRouter
from ..contracts.engine import ContractEngine

router = APIRouter()
engine = ContractEngine()

@router.post("/contracts/create")
def create_contract(payer, worker, task, reward):

    c = engine.create(
        payer=payer,
        worker=worker,
        task=task,
        reward=reward
    )

    return c.__dict__
