from django.urls import reverse, resolve
from django.test import SimpleTestCase
from apps.especes.views import EspeceListView, EspeceCreateView, EspeceUpdateView, EspeceDeleteView
import uuid

class TestEspeceURLs(SimpleTestCase):
    def test_espece_list_url(self):
        """Teste que l'URL de la liste des espèces est correctement résolue."""
        url = reverse('especes:espece-list')
        self.assertEqual(url, '/especes/')
        self.assertEqual(resolve(url).func.view_class, EspeceListView)

    def test_espece_create_url(self):
        """Teste que l'URL de création d'une espèce est correctement résolue."""
        url = reverse('especes:espece-create')
        self.assertEqual(url, '/especes/create/')
        self.assertEqual(resolve(url).func.view_class, EspeceCreateView)

    def test_espece_update_url(self):
        """Teste que l'URL de mise à jour d'une espèce est correctement résolue."""
        test_uuid = uuid.uuid4()
        url = reverse('especes:espece-update', args=[test_uuid])
        self.assertEqual(url, f'/especes/{test_uuid}/update/')
        self.assertEqual(resolve(url).func.view_class, EspeceUpdateView)

    def test_espece_delete_url(self):
        """Teste que l'URL de suppression d'une espèce est correctement résolue."""
        test_uuid = uuid.uuid4()
        url = reverse('especes:espece-delete', args=[test_uuid])
        self.assertEqual(url, f'/especes/{test_uuid}/delete/')
        self.assertEqual(resolve(url).func.view_class, EspeceDeleteView)

    def test_espece_urls_app_name(self):
        """Teste que le namespace 'especes' est correctement utilisé."""
        url = reverse('especes:espece-list')
        resolved = resolve(url)
        self.assertEqual(resolved.app_name, 'especes')
        self.assertEqual(resolved.namespace, 'especes')
