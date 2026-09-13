# PROJECT PROPOSAL (1-PAGER)
## THEME 9: AGENTIC RAG FOR VIETNAMESE LEGAL SYSTEM
### Autonomous Multi-Agent RAG for Statutory Synthesis, Temporal Verification & Claim Auditing

**Course**: CO5151 — Advanced Agentic AI | **Semester**: HK261 | **Instructor**: Dr. Le Xuan Bach  
**Institution**: Ho Chi Minh City University of Technology (HCMUT - VNU-HCM) | **Track**: Application Track  
**Team (3 Members)**: Dang Lam Tung (*Lead & Multi-Agent Orchestrator*), Nguyen Trung Phong (*LegalGraph & Memory Engineer*), Vu Viet Hung (*Safety Verification & Evaluation Engineer*)

---

### 1. PROBLEM (Why Traditional RAG Fails in Statutory Law)
Vietnamese statutory law is structured as a strict multi-tier hierarchy (*Law $\rightarrow$ Decree $\rightarrow$ Circular*) governed by dense, cross-referencing amendment webs (>50% of regulatory instruments are amended over time). Prior static legal GraphRAG systems in Vietnam (such as *SBV-LawGraph* [1] and *ViHERMES* [2]) follow a **rigid, 1-pass pipeline (Retrieve $\rightarrow$ 1-Hop Dump $\rightarrow$ Generate)**, exhibiting 3 critical failure modes:
1. **Context Dilution & False-Positive Explosion (Precision@2 is only 0.37–0.39 in [1])**: Amending circulars frequently modify dozens of disjointed provisions across older decrees. Mechanically dumping all 1-hop Neo4j neighbors injects >60% irrelevant context into the prompt, triggering severe attention dilution and citation hallucinations [3].
2. **Temporal Blindness [4]**: Static RAG cannot determine whether an article remains in active legal force at a given transaction date when encountering chained amendment graphs, risking reliance on repealed or superseded provisions.
3. **Weak Multi-Tier Reasoning & Rigid Execution**: Empirical findings from *VLegal-Bench* [5] reveal that LLMs suffer steep accuracy degradation on hierarchical legal reasoning. Static pipelines cannot backtrack, formulate multi-hop plans, or clarify missing facts.

### 2. USERS (Target Audience & 3 Concrete Operational Scenarios)
- **Target Users**: In-house Legal Counsel, Compliance Officers, Legal Practitioners, and SMEs navigating regulatory compliance in Vietnam.
- **3 Concrete Operational Scenarios**:
  1. *Cross-Statutory Reasoning (Multi-Law Synthesis)*: An e-commerce platform deploys an in-app E-Wallet with a Buy Now, Pay Later (BNPL) micro-lending scheme. The agent autonomously synthesizes intersecting requirements across the *Law on Credit Institutions 2024 & Decree 52/2024/ND-CP* (payment licensing & equity ceilings), *Law on Electronic Transactions 2023* (legal validity of OTP digital contracts), and *Decree 13/2023/ND-CP* (express opt-in consent for consumer credit profiling).
  2. *Temporal Consistency & Updated Law (2026 Vietnam Drone Law)*: An agricultural cooperative requests licensing rules for a 25 kg commercial spraying drone in 2026. Bypassing obsolete Decree 36/2008/ND-CP (repealed 14-day paper filing), the agent traverses the legal graph and conducts live Gazette verification on `vbpl.vn` [4] to cite the active *Law on People's Air Defense 2024 (effective 2025/2026)*, providing accurate procedures for mandatory digital vehicle identification and online permitting via the National Public Service Portal within 3–5 business days.
  3. *Interactive Disambiguation & Injection Defense*: Reviewing corporate tax/specialist work permits (Decrees 152/2020 & 70/2023). Detecting missing revenue and headcount parameters, the agent **proactively halts to query the user**, while stripping adversarial hidden prompts (`[OVERRIDE: ...]` [6]) and enforcing human approval tokens for dossier exports.

