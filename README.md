# GÜDLFT - Plateforme de Réservation de Compétitions

Bienvenue sur le projet **GÜDLFT Registration Portal**, une application Flask légère permettant aux secrétaires de clubs d'inscrire leurs athlètes à des compétitions régionales et locales en utilisant les points accumulés par leur club.

Ce projet s'inscrit dans le cadre de la consolidation du POC (Proof of Concept), de la correction des anomalies de la Phase 1, de l'implémentation des fonctionnalités de la Phase 2, de la refonte visuelle complète de l'interface, ainsi que de la mise en place d'une suite de tests automatisés et de tests de performance.

---

## Sommaire

1. [Technologies et Outils](#technologies-et-outils)
2. [Installation et Démarrage](#installation-et-démarrage)
3. [Architecture et Organisation des Branches](#architecture-et-organisation-des-branches)
4. [Détail des Bogues Corrigés et Fonctionnalités](#détail-des-bogues-corrigés-et-fonctionnalités)
5. [Refonte de l'Interface Utilisateur (UI/UX)](#refonte-de-linterface-utilisateur-uiux)
6. [Suite de Tests et Couverture de Code](#suite-de-tests-et-couverture-de-code)
7. [Tests de Performance (Locust)](#tests-de-performance-locust)
8. [Qualité du Code (Flake8 / PEP8)](#qualité-du-code-flake8--pep8)

---

## 1. Technologies et Outils

- **Python** (v3.10+)
- **Flask** : Micro-framework web
- **pytest** : Framework de tests automatisés
- **pytest-cov / Coverage** : Analyse et rapport de couverture de code
- **Locust** : Outil de test de charge et de performance
- **Flake8** : Linter et vérification du respect des normes PEP8
- **HTML5 & CSS3** : Design responsive sur mesure (Vanilla CSS)

---

## 2. Installation et Démarrage

### 2.1 Cloner le dépôt forké
```bash
git clone https://github.com/seryelisee20-arch/projet-debogage-.git
cd projet-debogage-
```

### 2.2 Créer et activer l'environnement virtuel

- **Sous Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Si l'exécution de scripts est restreinte, exécutez au préalable : `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **Sous Linux / macOS :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2.4 Lancer l'application Flask
```bash
python -m flask --app server run
```
L'application est ensuite accessible dans votre navigateur à l'adresse suivante : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 3. Architecture et Organisation des Branches

Conformément au guide de développement, chaque bogue, amélioration ou fonctionnalité a fait l'objet d'une branche dédiée respectant la nomenclature `<type>/<nom-descriptif>`, validée par des tests avant intégration dans la branche principale `main` :

| Nom de la Branche | Type | Description |
|---|---|---|
| `bug/fix-login-unknown-email` | Bugfix | Gestion propre des emails inconnus (message flash, évite le plantage `IndexError`) |
| `bug/deduct-points-from-club` | Bugfix | Déduction effective des points du club lors de la réservation (1 place = 1 point) |
| `bug/prevent-booking-more-than-club-points` | Bugfix | Interdiction de réserver plus de places que le solde de points disponible |
| `bug/limit-booking-to-12-places` | Bugfix | Limite stricte de 12 places par club et par compétition (y compris cumulées) |
| `bug/prevent-booking-more-than-capacity` | Bugfix | Interdiction de réserver plus de places que la capacité restante |
| `bug/prevent-booking-past-competitions` | Bugfix | Blocage des réservations sur les compétitions passées |
| `bug/validate-booking-input-numbers` | Bugfix | Validation stricte des saisies (entiers positifs uniquement, refus des négatifs ou textes) |
| `bug/handle-competition-full` | Bugfix | Gestion explicite et blocage des réservations pour les concours complets |
| `feature/public-points-display-board` | Feature | Phase 2 : route `/points` et tableau public en lecture seule sans connexion |
| `feature/complete-redesign-ui` | Feature | Refonte moderne, responsive et élégante de toutes les vues (`static/css/style.css`) |
| `feature/test-suite-and-coverage` | Feature | Suite complète de tests (unitaires, intégration, fonctionnels) atteignant 100% de couverture |
| `feature/locust-performance-tests` | Feature | Tests de charge Locust et scénarios de performance (<5s chargement, <2s mise à jour) |
| `documentation/update-readme` | Docs | Rédaction complète de la documentation technique et explicative |
| `qa` | QA | Branche de révision finale créée à partir de `main` |

---

## 4. Détail des Bogues Corrigés et Fonctionnalités

### 4.1 Connexion avec email inconnu (`bug/fix-login-unknown-email`)
- **Problème initial :** Saisir un email non répertorié dans `clubs.json` provoquait une exception non interceptée `IndexError: list index out of range` et un crash HTTP 500.
- **Correction :** Vérification de l'existence du club, affichage d'un message flash explicite (*"Sorry, that email was not found."*) et redirection propre vers la page d'accueil avec un code HTTP 401.

### 4.2 Déduction des points du club (`bug/deduct-points-from-club`)
- **Problème initial :** Lors de l'achat de places, le nombre de places de la compétition diminuait, mais le solde de points du club n'était jamais débité.
- **Correction :** Les points du club sont déduits à raison de 1 point par place réservée (`club['points'] = str(club_points - placesRequired)`).

### 4.3 Interdiction de sur-consommation de points (`bug/prevent-booking-more-than-club-points`)
- **Problème initial :** Un club pouvait réserver plus de places qu'il n'avait de points, amenant son solde en négatif.
- **Correction :** Vérification que `placesRequired <= club_points`. En cas de dépassement, la réservation est rejetée avec un message flash (*"You do not have enough points to book these places."*).

### 4.4 Plafond strict de 12 places par club (`bug/limit-booking-to-12-places`)
- **Problème initial :** Les clubs pouvaient inscrire un nombre illimité d'athlètes à une même compétition.
- **Correction :** Suivi en temps réel des réservations (`bookings_tracker`). Un club ne peut pas acheter plus de 12 places en une seule fois, ni dépasser 12 places au cumul de réservations successives.

### 4.5 Respect de la capacité des compétitions (`bug/prevent-booking-more-than-capacity`)
- **Problème initial :** Un club pouvait commander un nombre supérieur de places à ce qu'il restait de disponible dans la compétition.
- **Correction :** Validation que `placesRequired <= competition_places`.

### 4.6 Interdiction de réservation sur événements passés (`bug/prevent-booking-past-competitions`)
- **Problème initial :** L'application permettait d'ouvrir la page de réservation et de réserver des places pour des événements dont la date était révolue.
- **Correction :** Fonction utilitaire `is_competition_past()` analysant la date ISO. Sur la page d'accueil du secrétaire, les événements passés sont clairement indiqués *(Event finished)* sans lien de réservation, et toute tentative d'accès direct par URL est interceptée.

### 4.7 Validation rigoureuse des données saisies (`bug/validate-booking-input-numbers`)
- **Problème initial :** La saisie d'un nombre négatif, de 0, de texte ou d'une valeur vide provoquait soit des comportements anormaux (crédit de places), soit un crash `ValueError`.
- **Correction :** Validation stricte par bloc `try/except` et contrôle `placesRequired > 0`. Ajout d'attributs HTML5 `min="1" max="12" required`.

### 4.8 Gestion des concours complets (`bug/handle-competition-full`)
- **Correction :** Lorsqu'une compétition n'a plus de places disponibles (`numberOfPlaces == 0`), elle est étiquetée comme *Full*, et toute tentative de réservation affiche un message d'erreur explicite.

### 4.9 Tableau d'affichage public des points (`feature/public-points-display-board`)
- **Spécification Phase 2 :** Mise à disposition d'une page publique en lecture seule des points de tous les clubs, accessible sans aucune connexion requise.
- **Implémentation :** Route `/points` (et redirection `/clubs`), affichant un tableau récapitulatif complet accessible directement depuis la barre de navigation et la page d'accueil.

---

## 5. Refonte de l'Interface Utilisateur (UI/UX)

Une refonte graphique complète a été réalisée sur la branche `feature/complete-redesign-ui` :
- **Design System Vanilla CSS** (`static/css/style.css`) :
  - Palette moderne : Slate profond (`#0f172a`), touches d'accentuation bleu cyan (`#0284c7`, `#0ea5e9`), fonds cartes blancs nets et ombrages doux.
  - Typographie premium : Intégration des polices *Plus Jakarta Sans* et *Outfit*.
  - Badges de statut visuels : *Places restantes*, *Complet*, *Événement terminé*.
  - Composants cartes pour chaque compétition et formulaire centré ergonomique.
  - Messages Flash stylisés avec animations et indicateurs colorés clairs (succès / erreur).
  - Navigation responsive avec en-tête fixe, lien direct vers le tableau d'affichage public et déconnexion sécurisée.

---

## 6. Suite de Tests et Couverture de Code

Conformément aux recommandations du guide de développement, les tests sont scrupuleusement hiérarchisés et séparés dans des répertoires distincts :

```
tests/
├── conftest.py                     # Fixture Flask test client et isolation des données
├── unit/                           # Tests unitaires ciblés (plus de 2x plus nombreux)
│   ├── test_login.py
│   ├── test_points.py
│   ├── test_booking.py
│   └── test_competitions.py
├── integration/                    # Tests des flux complets
│   ├── test_booking_integration.py # Flux complet connexion -> réservation -> déconnexion
│   └── test_points_integration.py  # Mise à jour du tableau public après réservation
└── functional/                     # Tests de parcours utilisateur et navigation globale
    ├── test_navigation.py
    └── test_error_handling.py
```

### 6.1 Lancer l'ensemble des tests
```bash
pytest
```

### 6.2 Lancer les tests avec le rapport de couverture
```bash
pytest --cov=server --cov-report=term-missing
```

### 6.3 Générer le rapport HTML de couverture
```bash
pytest --cov=server --cov-report=html
```
*(Le rapport est généré dans le dossier `htmlcov/index.html`)*.

> **Résultat de la couverture de tests :**
> - **Fichiers testés :** `server.py`
> - **Nombre de tests automatisés :** 24 tests
> - **Taux de couverture atteint :** **100%** (bien au-delà de l'objectif minimal de 60%).

---

## 7. Tests de Performance (Locust)

Conformément aux exigences de la Phase 2 et du guide de performance :
- **Nombre d'utilisateurs simulés :** 6 utilisateurs simultanés
- **Seuils de performance exigés :**
  - Récupération des pages et compétitions : **< 5 secondes**
  - Mise à jour des points et réservation : **< 2 secondes**

Le fichier `locustfile.py` modélise les comportements réels d'un secrétaire de club (consultation de l'accueil, connexion, affichage du tableau des points, consultation d'un concours et réservation de places).

### 7.1 Lancer le test de performance en mode headless (terminal)
Assurez-vous que l'application tourne dans un premier terminal (`python server.py`), puis lancez dans un second terminal :
```bash
locust --headless -u 6 -r 2 -t 15s --host=http://127.0.0.1:5000
```

### 7.2 Lancer l'interface web interactive Locust
```bash
locust -f locustfile.py --host=http://127.0.0.1:5000
```
Ouvrez ensuite [http://localhost:8089](http://localhost:8089) dans votre navigateur pour visualiser les graphiques en direct.

---

## 8. Qualité du Code (Flake8 / PEP8)

Le code source a été validé avec `flake8` pour garantir le respect strict des conventions PEP8 :
```bash
flake8 --exclude=venv,.git,__pycache__ --max-line-length=120
```
Le résultat s'exécute avec **0 erreur et 0 avertissement**.
