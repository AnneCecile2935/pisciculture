from django.test import TestCase
from django.urls import reverse
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.aliments.tests.factories import AlimentFactory
from apps.activite_quotidien.models import Nourrissage
from apps.users.tests.factories import UserFactory


class NourrissageParSiteViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

        self.site = SiteFactory()

        self.bassin1 = BassinFactory(site=self.site)
        self.bassin2 = BassinFactory(site=self.site)

        self.aliment = AlimentFactory()

        self.url = reverse(
            "activite_quotidien:enregistrer-repas-par-site",
            args=[self.site.id]
        )

    # -------------------------
    # GET OK
    # -------------------------
    def test_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")

    # -------------------------
    # POST VALID => bulk_create
    # -------------------------
    def test_post_valid(self):
        data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "2",

            "form-0-bassin": self.bassin1.id,
            "form-0-aliment": self.aliment.id,
            "form-0-qte": 10,
            "form-0-motif_absence": "",

            "form-1-bassin": self.bassin2.id,
            "form-1-aliment": "",
            "form-1-qte": "",
            "form-1-motif_absence": "vide",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Nourrissage.objects.count(), 2)

    # -------------------------
    # POST INVALID => rien créé
    # -------------------------
    def test_post_invalid(self):
        data = {
            "form-INITIAL_FORMS": "0",
            "form-TOTAL_FORMS": "1",

            "form-0-bassin": self.bassin1.id,
            "form-0-aliment": "",
            "form-0-qte": "",
            "form-0-motif_absence": "",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(Nourrissage.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
