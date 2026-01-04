# Nikhil’s Portfolio

This repo contains the source code for my personal portfolio website. The site hosts my projects, blogs, paper summaries, and notes, all organized using **category**, **subcategory**, and **tags**.

## Content model

All content lives as posts, differentiated primarily by **category** → **subcategory** → **tags**.

### Categories (top-level type)

Current categories:

- **project**  
  End‑to‑end builds and case studies where I design, implement, and (ideally) deploy an AI/ML solution.

- **blog**  
  Longer, structured posts: explanations, deep dives, tutorials, and opinion pieces about ML, LLMs, MLOps, and related topics.

- **paper-summary**  
  Concise breakdowns of individual research papers: motivation, key ideas, method, results, and my takeaways.

- **note**  
  Short “Today I Learned”–style posts: debugging tricks, infra/MLOps gotchas, small insights, and quick experiments.

- **miscellaneous**  
  Posts that don’t fit the above buckets (meta notes, announcements, and other experiments).

Each post has exactly **one category**.

### Subcategories (topic bucket within a category)

Subcategories refine the category by area or type of work.

Examples:

- Under `project`:
  - `llm-systems` – LLM‑centric systems (e.g., financial advisor LLM, KG QA).
  - `mlops-infra` – Deployment, CI/CD, monitoring, and infra experiments.
  - `computer-vision` – CV projects and older hackathon work.  
  - `experiments` – Smaller or exploratory projects.

- Under `blog`:
  - `theory` – Conceptual/theoretical posts and derivations.  
  - `practical-guides` – Step‑by‑step tutorials and how‑tos.  
  - `career` – Reflections on learning, transitions, and work.

- Under `paper-summary`:
  - `llm`  
  - `peft`  
  - `knowledge-graphs`  
  - `reinforcement-learning`

- Under `note`:
  - `debugging`  
  - `infra-gotchas`  
  - `tiny-insights`

Subcategories are optional but recommended; each post should have at most **one** subcategory.

### Tags (fine-grained descriptors)

Tags describe **what** the post involves: methods, tools, topics, or patterns.

Examples (non‑exhaustive):

- Topics: `llm`, `nlp`, `knowledge-graphs`, `reinforcement-learning`, `streaming`, `optimization`.
- Methods / ideas: `qlora`, `adapters`, `lora`, `dora`, `parameter-efficient-finetuning`, `multi-hop`.
- Infra / tooling: `mlops`, `azure`, `azureml`, `pytorch`, `pytorch-lightning`, `docker`, `github-actions`, `mlflow`, `bytewax`, `qdrant`, `langchain`, `beam`.
- Meta: `learning-notes`, `reflection`, `career`

Guidelines:
- One **category**, zero or one **subcategory**, and multiple **tags** per post.
- Do not use category names as tags (avoid `project`, `blog` as tags).

***

## Site structure

The site is organized into the following main sections:

- **Home** – Recent posts across all categories with clear labels.  
- **Categories** – All categories (and optionally subcategories) with descriptions and post lists.
- **Tags** – All tags with links to filtered views.
- **Archives** – Chronological list of all posts by year/month.  
- **About** – Bio, experience, skills, and links to selected projects.

***

## Post front‑matter conventions

```yaml
---
title: TITLE
date: YYYY-MM-DD HH:MM:SS +/-TTTT
categories: [TOP_CATEGORY, SUB_CATEGORY]
tags: [TAG]     # TAG names should always be lowercase
---
```

***

## Category guidelines

- **project**
  - Clear problem, approach, and outcome.
  - Includes architecture, methods, tools, and lessons learned.

- **blog**
  - Explains a concept, tells a story, or teaches something in depth.
  - More polished and structured than a note.

- **paper-summary**
  - Focused on a single paper.
  - Includes citation, core idea, method, results, and commentary.

- **note**
  - Short, focused, usually written in one sitting.
  - Often “how I fixed X” or “one insight about Y”.

- **miscellaneous**
  - Use sparingly; if a theme repeats, promote it to a real category.

***

## Subcategory guidelines

- Each subcategory should group posts that feel related in theme or shape.
- Prefer reusing existing subcategories over creating near‑duplicates.
- If a subcategory has only one post for a long time, consider merging or renaming.

***

## Tagging guidelines

- Prefer **specific**, reusable tags over very generic ones.
- Include:
  - At least one **topic** tag (e.g., `llm`, `mlops`, `knowledge-graphs`).
  - At least one **tool/tech** tag (e.g., `pytorch`, `azure`, `mlflow`).
- Avoid:
  - Duplicating category/subcategory names as tags.
  - Super generic tags like `code`, `random`, `stuff`.

***

## Project post checklist

For **project** posts, try to include:

- Problem and motivation  
- High‑level architecture and design decisions  
- Datasets and methods  
- Tools/infra (cloud, frameworks, MLOps pieces)
- Results, limitations, and next steps  
- Links to code, demos, and related notes/paper summaries

***

## Paper-summary template

Suggested sections:

1. Motivation  
2. Problem definition  
3. Key idea  
4. Method (high‑level)  
5. Results (high‑level)  
6. My takeaways / how it connects to my projects

***

## Note template

Keep Notes lightweight:

- One clear title  
- 1–3 paragraphs or a short list  
- Concrete code snippet, config, or command if relevant  
- Optional: links to related project/blog/paper‑summary posts

***

## Internal bookmarks (for my reference)
- [Adding a new post](https://chirpy.cotes.page/posts/write-a-new-post/)
- [Plugin to add new content](https://github.com/jekyll/jekyll-compose)
