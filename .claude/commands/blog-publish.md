---
description: Publish post N — commit, squash-merge to main, verify deploy, sweep external links (phase 9). HARD gate.
argument-hint: "<post-number> [series-slug]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Publish a reviewed post. This pushes to `main` and triggers the live deploy, so it is a HARD
gate: present the full plan and get an explicit "publish" from Nikhil BEFORE any push.

1. Parse the post number from `$1`. Resolve the series from `$2` if given, else the most
   recently updated manifest. If post `$1` status is not `reviewed` (gate `G8_review`), tell
   the user to run /blog-review $1 first and stop.
2. Read the post `slug` and `title` from the manifest. Identify the files to publish: the
   post `_posts/YYYY-MM-DD-<slug>.md` and its `assets/img/posts/<slug>/` directory. Show
   Nikhil the exact `git status --short` for these paths and the list of external URLs the
   post contains (`grep -oE 'https?://[^) ]+' the post`).
3. **HARD GATE:** state plainly — "This will commit the post, squash-merge to `main`, push,
   and deploy live." Wait for an explicit yes. If anything else, stop.
4. On yes, confirm a clean start, then branch, commit ONLY the post + its assets (explicit
   paths, never `git add .`/`-A`):
   - `git checkout main && git pull --ff-only`
   - `git checkout -b post/<slug>`
   - `git add _posts/YYYY-MM-DD-<slug>.md assets/img/posts/<slug>` then commit
     `"post: <title>"` with the Co-Authored-By trailer.
5. Squash-merge to main and push:
   - `git checkout main`
   - `git merge --squash post/<slug>` then `git commit -m "post: <title>" -m "<trailer>"`
   - `git push origin main`
6. Verify the deploy: poll `gh run list --branch main --limit 5 --json databaseId,headSha,status,conclusion`
   for the run whose `headSha` matches the new main HEAD; wait until `status: completed` and
   confirm `conclusion: success`. If it fails, STOP and report — do not mark published.
7. **Post-publish external-link sweep:** for each external URL from step 2, run
   `curl -sS -o NUL -w "%{http_code}" -I -L <url>` (fall back to `-X GET` if HEAD is 405).
   Report any non-2xx/3xx. These do not block the build (html-proofer skips external), so
   they are a heads-up for Nikhil to fix in a follow-up, not a rollback trigger.
8. Update the manifest: post `status: published`, `gate: G9_published`, bump `updated`,
   append a `log` line. If every post in `posts[]` is now `published`, set
   `series_phase: done`. Delete the `post/<slug>` branch (`git branch -d`).
9. Report: the deploy run id + conclusion, the live URL
   (`/posts/<title-slug>/`), and the link-sweep results.
