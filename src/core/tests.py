import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import Role
from core.models import Resource 

@pytest.mark.django_db
def test_healthz(client):
    resp = client.get("/healthz/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

@pytest.mark.django_db
def test_resource_crud_with_roles():
    User = get_user_model()

    # Ensure roles exist
    admin_role, _ = Role.objects.get_or_create(name="admin")
    creator_role, _ = Role.objects.get_or_create(name="creator")

    # Create user and give them the creator role
    u = User.objects.create_user(username="alice", password="pw")
    u.roles.add(creator_role)

    client = APIClient()
    # Instead of client.login(...), force auth directly
    client.force_authenticate(user=u)

    # CREATE
    r = client.post("/resources/", {"title": "Test", "data": {"x": 1}}, format="json")
    assert r.status_code == 201, r.content
    rid = r.json()["id"]

    # LIST (user should only see their own)
    r = client.get("/resources/")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["results"][0]["id"] == rid

    # UPDATE (owner can update)
    r = client.patch(f"/resources/{rid}/", {"title": "Updated"}, format="json")
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

@pytest.mark.django_db
def test_resource_creation_requires_auth():
    client = APIClient()

    #No authentication at all

    r = client.post("/resources/", {'title': 'Anon', 'data': {"x": 1}}, format="json")

    # DRF should reject this as unauthorized
    assert r.status_code == 401 # Unauthorized
    
@pytest.mark.django_db
def test_resource_creation_requires_creator_or_admin_role():
    User = get_user_model()

    # Make sure roles exist

    creator_role, _ = Role.objects.get_or_create(name="creator")
    admin_role, _ = Role.objects.get_or_create(name="admin")

    # user with no roles

    u = User.objects.create_user(username="bob", password="pw")

    client = APIClient()
    client.force_authenticate(user=u)

    
    r = client.post("/resources/", {"title": "Should Fail", "data": {"x": 1}}, format="json")

    # Authenticated but missing required role -> Forbidden
    assert r.status_code == 403

@pytest.mark.django_db
def test_admin_sees_all_resources():
    User = get_user_model()
    admin_role, _ = Role.objects.get_or_create(name="admin")
    creator_role, _ = Role.objects.get_or_create(name="creator")

    # Admin user
    admin = User.objects.create_user(username="admin_user", password="pw")
    admin.roles.add(admin_role)

    # Creator user
    creator = User.objects.create_user(username="creator_user", password="pw")
    creator.roles.add(creator_role)

    # Create resources owned by each
    r1 = Resource.objects.create(owner=admin, title="Admin's resource", data={"a": 1})
    r2 = Resource.objects.create(owner=creator, title="Creator's resource", data={"b": 2})

    client = APIClient()

    # Admin should see both resources
    client.force_authenticate(user=admin)
    r = client.get("/resources/")
    assert r.status_code == 200
    body = r.json()
    ids = {res["id"] for res in body["results"]}
    assert r1.id in ids
    assert r2.id in ids

    # Creator should see ONLY their own
    client.force_authenticate(user=creator)
    r = client.get("/resources/")
    assert r.status_code == 200
    body = r.json()
    ids = {res["id"] for res in body["results"]}
    assert r2.id in ids
    assert r1.id not in ids

