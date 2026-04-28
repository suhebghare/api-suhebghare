import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}


def _load(filename):
    if filename not in _cache:
        with open(os.path.join(BASE, filename)) as f:
            _cache[filename] = json.load(f)
    return _cache[filename]


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def _profile_section(key):
    return lambda: _response(200, _load("profile.json").get(key, {}))


def _blogs_by_category(category):
    articles = _load("blogs.json").get("blog", {}).get("articles", [])
    return _response(200, [a for a in articles if a.get("category", "").lower() == category.lower()])


ROUTES = {
    "/profile": lambda: _response(200, _load("profile.json")),
    "/blogs": lambda: _response(200, _load("blogs.json")),
    "/health": lambda: _response(200, {"status": "healthy"}),
    "/projects": _profile_section("projects"),
    "/skills": _profile_section("skills"),
    "/education": _profile_section("education"),
    "/contact": _profile_section("contact"),
    "/experience": _profile_section("experience"),
    "/certifications": _profile_section("certifications"),
    "/addresses": _profile_section("addresses"),
    "/languages": _profile_section("languages"),
    "/hobbies": _profile_section("hobbies"),
    "/blogs/kubernetes": lambda: _blogs_by_category("Kubernetes"),
    "/blogs/cicd": lambda: _blogs_by_category("CI/CD"),
    "/blogs/cloud": lambda: _blogs_by_category("Cloud"),
    "/blogs/security": lambda: _blogs_by_category("Security"),
    "/blogs/observability": lambda: _blogs_by_category("Observability"),
    "/blogs/ai": lambda: _blogs_by_category("AI & DevOps"),
}


def lambda_handler(event, context):
    path = event.get("path", "")
    try:
        handler = ROUTES.get(path)
        if handler:
            return handler()
        return _response(404, {"error": "Not found"})
    except Exception as e:
        return _response(500, {"error": str(e)})
