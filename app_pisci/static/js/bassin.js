async function afficherSites() {
    const spinner = document.getElementById('loading-spinner');
    const container = document.getElementById('sites-container');
    container.style.display = 'none';  // Cache le conteneur au démarrage
    spinner.style.display = 'block';   // Affiche le spinner

    try {
        const response = await fetch('sites/api/bassins/');
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        const sites = await response.json();
        const siteSelect = document.getElementById('site-select');
        siteSelect.innerHTML = '<option value="">Tous les sites</option>';
        sites.forEach(site => {
            siteSelect.innerHTML += `<option value="${site.nom}">${site.nom}</option>`;
        });

        if (sites.length === 0) {
            container.innerHTML = '<div class="col-12 text-center"><p class="empty-message">Aucun site trouvé.</p></div>';
            return;
        }

        sites.forEach(site => {
            const siteCard = document.createElement('div');
            siteCard.className = 'col-md-6 mb-4';
            siteCard.innerHTML = `
                <div class="card site-card">
                    <div class="card-body text-center">
                        <h5 class="card-title">${site.nom}</h5>
                        <p class="card-text">${site.bassins.length} bassin(s) • Cliquez pour voir les détails</p>
                    </div>
                </div>
                <div class="row bassins-container" id="bassins-${site.nom.replace(/\s+/g, '-')}"></div>
            `;

            siteCard.addEventListener('click', () => {
                const bassinsContainer = document.getElementById(`bassins-${site.nom.replace(/\s+/g, '-')}`);
                bassinsContainer.style.display = bassinsContainer.style.display === 'none' ? 'flex' : 'none';
            });

            container.appendChild(siteCard);
            const bassinsRow = document.getElementById(`bassins-${site.nom.replace(/\s+/g, '-')}`);

            site.bassins.forEach(bassin => {
                const bassinCol = document.createElement('div');
                bassinCol.className = 'col-md-6 mb-3';
                const bassinCard = document.createElement('div');

                // Détermine la classe CSS en fonction de l'état du bassin
                let cardClass = 'card bassin-card ';
                let statusBadge = '';
                let statusMessage = '';

                if (!bassin.a_un_lot) {
                    cardClass += 'border-secondary';
                    statusBadge = '<span class="badge bg-secondary">Vide</span>';
                    statusMessage = 'Aucun lot affecté à ce bassin.';
                } else {
                    const dernierNourrissage = new Date(bassin.lot.dernier_nourrissage);
                    const aujourdHui = new Date();
                    const joursSansNourriture = Math.floor((aujourdHui - dernierNourrissage) / (1000 * 60 * 60 * 24));

                    if (joursSansNourriture > 2) {
                        cardClass += 'border-danger';
                        statusBadge = '<span class="badge bg-danger">À nourrir !</span>';
                        statusMessage = `Dernier nourrissage il y a ${joursSansNourriture} jours.`;
                    } else {
                        cardClass += 'border-success';
                        statusBadge = '<span class="badge bg-success">OK</span>';
                        statusMessage = `Nourri le ${bassin.lot.dernier_nourrissage}.`;
                    }
                }

                const tauxRemplissage = bassin.volume && bassin.lot ?
                    Math.round((bassin.lot.quantite / (bassin.volume * 1000)) * 100) : null;

                bassinCard.className = cardClass;
                bassinCard.innerHTML = `
                    <div class="card-body">
                        <h6 class="card-title d-flex justify-content-between">
                            ${bassin.nom}
                            ${statusBadge}
                        </h6>
                        <p class="card-text">
                            <i class="fas fa-water"></i> Volume: ${bassin.volume || 'N/A'} m³
                            ${tauxRemplissage ? ` • ${tauxRemplissage}% rempli` : ''}
                        </p>
                        <p class="card-text small text-muted">${statusMessage}</p>
                    </div>
                    ${bassin.a_un_lot ? `
                    <div class="bassin-detail">
                        <div class="lot-item">
                            <p class="mb-1">
                                <i class="fas fa-fish"></i> <strong>${bassin.lot.code}</strong>:
                                ${bassin.lot.quantite} ${bassin.lot.espece}
                                <span class="badge bg-primary">${bassin.lot.statut}</span>
                            </p>
                            <p class="mb-1">
                                Poids moyen: ${bassin.lot.poids_moyen ? bassin.lot.poids_moyen + 'g' : 'N/A'} |
                                Arrivé le: ${bassin.lot.date_arrivee}
                            </p>
                            <p class="mb-0">
                                Quantité: ${bassin.lot.quantite_actuelle}/${bassin.lot.quantite}
                            </p>
                        </div>
                    </div>
                    ` : `
                    <div class="bassin-detail">
                        <p class="empty-message text-center p-3">Ce bassin est vide.</p>
                    </div>
                    `}
                `;
                bassinCol.appendChild(bassinCard);
                bassinsRow.appendChild(bassinCol);
            });
        });
    } catch (error) {
        console.error("Erreur lors du chargement des bassins:", error);
        container.innerHTML = `
            <div class="col-12 text-center">
                <div class="alert alert-danger">
                    Erreur lors du chargement des données. Veuillez réessayer plus tard.
                </div>
            </div>
        `;
    } finally {
        spinner.style.display = 'none';
        container.style.display = 'block';
    }
}

// Charge les sites au démarrage
window.onload = afficherSites;
