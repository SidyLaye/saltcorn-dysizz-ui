# Blocs en code

Chaque fichier `.html` de ce dossier devient un bloc de la Library du builder
(pour tous les tenants qui installent le kit), après :

```bash
python3 tools/build_packs.py && python3 tools/build_index.py
```

puis commit/push, mise à jour du module, et « Mettre à jour les blocs » sur `/dysizz-ui`.

Première ligne facultative :

```html
<!-- name: Web · Bandeau promo | icon: fas fa-bullhorn | wrap: section -->
```

- `name` : nom dans la Library (garde un préfixe « Web · », « App · »… pour le tri)
- `icon` : icône Font Awesome 5
- `wrap` : `none` (brut), `section` (section + conteneur centré), `full` (pleine largeur)

Le reste du fichier est le HTML du bloc. `<style>` et `<script>` sont permis.
Toutes les classes `dz-*` et attributs `data-dz-*` du kit fonctionnent.

Pour un bloc propre à un seul tenant, pas besoin de code : utilise l'atelier
`/dysizz-ui/blocks` dans ce tenant.
