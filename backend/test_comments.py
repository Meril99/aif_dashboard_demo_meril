from fastapi.testclient import TestClient
from immudb.client import ImmudbClient
import os

from main_api import app


# -------------------------
# immudb test client
# -------------------------
def get_immudb_client():
    host = os.getenv("IMMUDB_HOST", "immudb")
    port = os.getenv("IMMUDB_PORT", "3322")

    ic = ImmudbClient(f"{host}:{port}")
    ic.login(
        os.getenv("IMMUDB_USER", "immudb"),
        os.getenv("IMMUDB_PASSWORD", "immudb"),
    )
    ic.useDatabase(b"auditdb")
    return ic


# -------------------------
# ADD
# -------------------------
def test_add_comment_creates_immudb_audit():
    payload = {
        "Name": "test-user",
        "TimeStamp": "2026-01-26T12:00:00",
        "Comments": "hello immudb",
    }

    with TestClient(app) as client:
        response = client.post("/comments/", json=payload)
        assert response.status_code == 200
        comment = response.json()

    ic = get_immudb_client()

    result = ic.sqlQuery(
        """
        SELECT action, entity, entity_id
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment["id"]},
    )

    rows = list(result)
    assert len(rows) >= 1

    action, entity, entity_id = rows[0]
    assert action == "ADD"
    assert entity == "Comments"
    assert entity_id == comment["id"]


# -------------------------
# EDIT
# -------------------------
def test_edit_comment_creates_immudb_audit():
    with TestClient(app) as client:
        payload = {
            "Name": "edit-user",
            "TimeStamp": "2026-01-26T12:10:00",
            "Comments": "before edit",
        }

        create_resp = client.post("/comments/", json=payload)
        comment = create_resp.json()
        comment_id = comment["id"]

        updated = {
            "Name": "edit-user",
            "TimeStamp": "2026-01-26T12:20:00",
            "Comments": "after edit",
        }

        resp = client.put(f"/comments/{comment_id}/", json=updated)
        assert resp.status_code == 200

    ic = get_immudb_client()

    result = ic.sqlQuery(
        """
        SELECT action
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment_id},
    )

    rows = list(result)
    assert len(rows) >= 1
    (action,) = rows[0]
    assert action == "EDIT"


# -------------------------
# DELETE
# -------------------------
def test_delete_comment_creates_immudb_audit():
    with TestClient(app) as client:
        payload = {
            "Name": "delete-user",
            "TimeStamp": "2026-01-26T12:30:00",
            "Comments": "to be deleted",
        }

        create_resp = client.post("/comments/", json=payload)
        comment = create_resp.json()
        comment_id = comment["id"]

        delete_resp = client.delete(f"/comments/{comment_id}/")
        assert delete_resp.status_code == 200

    ic = get_immudb_client()

    result = ic.sqlQuery(
        """
        SELECT action
        FROM comments_audit_v2
        WHERE entity_id = @entity_id
        ORDER BY tx_id DESC
        """,
        {"entity_id": comment_id},
    )

    rows = list(result)
    assert len(rows) >= 1
    (action,) = rows[0]
    assert action == "DELETE"


def test_fetch_all_immudb_audit_logs():
    """
    This test validates that all audit logs can be fetched
    in reverse chronological order (latest first).

    This is the exact logic the future backend endpoint will use.
    """

    # Create 2 comments → generates 2 audit rows (ADD)
    with TestClient(app) as client:
        for i in range(2):
            payload = {
                "Name": f"user-{i}",
                "TimeStamp": "2026-01-26T12:00:00",
                "Comments": f"log {i}",
            }
            resp = client.post("/comments/", json=payload)
            assert resp.status_code == 200

    ic = get_immudb_client()

    # Fetch ALL audit logs
    result = ic.sqlQuery(
        """
        SELECT
            tx_id,
            action,
            entity,
            entity_id,
            payload,
            created_at
        FROM comments_audit_v2
        ORDER BY tx_id DESC
        """
    )

    rows = list(result)
    assert len(rows) >= 2

    # Validate row structure
    tx_id, action, entity, entity_id, payload, created_at = rows[0]

    assert isinstance(tx_id, int)
    assert action in {"ADD", "EDIT", "DELETE"}
    assert entity == "Comments"
    assert isinstance(entity_id, int)
    assert isinstance(payload, str)
    assert isinstance(created_at, int)

    # Ordering guarantee: newest first
    assert rows[0][0] > rows[1][0]