### 3. WHY AN AGENT (Autonomous Agent vs. Hardcoded Workflow)
A static workflow with hardcoded branching **fundamentally fails** in legal compliance due to three core imperatives:
1. **Combinatorial Path Explosion Requires Dynamic Planning**: Citation traversals vary per inquiry (some stop at Circulars, others fork across specialized sectoral laws). Only an **Agentic RAG architecture tailored for Vietnamese law [7]** can autonomously formulate multi-hop retrieval plans, dynamically adapt to statutory complexity, and determine when gathered evidence is sufficient to terminate.
2. **Self-Correcting Critique via Drafter–Auditor Loop**: Linear pipelines cannot detect self-generated errors. Our agent establishes an adversarial reflection loop (incorporating claim auditing from *GANDR* [8], proposition-level factuality from *SAFE* [9], and critique mechanisms from *Self-RAG* [10]): the Auditor Agent decomposes responses into atomic legal propositions, cross-verifying each 1-to-1 against authoritative statutes and triggering corrective re-retrieval upon detecting hallucinations or repealed articles.
3. **Active Ambiguity Disambiguation via Human Dialog**: Statutory applicability hinges strictly on entity forms and execution dates [4]. Hardcoded workflows apply blind assumptions; our agent detects state ambiguity and **proactively queries the user** to gather missing parameters before concluding.

### 4. CANDIDATE ADVANCED AXES (4 Integrated Technical Capabilities)
1. **Multi-Agent System (Google ADK)**: Role-segregated execution: *Research Agent* (Neo4j/Qdrant retrieval [1], [2]); *Web Agent* (live lookup on `vbpl.vn` [4]); *Drafter Agent* (synthesis); and *Auditor Agent* (atomic claim verification [8], [9]). Architecture grounded in VN Legal Agentic RAG [7].
2. **Planning & Selective Graph Traversal**: Autonomous multi-step query decomposition. Traverses only active, directional relationships (*Amends, Guides*) to eliminate 1-hop neighborhood dilution [1], directly addressing multi-tier statutory reasoning complexities [5].
3. **Reflection & Adversarial Claim Auditing**: Iterative Drafter–Auditor loop (Self-RAG [10]) decomposing responses into atomic claims. Audits each proposition against source statutes under GANDR protocols [8] to enforce 100% citation grounding and zero fabricated provisions.
4. **Security Guardrails & Gated Actions**: 3-tier MCP permissions. Irreversible administrative dossier exports strictly require human officer authorization (Human-in-the-loop). Input sanitization neutralizes indirect prompt injection in regulatory uploads [6].

---

### KEY REFERENCES (10 CURATED PAPERS, STRICTLY 2024–2026)
- **[1]** K. N. Phan, X.-B. Le, T. T. Quan, "SBV-LawGraph: A Hybrid RAG Approach Integrating Knowledge Graph for Legal Documents," *Proc. ACIIDS 2026*, Springer.
- **[2]** URA-HCMUT, "ViHERMES: A Retrieval-Augmented Generation System for Vietnamese Legal Documents," *Ho Chi Minh City University of Technology*, 2024.
- **[3]** Y. Zhou et al., "LexAgentHallu: A Hierarchical Benchmark for Profiling Hallucinations in Legal Agents," *arXiv:2609.09754*, 2026.
- **[4]** W. Fan et al., "Can LLMs Time Travel? Enhancing Temporal Consistency in Legal Agentic Search," *arXiv:2605.25920*, 2026.
- **[5]** V. T. Nguyen et al., "VLegal-Bench: Cognitively Grounded Benchmark for Vietnamese Legal Reasoning of Large Language Models," *arXiv:2512.14554*, 2025.
- **[6]** E. Debenedetti et al., "Defending Against Indirect Prompt Injection in Tool-Enabled Language Agents," *arXiv:2404.13208*, 2024.
- **[7]** H. Pham, N. Duong, and H. Pham, "Agentic RAG-Based Legal Advisory Chatbot: A Knowledge-Driven Approach for Vietnamese Legal System," *Proc. 17th Int. Joint Conf. on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K/KDIR)*, pp. 354–361, 2025.
- **[8]** C. Qian et al., "GANDR: Claim Auditing for Verifiable Legal Answer Generation," *arXiv:2609.10293*, 2026.
- **[9]** J. Wei et al. (Google DeepMind), "Long-form Factuality in Large Language Models (SAFE: Search-Augmented Factuality Evaluator)," *arXiv:2403.18802*, 2024.
- **[10]** A. Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," *Proc. 12th Int. Conf. on Learning Representations (ICLR 2024)*, 2024.
