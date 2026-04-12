import pytest
from django.urls import reverse
from apps.aliments.tests.factories import AlimentFactory
from apps.aliments.models import Aliment

import pytest
from django.urls import reverse
from apps.aliments.models import Aliment

pytestmark = pytest.mark.django_db


def test_list_view_status(staff_client, aliments):
    response = staff_client.get(reverse("aliments:list"))
    assert response.status_code == 200


def test_list_view_contains_data(staff_client, aliments):
    response = staff_client.get(reverse("aliments:list"))
    assert response.context["aliments"].count() == 3


def test_create_aliment_valid(admin_client, fournisseur):
    response = admin_client.post(
        reverse("aliments:create"),
        {
            "nom": "Test aliment",
            "code_alim": "TA001",
            "description": "desc",
            "fournisseur": fournisseur.id,
        },
    )

    assert response.status_code == 302
    assert Aliment.objects.filter(code_alim="TA001").exists()


def test_create_aliment_invalid(admin_client, fournisseur):
    response = admin_client.post(
        reverse("aliments:create"),
        {
            "nom": "",
            "code_alim": "TA002",
            "fournisseur": fournisseur.id,
        },
    )

    assert response.status_code == 200
    assert "nom" in response.context["form"].errors


def test_update_aliment(staff_client, aliment, fournisseur):
    response = staff_client.post(
        reverse("aliments:update", args=[aliment.id]),
        {
            "nom": "Updated",
            "code_alim": aliment.code_alim,
            "description": "updated",
            "fournisseur": fournisseur.id,
        },
    )

    assert response.status_code == 302


def test_delete_aliment(admin_client, aliment):
    response = admin_client.post(reverse("aliments:delete", args=[aliment.id]))

    assert response.status_code == 302
    assert not Aliment.objects.filter(id=aliment.id).exists()


def test_json_response(staff_client, aliments):
    response = staff_client.get(
        reverse("aliments:list_json"),
        HTTP_X_REQUESTED_WITH="XMLHttpRequest",
    )

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert "code_alim" in data[0]
    assert "nom" in data[0]
