# Nikhil's Portfolio

Personal portfolio and blog built with [Jekyll](https://jekyllrb.com/) and the [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) theme. Hosted on GitHub Pages.

---

## Running locally

```bash
# Serve with live reload (default)
./tools/run.sh

# Custom host (e.g. to access from another device on the network)
./tools/run.sh -H 0.0.0.0

# Production build + html-proofer check
./tools/test.sh
```

The dev server runs at `http://127.0.0.1:4000` by default.

---

## Creating a new post

Use jekyll-compose to scaffold a post with the correct filename and front matter:

```bash
bundle exec jekyll post "My Post Title"
```

This creates a file in `_posts/` named `YYYY-MM-DD-my-post-title.md`.

### Front matter

```yaml
---
title: Title Here
date: YYYY-MM-DD HH:MM:SS +0530
categories: [CATEGORY, SUBCATEGORY]   # max 2 levels, one post = one category
tags: [tag1, tag2]                    # lowercase; topic/tool descriptors
math: true                            # add this if the post has LaTeX
---
```

Categories and subcategories grow organically as content is added — don't pre-define them.

---

## Deployment

Pushing to `main` triggers the GitHub Actions workflow at `.github/workflows/pages-deploy.yml`, which builds the site and deploys it to GitHub Pages automatically. You can also trigger a manual deploy from the Actions tab.

---

## Project layout

```
.
├── _posts/          # All blog posts (YYYY-MM-DD-title.md)
├── _tabs/           # Navigation pages (about, categories, tags, archives)
├── _config.yml      # Site-wide settings: URL, title, author, social links
├── _data/
│   ├── contact.yml  # Sidebar contact/social links
│   └── share.yml    # Share buttons on posts
├── assets/
│   ├── img/         # Images; posts use assets/img/posts/<slug>/
│   └── lib/         # Static assets submodule (Chirpy)
├── _layouts/        # Theme layout overrides (avoid editing unless necessary)
├── _includes/       # Theme partial overrides
├── _sass/           # Theme style overrides
└── tools/
    ├── run.sh       # Dev server wrapper
    └── test.sh      # Production build + proofer wrapper
```

---

## Useful links

- [Chirpy — Writing a new post](https://chirpy.cotes.page/posts/write-a-new-post/)
- [jekyll-compose](https://github.com/jekyll/jekyll-compose) — post scaffolding
- [GitHub Actions deploy](.github/workflows/pages-deploy.yml)
