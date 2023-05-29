import sys

from fastapi import APIRouter

router = APIRouter()

@router.get('/info')
async def info_handler():
    return {
        'api': 'v1',
        'python': sys.version_info
    }

@router.get('/{action}')
async def action_handler(action):
    return {
        'action': action
    }

@router.get('/filter')
async def filter_handler(param1, param2, param3):
    return {
        'action': 'filter',
        'param1': param1,
        'param2': param2,
        'param3': param3
    }
