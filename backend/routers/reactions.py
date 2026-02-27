"""
Reactions are handled inline on the articles router (/articles/{id}/react).
This module is kept for future standalone reaction endpoints.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/reactions", tags=["reactions"])
