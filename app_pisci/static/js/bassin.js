async function afficherSites() {
    const spinner = document.getElementById('loading-spinner');
    const container = document.getElementById('sites-container');
    container.style.display = 'none';
    spinner.style.display = 'block';

    try {
        const response = await fetch('/api/bassins/');
        if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
        const sites = await response.json();
        const siteSelect = document.getElementById('site-select');
        siteSelect.innerHTML = '<option value="">Tous les sites</option>';

        sites.forEach(site => {
            siteSelect.innerHTML += `<option value="${site.id}">${site.nom}</option>`;

            // Filtrer les bassins par préfixe pour ce site
            const bassinsK = site.bassins.filter(bassin => bassin.nom.startsWith('K'));
            const bassinsT = site.bassins.filter(bassin => bassin.nom.startsWith('T'));
            const bassinsB = site.bassins.filter(bassin => bassin.nom.startsWith('B'));

            const siteCard = document.createElement('div');
            siteCard.className = 'col-md-12 mb-4 site-container';
            siteCard.id = `site-${site.id}`;

            // Fonction pour regrouper les bassins par ligne (similaire à votre filtre Django)
            function groupByLine(bassins, prefix) {
                const groups = {
                    'K': [[], [], [], [], []], // K1-K4, K5-K8, K9-K10, K11-K12, K13-K14
                    'T': [[], []],            // T1-T4, T5-T8 (adaptez selon vos besoins)
                    'B': [[], []]             // B1-B4, B5-B6
                };

                bassins.forEach(bassin => {
                    const num = parseInt(bassin.nom.substring(1));
                    if (prefix === 'K') {
                        if (num >= 1 && num <= 4) groups['K'][0].push(bassin);
                        else if (num >= 5 && num <= 8) groups['K'][1].push(bassin);
                        else if (num >= 9 && num <= 10) groups['K'][2].push(bassin);
                        else if (num >= 11 && num <= 12) groups['K'][3].push(bassin);
                        else if (num >= 13 && num <= 14) groups['K'][4].push(bassin);
                    } else if (prefix === 'T') {
                        if (num >= 1 && num <= 4) groups['T'][0].push(bassin);
                        else if (num >= 5 && num <= 8) groups['T'][1].push(bassin);
                    } else if (prefix === 'B') {
                        if (num >= 1 && num <= 4) groups['B'][0].push(bassin);
                        else if (num >= 5 && num <= 6) groups['B'][1].push(bassin);
                    }
                });

                return groups[prefix];
            }

            // Générer le HTML pour les bassins K
            let bassinsKHTML = '';
            const groupesK = groupByLine(bassinsK, 'K');
            groupesK.forEach((ligne, index) => {
                if (ligne.length > 0) {
                    bassinsKHTML += `
                        <div class="pond-line">
                            ${ligne.map(bassin => `
                                <div class="bassin-card" data-bassin-id="${bassin.id}" onclick="showBassinDetails('${bassin.id}')"
                                     style="background-color: ${bassin.a_un_lot ? (bassin.lot.a_jeun ? '#000000' :
                                                                                         !bassin.lot.dernier_nourrissage ? '#dc3545' :
                                                                                         bassin.lot.nourrissages_today === 2 ? '#28a745' : '#ffa500') : '#6c757d'}">
                                    <div class="pond-name">${bassin.nom}</div>
                                    ${bassin.a_un_lot ? `
                                        <div class="pond-lot">${bassin.lot.quantite_actuelle}<br>${bassin.lot.poids_moyen || 0} kg</div>
                                        <span class="badge bg-light text-dark">${bassin.lot.get_statut_display || '-'}</span>
                                    ` : '<div class="pond-lot">Vide</div>'}
                                </div>
                            `).join('')}
                        </div>
                    `;
                }
            });

            // Générer le HTML pour les bassins T
            let bassinsTHTMl = '';
            const groupesT = groupByLine(bassinsT, 'T');
            groupesT.forEach((ligne, index) => {
                if (ligne.length > 0) {
                    bassinsTHTMl += `
                        <div class="pond-line">
                            ${ligne.map(bassin => `
                                <div class="bassin-card" data-bassin-id="${bassin.id}" onclick="showBassinDetails('${bassin.id}')"
                                     style="background-color: ${bassin.a_un_lot ? (bassin.lot.a_jeun ? '#000000' :
                                                                                         !bassin.lot.dernier_nourrissage ? '#dc3545' :
                                                                                         bassin.lot.nourrissages_today === 2 ? '#28a745' : '#ffa500') : '#6c757d'}">
                                    <div class="pond-name">${bassin.nom}</div>
                                    ${bassin.a_un_lot ? `
                                        <div class="pond-lot">${bassin.lot.quantite_actuelle}<br>${bassin.lot.poids_moyen || 0} kg</div>
                                        <span class="badge bg-light text-dark">${bassin.lot.get_statut_display || '-'}</span>
                                    ` : '<div class="pond-lot">Vide</div>'}
                                </div>
                            `).join('')}
                        </div>
                    `;
                }
            });

            // Générer le HTML pour les bassins B
            let bassinsBHTML = '';
            const groupesB = groupByLine(bassinsB, 'B');
            groupesB.forEach((ligne, index) => {
                if (ligne.length > 0) {
                    bassinsBHTML += `
                        <div class="pond-line">
                            ${ligne.map(bassin => `
                                <div class="bassin-card" data-bassin-id="${bassin.id}" onclick="showBassinDetails('${bassin.id}')"
                                     style="background-color: ${bassin.a_un_lot ? (bassin.lot.motif_absence === 'JEUN' ? '#000000' :
                                                                                         !bassin.lot.dernier_nourrissage ? '#dc3545' :
                                                                                         bassin.lot.nourrissages_today === 2 ? '#28a745' : '#ffa500') : '#6c757d'}">
                                    <div class="pond-name">${bassin.nom}</div>
                                    ${bassin.a_un_lot ? `
                                        <div class="pond-lot">${bassin.lot.quantite_actuelle}<br>${bassin.lot.poids_moyen || 0} kg</div>
                                        <span class="badge bg-light text-dark">${bassin.lot.get_statut_display || '-'}</span>
                                    ` : '<div class="pond-lot">Vide</div>'}
                                </div>
                            `).join('')}
                        </div>
                    `;
                }
            });

            // Assembler le HTML du site
            siteCard.innerHTML = `
                <div class="card site-card mb-3">
                    <div class="card-body text-center">
                        <h5 class="card-title">${site.nom}</h5>
                        <p class="card-text">${site.bassins.length} bassin(s)</p>
                    </div>
                </div>
                <div class="ponds-container">
                    ${bassinsK.length > 0 ? `
                        <div class="ponds-column">
                            <h4 class="section-title">Bassins de production</h4>
                            ${bassinsKHTML}
                        </div>
                    ` : ''}
                    ${bassinsT.length > 0 ? `
                        <div class="ponds-column">
                            <h4 class="section-title">Bassins de production</h4>
                            ${bassinsTHTMl}
                        </div>
                    ` : ''}
                    ${bassinsB.length > 0 ? `
                        <div class="ponds-column">
                            <h4 class="section-title">Bassins Alevinage</h4>
                            ${bassinsBHTML}
                        </div>
                    ` : ''}
                </div>
            `;

            container.appendChild(siteCard);
        });
    } catch (error) {
        console.error("Erreur:", error);
        container.innerHTML = `<div class="alert alert-danger">Erreur lors du chargement des données.</div>`;
    } finally {
        spinner.style.display = 'none';
        container.style.display = 'block';
    }
}

