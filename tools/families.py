"""Familles de blocs : noms génériques, installables séparément par tenant."""
FAMILIES = {
    "site":     ("Site",      "fas fa-globe",          "Site vitrine, landing, présentation : menus, héros, sections, tarifs, avis, FAQ, pieds de page"),
    "app":      ("App",       "fas fa-th-large",       "Application web / bureau : coquille, tableaux de bord, listes, réglages, assistants"),
    "projet":   ("Projet",    "fas fa-tasks",          "Gestion de projet : tickets, tableau kanban, cycles, feuille de route, jalons, charge d'équipe"),
    "support":  ("Support",   "fas fa-headset",        "Relation client : boîte de conversations, fil de discussion, fiche contact, réponses types, satisfaction"),
    "mail":     ("Mail",      "fas fa-envelope-open-text", "Messagerie : boîte de réception, lecture d'un mail, rédaction, fil, pièces jointes, modèles"),
    "commerce": ("Commerce",  "fas fa-shopping-bag",   "Boutique : fiches produit, panier, paiement, commandes, suivi de livraison, avis"),
    "finance":  ("Finance",   "fas fa-wallet",         "Argent : portefeuille, cartes, transactions, factures, budgets, cours"),
    "donnees":  ("Données",   "fas fa-chart-pie",      "Graphiques et indicateurs : barres, courbes, anneaux, jauges, cartes de chaleur, entonnoirs, classements"),
    "agenda":   ("Agenda",    "fas fa-calendar-alt",   "Temps : calendrier, semaine, prise de rendez-vous, événements, frise chronologique"),
    "social":   ("Social",    "fas fa-users",          "Communauté : publications, fil d'actualité, profils, commentaires, réactions"),
    "contenu":  ("Contenu",   "fas fa-book-open",      "Écrits : article, documentation, base de connaissances, journal des versions, sommaire"),
    "media":    ("Média",     "fas fa-play-circle",    "Vidéo, musique, podcast, galeries, visionneuse"),
    "compte":   ("Compte",    "fas fa-user-shield",    "Connexion, inscription, double authentification, profil, abonnement, clés d'API, sécurité"),
    "equipe":   ("Équipe",    "fas fa-sitemap",        "Organigramme, annuaire, fiches membres, congés, recrutement"),
    "mobile":   ("Mobile",    "fas fa-mobile-alt",     "Écrans d'app mobile : barres, listes, feuilles, onglets, stories"),
    "outils":   ("Outil",     "fas fa-toolbox",        "Réglages de page, séparateurs, bascules, effets, utilitaires invisibles"),
    "insolite": ("Insolite",  "fas fa-hat-wizard",     "Blocs surprenants : terminal, billet, polaroid, post-it, platine vinyle, reçu, horloge…"),
}
ORDER = list(FAMILIES.keys())


def prefix(fam):
    return FAMILIES[fam][0] + " · "
