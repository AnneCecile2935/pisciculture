from django.urls import reverse, resolve
from django.test import SimpleTestCase
from apps.fournisseurs.views import (
    FournisseurListView, FournisseurCreateView,
    FournisseurUpdateView, FournisseurDeleteView
)
import uuid

class TestFournisseurURLs(SimpleTestCase):
    def test_fournisseur_list_url(self):
        """Teste que l'URL de la liste des fournisseurs est correctement résolue."""
        url = reverse('fournisseurs:fournisseur-list')
        self.assertEqual(url, '/fournisseurs/')
        self.assertEqual(resolve(url).func.view_class, FournisseurListView)

    def test_fournisseur_create_url(self):
        """Teste que l'URL de création d'un fournisseur est correctement résolue."""
        url = reverse('fournisseurs:fournisseur-create')
        self.assertEqual(url, '/fournisseurs/create/')
        self.assertEqual(resolve(url).func.view_class, FournisseurCreateView)

    def test_fournisseur_update_url(self):
        """Teste que l'URL de mise à jour d'un fournisseur est correctement résolue."""
        test_uuid = uuid.uuid4()
        url = reverse('fournisseurs:fournisseur-update', args=[test_uuid])
        self.assertEqual(url, f'/fournisseurs/{test_uuid}/update/')
        self.assertEqual(resolve(url).func.view_class, FournisseurUpdateView)

    def test_fournisseur_delete_url(self):
        """Teste que l'URL de suppression d'un fournisseur est correctement résolue."""
        test_uuid = uuid.uuid4()
        url = reverse('fournisseurs:fournisseur-delete', args=[test_uuid])
        self.assertEqual(url, f'/fournisseurs/{test_uuid}/delete/')
        self.assertEqual(resolve(url).func.view_class, FournisseurDeleteView)
