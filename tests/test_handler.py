import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.handler import lambda_handler


def _event(path):
    return {"path": path}


def _call(path):
    res = lambda_handler(_event(path), None)
    return res["statusCode"], json.loads(res["body"]), res["headers"]


# --- Core endpoints ---

def test_profile():
    status, body, _ = _call("/profile")
    assert status == 200
    assert "meta" in body


def test_blogs():
    status, body, _ = _call("/blogs")
    assert status == 200
    assert "blog" in body


def test_health():
    status, body, _ = _call("/health")
    assert status == 200
    assert body == {"status": "healthy"}


# --- Profile sub-endpoints ---

def test_projects():
    status, body, _ = _call("/projects")
    assert status == 200
    assert isinstance(body, list)
    assert len(body) > 0


def test_skills():
    status, body, _ = _call("/skills")
    assert status == 200
    assert "cloud" in body


def test_education():
    status, body, _ = _call("/education")
    assert status == 200
    assert isinstance(body, list)


def test_contact():
    status, body, _ = _call("/contact")
    assert status == 200
    assert "email" in body


def test_experience():
    status, body, _ = _call("/experience")
    assert status == 200
    assert isinstance(body, list)
    assert len(body) > 0


def test_certifications():
    status, body, _ = _call("/certifications")
    assert status == 200
    assert isinstance(body, list)


def test_addresses():
    status, body, _ = _call("/addresses")
    assert status == 200
    assert "present" in body and "permanent" in body


def test_languages():
    status, body, _ = _call("/languages")
    assert status == 200
    assert "English" in body and "Hindi" in body and "Marathi" in body


def test_hobbies():
    status, body, _ = _call("/hobbies")
    assert status == 200
    assert "Cricket" in body


# --- Blog category endpoints ---

def test_blogs_kubernetes():
    status, body, _ = _call("/blogs/kubernetes")
    assert status == 200
    assert isinstance(body, list)
    assert all(a["category"] == "Kubernetes" for a in body)


def test_blogs_cicd():
    status, body, _ = _call("/blogs/cicd")
    assert status == 200
    assert isinstance(body, list)
    assert all(a["category"] == "CI/CD" for a in body)


def test_blogs_cloud():
    status, body, _ = _call("/blogs/cloud")
    assert status == 200
    assert isinstance(body, list)


def test_blogs_security():
    status, body, _ = _call("/blogs/security")
    assert status == 200
    assert isinstance(body, list)


def test_blogs_observability():
    status, body, _ = _call("/blogs/observability")
    assert status == 200
    assert isinstance(body, list)


def test_blogs_ai():
    status, body, _ = _call("/blogs/ai")
    assert status == 200
    assert isinstance(body, list)
    assert all(a["category"] == "AI & DevOps" for a in body)


# --- Error handling & headers ---

def test_not_found():
    status, body, _ = _call("/unknown")
    assert status == 404


def test_cors_headers():
    _, _, headers = _call("/health")
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert headers["Content-Type"] == "application/json"
