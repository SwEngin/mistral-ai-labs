"""Fictional, read-only incident investigation tools."""

INCIDENTS = {
    "INC-1042": {
        "incident_id": "INC-1042",
        "service": "checkout-api",
        "started_at": "2026-11-12T10:15:00Z",
        "summary": "Elevated checkout errors reported by monitoring.",
        "root_cause": "Not confirmed",
    },
    "INC-1043": {
        "incident_id": "INC-1043",
        "service": "search-api",
        "started_at": "2026-11-12T11:00:00Z",
        "summary": "Search requests are intermittently timing out.",
        "root_cause": "Not confirmed",
    },
}

HEALTH = {
    "checkout-api": {
        "service": "checkout-api",
        "health": "degraded",
        "observation": "Elevated HTTP 500 error rate.",
        "observed_at": "2026-11-12T10:25:00Z",
    }
}

DEPLOYMENTS = {
    "checkout-api": [
        {
            "version": "2.8.0",
            "deployed_at": "2026-11-12T10:05:00Z",
            "change": "Updated checkout request validation.",
        }
    ],
    "search-api": [],
}


def get_incident_details(incident_id: str) -> dict:
    incident = INCIDENTS.get(incident_id)
    if incident is None:
        return {"error": "Incident not found", "incident_id": incident_id}
    return dict(incident)


def get_service_health(service_name: str) -> dict:
    if service_name == "search-api":
        return {"error": "Health data unavailable", "service": service_name}
    health = HEALTH.get(service_name)
    if health is None:
        return {"error": "Service not found", "service": service_name}
    return dict(health)


def get_recent_deployments(service_name: str) -> dict:
    if service_name not in DEPLOYMENTS:
        return {"error": "Service not found", "service": service_name}
    return {
        "service": service_name,
        "deployments": [dict(deployment) for deployment in DEPLOYMENTS[service_name]],
    }
