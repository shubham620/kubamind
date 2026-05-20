"""
AI Agents endpoints
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def get_agents_status():
    """Get status of all AI agents"""
    return {
        "agents": [
            {
                "name": "cpu_agent",
                "status": "active",
                "last_analysis": "2024-01-15T10:30:00Z"
            },
            {
                "name": "memory_agent",
                "status": "active",
                "last_analysis": "2024-01-15T10:30:00Z"
            }
        ]
    }


@router.get("/{agent_name}/insights")
async def get_agent_insights(agent_name: str):
    """Get insights from a specific agent"""
    return {
        "agent": agent_name,
        "insights": []
    }


@router.post("/{agent_name}/trigger")
async def trigger_agent(agent_name: str):
    """Manually trigger an agent analysis"""
    return {
        "agent": agent_name,
        "status": "triggered"
    }