// Fonction pour afficher les détails d'un bassin
function showBassinDetails(bassinId) {
    const spinner = document.getElementById('loading-spinner');
    spinner.style.display = 'block';  // Affiche le spinner de chargement

    // Appelle l'API Django pour récupérer les détails du lot
    fetch(`/sites/bassin/${bassinId}/lot/`)
        .then(response => response.json())
        .then(data => {
            spinner.style.display = 'none';  // Cache le spinner

            // Génère la liste des repas (ou un message si vide)
            let repasList = data.derniers_repas && data.derniers_repas.length > 0
                ? data.derniers_repas.map(repas =>
                    `<li>${repas.date} : ${repas.quantite} kg de ${repas.type_aliment}</li>`
                ).join('')
                : '<li>Aucun repas enregistré.</li>';

            // Construit le contenu de la modale
            let content = `
                <p><strong>Bassin:</strong> ${data.bassin_nom || 'N/A'}</p>
                <p><strong>Site:</strong> ${data.site_nom || 'N/A'}</p>
                <hr>
                ${data.code_lot ? `
                    <p><strong>Code lot:</strong> ${data.code_lot}</p>
                    <p><strong>Espèce:</strong> ${data.espece || 'N/A'}</p>
                    <p><strong>Quantité actuelle:</strong> ${data.quantite_actuelle || '0'}</p>
                    <p><strong>Poids moyen:</strong> ${data.poids_moyen ? data.poids_moyen + ' g' : 'N/A'}</p>
                    <p><strong>Poids total:</strong> ${data.poids_total ? data.poids_total + ' kg' : 'N/A'}</p>
                    <p><strong>Date d'arrivée:</strong> ${data.date_arrivee || 'N/A'}</p>
                    <h5>Derniers repas :</h5>
                    <ul>${repasList}</ul>
                ` : `
                    <p class="empty-message">Ce bassin est vide.</p>
                `}

                <div class="mt-3 d-flex gap-2">
                    <a href="/nourrissage/enregistrer-repas/${data.site_id}/" class="btn btn-primary btn-sm">Enregistrer un repas</a>
                </div>
            `;

            // Injecte le contenu dans la modale et l'affiche
            document.getElementById('bassinDetailsContent').innerHTML = content;
            const modal = new bootstrap.Modal(document.getElementById('bassinDetailsModal'));
            modal.show();
        })
        .catch(error => {
            spinner.style.display = 'none';  // Cache le spinner en cas d'erreur
            console.error('Erreur:', error);
            alert("Une erreur est survenue lors du chargement des détails.");
        });
}

// Fonction pour filtrer par site
function filtrerParSite(siteId) {
    document.querySelectorAll('.site-container').forEach(container => {
        container.style.display = 'none';
    });
    if (siteId) {
        document.getElementById(`site-${siteId}`).style.display = 'block';
    } else {
        document.querySelectorAll('.site-container').forEach(container => {
            container.style.display = 'block';
        });
    }
}

// Charge les sites au démarrage
window.onload = afficherSites;
