---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

I'm Nikhil, an AI & ML engineer focused on **LLMOps and MLOps**. I build ML systems that actually hold up in production: RAG pipelines with retrieval evaluation baked in, CI quality gates that catch regressions before they ship, observability that traces a request from prompt to response.

I spent three years at **Microsoft** as an ML & DS Consultant on large Azure delivery portfolios before switching to engineering. That time changed how I think about ML systems. I pay as much attention to latency SLAs, cost-per-request, and failure traceability as I do to benchmark numbers. At some point, the gap between scoping the problems and building the solutions got too frustrating. I went back to school (**Rice University, MS CS**) and made the switch.

This site is where I write up what I build, the technical decisions behind it, and what I'd do differently next time.

---

## 📄 Publications

**SWiM: A New Dataset and Performance Benchmark for Real-time Spacecraft Segmentation in Onboard Computers** · [arXiv:2507.10775](https://arxiv.org/abs/2507.10775)
_Co-lead author · D2K Lab / NASA · 2024_

64K annotated images and the **first standardized benchmark** for real-time instance segmentation on embedded orbital hardware.

---

## 💼 Experience

### 🔷 Verizon Communications · AI & ML Engineer
📍 Houston, TX &nbsp;|&nbsp; 🗓️ Jan 2025 – Jan 2026

- Built **SQL transformation pipelines** against Verizon's enterprise data warehouse, resolving cross-schema timestamp misalignments and structuring raw telemetry into model-ready feature sets at 12M+ device scale.
- Fixed a production deployment blocked by a **6x SLA breach**: SHAP runtime was 90 min against a 15-min requirement. After exhausting parallelization and hardware scaling, built a Saabas approximation engine that brought it to 3 min (5x SLA headroom), enabling real-time diagnostics across the full fleet.
- Validated the approximation with Jaccard Similarity against SHAP's top-3 feature attributions across router entries, confirming zero accuracy cost before shipping.

---

### 🔬 D2K Lab / NASA Research Collaboration · AI Research Volunteer
📍 Houston, TX &nbsp;|&nbsp; 🗓️ May 2024 – Dec 2024

- Built the **SWiM benchmark**: 64K annotated instance segmentation images with simulated orbital conditions (glare, aurora, varied lighting) using NASA's TTALOS pipeline and Stable Diffusion.
- Fine-tuned YOLOv8/v11 to **0.92 Dice score** with inference at ~443ms, within the sub-950ms flight constraint on a 4-core/4GB spacecraft computer.
- Co-lead author on [arXiv:2507.10775](https://arxiv.org/abs/2507.10775). First standardized evaluation framework for real-time spacecraft segmentation on embedded orbital hardware.

---

### 🏢 Microsoft · ML & DS Consultant (Data & AI)
📍 Hyderabad, India &nbsp;|&nbsp; 🗓️ Aug 2020 – Jul 2023

- Rebuilt KPI reporting for **multi-million-dollar Azure delivery portfolios**: replaced ad-hoc reporting with a bi-weekly metrics-driven review cadence that improved revenue forecast accuracy from 40% to 70% and correctly projected ~$600K in previously misforecast revenue per cycle.
- Ran statistical root-cause analysis on delivery KPIs and partnered with engineering leads on recovery plans, mitigating 4-6 at-risk projects per quarter and protecting an estimated $1M-$2M in at-risk revenue quarterly.
- Built automated **Power BI portfolio dashboards** that eliminated ~15 hrs/week of manual tracking and cut anomaly detection from days to near real-time.

---

### 🧪 Indian Servers · Machine Learning Engineer Intern
📍 Vijayawada, India &nbsp;|&nbsp; 🗓️ Jan 2019 – Jun 2020

- Fine-tuned a **deep CNN for SAR image segmentation**, improving oil seep detection accuracy by 30%.
- Built full **ML deployment pipelines** (GitHub Actions, MLflow, Docker, Azure ML), replacing manual release processes and cutting model release cycles from days to hours.
