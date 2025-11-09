from django import template

register = template.Library()

@register.filter
def bassin_number(value):
    """Extrait le numéro d'un bassin (ex: 'K1' -> 1)."""
    if not value:
        return 0
    return int(value[1:])

@register.filter
def group_by_line(bassins, prefix):
    """Regroupe les bassins par ligne selon leur préfixe (K ou B) et leur numéro."""
    groups = {
        'K': {1: [], 2: [], 3: [], 4: [], 5: []},  # K1-K4, K5-K8, K9-K10, K11-K12, K13-K14
        'B': {1: [], 2: []},  # B1-B4, B5-B6
        'T': {1: [], 2: []},
        'D': {1: [], 2: []}
    }
    for bassin in bassins:
        if bassin.nom.startswith(prefix):
            try:
                num = int(bassin.nom[1:])
            except (ValueError, IndexError):
                continue  # Ignore les noms mal formatés
            if prefix == 'K':
                if 1 <= num <= 4:
                    groups['K'][1].append(bassin)
                elif 5 <= num <= 8:
                    groups['K'][2].append(bassin)
                elif 9 <= num <= 10:
                    groups['K'][3].append(bassin)
                elif 11 <= num <= 12:
                    groups['K'][4].append(bassin)
                elif 13 <= num <= 14:
                    groups['K'][5].append(bassin)
            elif prefix == 'B':
                if 1 <= num <= 4:
                    groups['B'][1].append(bassin)
                elif 5 <= num <= 6:
                    groups['B'][2].append(bassin)
            elif prefix == 'T':
                if 1 <= num <= 4:
                    groups['T'][1].append(bassin)
                elif 5 <= num <= 8:
                    groups['T'][2].append(bassin)
            elif prefix == 'D':
                if 1 <= num <= 3:
                    groups['D'][1].append(bassin)
                elif 4 <= num <= 5:
                    groups['D'][2].append(bassin)
    return groups
