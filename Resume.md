# Nikhil Chigali

+1 (713) 498-2302 | nikhil.chigali@gmail.com | linkedin.com/in/nikhil-chigali | github.com/nikhilchigali


## Education

**Rice University**
Aug 2023 - Dec 2024
Master's, Computer Science | GPA: **3.64**

**Jawaharlal Nehru University of Technology**
Jul 2016 - Sep 2020
Bachelor's, Computer Science | GPA: **8.43**

## Projects & Outside Experience

### Research Paper Enterprise RAG Pipeline

- Built a hybrid RAG ingestion pipeline for research papers using Unstructured.io's VLM cloud API, Claude Sonnet for table enrichment, and contextual chunking. Raw PDFs are processed into retrieval-ready chunks, each carrying a structured paper > section > subsection prefix, LaTeX-rendered equations, and HTML-formatted tables. This addresses the noise and context-loss problems that make naive PDF chunking unreliable for dense technical content.
- Designed a hybrid retrieval architecture combining dense semantic search (OpenAI's text-embedding-3-small, 1536-dim) with BM25 sparse vectors in a Pinecone serverless index, followed by a cross-encoder re-ranker (Cohere Re-rank) to rescore chunks by query relevance. This improves precision on acronym-heavy and terminology-dense research content, where pure vector search alone falls short.
- Added citation enforcement and hallucination gating at the generation layer. GPT-4 calls are configured so the system declines to answer when retrieved chunks do not support a response, rather than generating plausible but unsupported text.
- Built an LLMOps evaluation layer using Ragas with a golden dataset of ~50 manually verified QA pairs, measuring Faithfulness, Answer Relevancy, and Context Precision on every run. The evaluation script runs in CI, so any change to prompts, retrieval, or model config that drops quality below a set threshold fails the build.

### LLMOps Observability for Production RAG

- Instrumented the full RAG pipeline with request tracing using Langfuse, capturing retrieved chunk identities, reranker reordering decisions, versioned prompts, LLM responses, and per-request token consumption. Retrieval failures, ranking errors, and generation issues are traceable to their exact origin instead of surfacing as vague "the AI gave a bad answer" reports.
- Set up SRE-style quality monitoring tracking P50/P95 latency, cost-per-request, citation coverage rate, and failure rate across live traffic. A dashboard surfaces which pipeline stage is responsible when citation coverage drops or latency spikes, cutting mean-time-to-diagnosis from hours of log-digging to minutes.
- Integrated regression gating into the CI pipeline, blocking deployments when Faithfulness or Context Precision drops below defined thresholds. All prompts and config files are versioned alongside code so prompt changes are tracked, reviewable, and rollback-capable like any other artifact.

### Agentic AI SMS Conversion System (Flowise POC)

- Built an agentic AI SMS messaging system using Flowise and LangChain, coordinating four agents (Qualification, Scheduling, Re-engagement, Supervisor/Router) with defined tool boundaries and stateful handoffs. Agents engage inbound leads, capture consent, qualify buyers using RAG-grounded answers, and book appointments into calendar/CRM systems.
- Created a multi-tool RAG pipeline seeded with FAQs, policies, and high-converting conversation snippets, augmented with live web scraping of landing pages for real-time product and coverage data. Integrated Model Context Protocol (MCP) adapters for external tool calls and enforced citation-grounded generation to prevent unsupported responses (e.g., confirming coverage without successful tool verification).
- Set up a prompt governance and retrieval configuration system for all agents. System prompts, retrieval profiles, MCP tool definitions, and tool-use rules live in versioned config files tracked alongside code. This supports safe A/B testing of agent behaviors and retrieval strategies, plus automated regression checks to keep conversational flows and tool-calling policies auditable and reproducible.

## Skills

**LLM & GenAI**
RAG (hybrid retrieval, BM25 + dense), multi-agent systems, prompt engineering, hallucination gating, citation enforcement, contextual chunking, LangChain, LangGraph, LlamaIndex, Flowise, CrewAI, Model Context Protocol (MCP), OpenAI API (GPT-4, text-embedding-3-small), Anthropic Claude (Sonnet), Unstructured.io, Pinecone, Cohere Re-rank, vector databases & embeddings, QLoRA, LoRA, PEFT

**ML & Computer Vision**
PyTorch, Hugging Face, YOLOv8/v11, Stable Diffusion, instance segmentation, deep CNN, SAR image segmentation, model quantization, inference optimization

**MLOps, Evaluation & Observability**
Ragas, DeepEval, LangSmith, Langfuse, MLflow, SHAP, SRE-style AI monitoring (P50/P95 latency, cost-per-request, citation coverage), regression gating in CI, prompt versioning, golden dataset curation, Azure ML

**Languages & Frameworks**
Python (expert), SQL, FastAPI, Pydantic, Streamlit, JavaScript/TypeScript, HTML5, CSS

**Cloud, DevOps & Infrastructure**
Docker, GitHub Actions, Azure (Azure ML, enterprise data warehouse), AWS, Jenkins, OpenShift, CI/CD pipelines

**Data & Databases**
PostgreSQL, SQL/PL/SQL, RDBMS, Pinecone (serverless vector index), enterprise data warehouse pipelines, schema design, query optimization

**Practices & Tools**
Git/GitHub Enterprise, Claude Code, Power BI, Agile/Scrum, Jira, statistical analysis, hypothesis-driven root-cause analysis, A/B testing, versioned config management, automated testing (unit, integration, end-to-end)

## Professional Experience

### **Verizon Communications** | Houston, TX, USA

**AI & ML Engineer** | Jan 2025 - Jan 2026

- Built SQL transformation pipelines against Verizon's enterprise data warehouse, resolving cross-schema timestamp misalignments and structuring raw telemetry into model-ready feature sets. Fixing temporal consistency across data sources removed a class of silent data quality failures that, at **12M+** device scale, would have corrupted model predictions and invalidated downstream diagnostics.
- Unblocked a production deployment stalled by a 6x SLA breach (SHAP runtime: 90 min vs. 15 min SLA). After exhausting parallelization and hardware scaling options, built a Saabas approximation engine that cut runtime from 90 min to 3 min per region, a **30x improvement**. This met the SLA with 5x headroom and made real-time telemetry diagnostics feasible across a **12M-device** fleet.
- Validated the Saabas approximation against SHAP using a Jaccard Similarity experiment, confirming that top-3 feature attributions matched with high consistency across router entries. This proved the **30x** speedup came with zero accuracy cost, giving the team confidence to ship to **12M+** production devices.

### **D2K Lab - NASA Research Collaboration** | Houston, TX, USA

**AI Research Volunteer** | May 2024 - Dec 2024

- Created the SWiM (Spacecraft With Masks) benchmark dataset: **64k** annotated images for instance segmentation, generated using NASA's TTALOS pipeline and Stable Diffusion to simulate orbital conditions (glare, aurora borealis, varied lighting).
- Fine-tuned YOLOv8 and YOLOv11 models to a **0.92 Dice score** while staying within the hardware constraints of NASA's inspector spacecraft (4-core CPU, 4GB RAM).
- Optimized inference to **~443ms**, well within the sub-0.95s flight requirement, using quantization and efficient architectures.
- Co-lead author of the published benchmark on arXiv (2507.10775): "A New Dataset and Performance Benchmark for Real-time Spacecraft Segmentation in Onboard Computers."

### **Microsoft** | Hyderabad, TG, India

**ML & DS Consultant (Data and AI)** | Aug 2020 - Jul 2023

- Rebuilt KPI health tracking for multi-million-dollar Azure delivery portfolios, replacing ad-hoc reporting with a structured bi-weekly metrics review. Built a data-backed remediation framework that improved revenue forecast accuracy from **40% to 70%** and forecast-to-plan adherence from **60% to 90%**, correctly projecting ~**$600K** in previously misforecast revenue per cycle.
- Ran statistical root-cause analysis on underperforming delivery KPIs through hypothesis-driven trend analysis. Partnered with engineering leads on targeted recovery plans, successfully recovering or mitigating **4-6** at-risk projects per quarter (an estimated ~**$1M-$2M** in protected revenue) and reducing average time-to-recovery from weeks to days.
- Built and owned automated Power BI portfolio health dashboards across multi-million-dollar Azure portfolios, cutting ~**15 hours/week** of manual tracking. KPI anomaly detection went from days to near real-time, letting leadership act on financial and delivery risks before they became missed deadlines or cost overruns.

### **Indian Servers** | Vijayawada, AP, India

**Machine Learning Engineer Intern** | Jan 2019 - Jun 2020

- Developed and fine-tuned a deep CNN for SAR image segmentation, achieving a **30%** improvement in oil seep detection accuracy. This replaced a manual, error-prone detection process with an automated system.
- Built ML deployment pipelines for PyTorch computer vision models, replacing manual release processes with automated CI/CD workflows (GitHub Actions, MLflow, Docker, Azure ML). Model release cycles dropped from days to hours across multiple client environments.
