from django.core.management.base import BaseCommand
from apps.activite_quotidien.models import Nourrissage

class Command(BaseCommand):
    help = "Remplit les champs redondants pour les nourrissages existants."

    def handle(self, *args, **options):
        for nourrissage in Nourrissage.objects.all():
            if nourrissage.site_prod:
                nourrissage.site_prod_nom = nourrissage.site_prod.nom
            if nourrissage.bassin:
                nourrissage.bassin_nom = nourrissage.bassin.nom
            if nourrissage.crea_lot:
                nourrissage.crea_lot_code = getattr(nourrissage.crea_lot, 'code_lot', f"LOT-{nourrissage.crea_lot.id}")
            if nourrissage.aliment:
                nourrissage.aliment_nom = nourrissage.aliment.nom
            if nourrissage.cree_par:
                nourrissage.cree_par_nom = nourrissage.cree_par.get_username()
            nourrissage.save()  # Appelle save() pour déclencher la logique
        self.stdout.write(self.style.SUCCESS("Noms backfillés pour tous les nourrissages !"))
