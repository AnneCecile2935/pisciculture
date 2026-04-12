from django.test import TestCase
from apps.activite_quotidien.forms import NourrissageForm
from apps.activite_quotidien.tests.factories import NourrissageFactory
from apps.aliments.tests.factories import AlimentFactory
from apps.sites.tests.factories import BassinFactory


class NourrissageFormTest(TestCase):

    def setUp(self):
        self.nourrissage = NourrissageFactory()
        self.bassin = self.nourrissage.bassin
        self.aliment = AlimentFactory()

    # -------------------------
    # CAS VALIDE : aliment + qte
    # -------------------------
    def test_valid_aliment_qte(self):
        form = NourrissageForm(
            data={
                "bassin": self.bassin.id,
                "aliment": self.aliment.id,
                "qte": 5,
                "motif_absence": ""
            },
            bassin_id=self.bassin.id
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["aliment"].id, self.aliment.id)
        self.assertEqual(form.cleaned_data["qte"], 5)

    # -------------------------
    # CAS VALIDE : motif seul
    # -------------------------
    def test_valid_motif_only(self):
        form = NourrissageForm(
            data={
                "bassin": self.bassin.id,
                "aliment": "",
                "qte": "",
                "motif_absence": "vide"
            },
            bassin_id=self.bassin.id
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["qte"], 0)
        self.assertIsNone(form.cleaned_data["aliment"])
        self.assertEqual(form.cleaned_data["motif_absence"], "vide")

    # -------------------------
    # CAS INVALID : tout vide
    # -------------------------
    def test_invalid_empty(self):
        form = NourrissageForm(
            data={
                "bassin": self.bassin.id,
                "aliment": "",
                "qte": "",
                "motif_absence": ""
            },
            bassin_id=self.bassin.id
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    # -------------------------
    # CAS INVALID : aliment + motif
    # -------------------------
    def test_invalid_both(self):
        form = NourrissageForm(
            data={
                "bassin": self.bassin.id,
                "aliment": self.aliment.id,
                "qte": 5,
                "motif_absence": "vide"
            },
            bassin_id=self.bassin.id
        )

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    # -------------------------
    # CAS MÉTIER : aliment queryset global
    # -------------------------
    def test_aliment_queryset_is_global(self):
        form = NourrissageForm(bassin_id=self.bassin.id)
        self.assertEqual(
            form.fields["aliment"].queryset.model,
            AlimentFactory._meta.model
        )

    # -------------------------
    # CAS MÉTIER : dernier aliment initialisé
    # -------------------------
    def test_last_aliment_initial(self):
        form = NourrissageForm(bassin_id=self.bassin.id)
        self.assertEqual(form.fields["aliment"].initial, self.nourrissage.aliment)
