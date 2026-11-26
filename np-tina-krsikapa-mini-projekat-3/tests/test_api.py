from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store() -> Iterator[None]:
    main._tasks.clear()
    yield
    main._tasks.clear()


def test_create_task_success() -> None:
    response = client.post("/tasks", json={"title": "Ucenje", "priority": 3})
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Ucenje"
    assert body["description"] == ""
    assert body["priority"] == 3


def test_get_existing_task() -> None:
    created = client.post("/tasks", json={"title": "Test"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_task_returns_404() -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404


@pytest.mark.parametrize("task_id", ["0", "-5", "abc"])
def test_get_task_invalid_id_returns_422(task_id: str) -> None:
    assert client.get(f"/tasks/{task_id}").status_code == 422


@pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": "   "}, {"title": 123}])
def test_create_task_invalid_title_returns_422(payload: dict[str, object]) -> None:
    assert client.post("/tasks", json=payload).status_code == 422


@pytest.mark.parametrize(
    ("length", "expected"),
    [(1, 201), (100, 201), (101, 422)],
)
def test_title_length_boundaries(length: int, expected: int) -> None:
    response = client.post("/tasks", json={"title": "a" * length})
    assert response.status_code == expected


@pytest.mark.parametrize(
    ("priority", "expected"),
    [(0, 422), (1, 201), (5, 201), (6, 422), ("high", 422)],
)
def test_priority_boundaries(priority: object, expected: int) -> None:
    response = client.post("/tasks", json={"title": "x", "priority": priority})
    assert response.status_code == expected


def test_description_too_long_returns_422() -> None:
    response = client.post("/tasks", json={"title": "x", "description": "d" * 501})
    assert response.status_code == 422


def test_title_is_trimmed() -> None:
    response = client.post("/tasks", json={"title": "  zadatak  "})
    assert response.json()["title"] == "zadatak"


def test_ids_are_incremental() -> None:
    first = client.post("/tasks", json={"title": "a"}).json()
    second = client.post("/tasks", json={"title": "b"}).json()
    assert (first["id"], second["id"]) == (1, 2)


def test_task_limit_returns_507(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(main, "MAX_TASKS", 2)
    assert client.post("/tasks", json={"title": "a"}).status_code == 201
    assert client.post("/tasks", json={"title": "b"}).status_code == 201
    assert client.post("/tasks", json={"title": "c"}).status_code == 507
