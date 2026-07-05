# Deep Technology Agents Platform Architecture

The Deep Technology Agents platform is a production-grade, highly scalable multi-agent system built using **LangGraph**, **FastAPI**, and **Google Gemini**. It dynamically orchestrates multiple specialized AI agents to execute deep research, analyze data, and synthesize comprehensive reports.

## System Overview: What It Is & How It Works

### What Is It?
The Deep Technology Agents platform is an autonomous, enterprise-grade AI research system. It is designed to take vague or highly complex user queries—such as "Analyze the latest trends in autonomous vehicle AI models and their funding"—and autonomously perform the work of a human research analyst. It crawls the web, reads academic papers, searches news, cross-references facts, synthesizes the findings, and generates a polished, fully-cited intelligence report.

### How Does It Work?
The platform operates as a continuous state machine where a single "state" (containing the query, evidence, and report) is passed down an assembly line of specialized AI agents. Here is the end-to-end lifecycle of a request:

1. **Ingestion & Triage:** A user submits a prompt via the FastAPI backend. The `QueryUnderstandingAgent` intercepts this, classifies the user's intent, and determines the **Complexity** (Simple, Medium, Complex, Very Complex).
2. **Planning & Decomposition:** If the query is complex, the `PlannerAgent` and `TaskSplitterNode` break the single massive prompt into multiple independent, highly-focused sub-tasks (e.g., separating "AI Models" from "Funding").
3. **Parallel Execution:** The `ResearchOrchestrator` takes these sub-tasks and fires off dozens of asynchronous searches across the web, Wikipedia, arXiv, and news APIs simultaneously. It operates under a strict **Global Execution Budget**—if the 180-second timer runs out, it gracefully halts new searches to guarantee a response is delivered.
4. **Data Normalization:** As raw JSON/HTML data floods back, the `EvidenceCollectorAgent` cleans, normalizes, and deduplicates the information into a strict schema.
5. **Hierarchical Synthesis:** To prevent overwhelming the AI's context window, the `KnowledgeSynthesisAgent` processes evidence for each sub-task individually to create **Local Summaries**, and then merges them into a single **Global Knowledge Graph**.
6. **Insight & Reporting:** The `InsightGenerationAgent` extracts higher-level trends, risks, and competitor comparisons. Finally, the `ReportWriterAgent` takes all this knowledge and drafts the final Markdown report. If the knowledge payload is too large, it dynamically switches to **Adaptive Generation**, writing the report section-by-section.
7. **Quality Control:** Before returning to the user, a `ReviewAgent` checks for hallucinations, and a `CitationFormatterAgent` injects proper inline references mapping back to the originally scraped URLs.

Throughout this entire process, a centralized **Model Router** dynamically switches between Gemini models (Flash vs. Pro) based on task difficulty, while a **Monitoring Service** logs every latency spike and token used.

### Execution Paths by Query Complexity

The platform executes entirely different logic paths depending on how the `QueryUnderstandingAgent` classifies the request:

*   **Short/Simple Queries:** (e.g., "What is React?")
    *   **Fast Path:** The `IntentRouter` bypasses the entire Deep Research pipeline. The system immediately routes the query to a lightweight `casual_chat_node` or `knowledge_answer_node`, utilizing Gemini Flash for sub-second response times. No complex agents or tool orchestrators are invoked.
*   **Medium Queries:** (e.g., "What are the new features in Next.js 15?")
    *   **Standard Path:** The system generates a simple hypothesis and plan. The `ResearchOrchestrator` runs standard parallel searches. Validation is performed directly, and `KnowledgeSynthesisAgent` synthesizes all the evidence in a single context window. A standard report is generated in one pass.
*   **Long/Complex Queries:** (e.g., "Analyze the latest trends in autonomous vehicle AI models and compare their startup funding rounds.")
    *   **Decomposed Path:** The query hits the `TaskSplitterNode`, which fragments the massive prompt into independent research sub-tasks. The system iterates through each sub-task, running isolated searches for "AI Models" and "Startup Funding." 
    *   **Hierarchical Synthesis:** Evidence is synthesized locally for each sub-task first to prevent context overflows, then merged globally. 
    *   **Adaptive Reporting:** The `ReportWriterAgent` detects the massive JSON payload and intelligently generates the final report section-by-section to ensure depth and accuracy without hitting LLM token limits.

## Core System Architecture

The core architecture operates as a Directed Acyclic Graph (DAG) state machine (powered by LangGraph). The state of the entire system (`GraphState`) flows through sequential nodes, each powered by a specialized Agent or Service.

### 1. Routing & Understanding
*   **Query Understanding Node:** Evaluates incoming user queries, extracting structure (intent, keywords, domain) and classifying complexity (`Simple`, `Medium`, `Complex`, `Very Complex`). It initializes a strict global execution timer.
*   **Intent Router Node:** Determines if the query requires casual chat, a direct knowledge answer, or deep agentic research, bypassing the heavy pipeline for trivial queries.

### 2. Planning & Decomposition
*   **Hypothesis Generation Node:** Drafts an initial research hypothesis based on the structured query.
*   **Planner Node:** Analyzes the hypothesis and generates a structured research plan, including recommended search tools.
*   **Task Splitter Node:** For `Complex` or `Very Complex` queries, this node automatically decomposes the single massive query into smaller, highly-focused independent research sub-tasks (e.g., separating "AI Models" from "Startup Funding").

### 3. Independent Parallel Research
*   **Parallel Research Tools Node:** Uses the `ResearchOrchestrator` to execute recommended tools (Web Search, Wikipedia, Arxiv, News Search) asynchronously.
    *   **Complex Queries:** Spins up independent pipelines for each sub-task (`Sub-Plan -> Search -> Collect`). Each task maintains its own isolated evidence pool to prevent context contamination.
    *   **Execution Budget:** Implements a global timeout (e.g., 180 seconds). If the system nears the budget limit, it preemptively stops launching new tool queries and pushes the existing data downstream.
*   **Evidence Collector Node:** Normalizes raw data from various APIs into a strict `EvidenceItem` schema without aggressively truncating or deduplicating.

### 4. Validation & Grounding (Modular Pipeline)
*   **Reference Manager & Fusion Grounding:** Cross-references the raw evidence with the initial hypothesis to ground the facts.
*   *Note on Fast-Pathing:* The system utilizes "Fast Paths" to dynamically skip intensive validation nodes (duplicate detection, credibility scoring, conflict detection) when maximum speed is prioritized, routing directly to Knowledge Synthesis.

### 5. Hierarchical Knowledge Synthesis
*   **Knowledge Synthesis Node & Agent:** Transforms unstructured evidence into structured `KnowledgeGraph`, `Facts`, `Entities`, and `Topic Summaries`.
    *   **Hierarchical Merge:** For complex, decomposed queries, it prevents context window overflows by first generating **Local Summaries** for each sub-task independently, and subsequently merging those into a singular **Global Knowledge Summary**.

### 6. Insight Generation
*   **Insight Generation Node:** Analyzes the structured knowledge to extract higher-order intelligence: trend analysis, competitor comparisons, risks, opportunities, and strategic takeaways.

### 7. Adaptive Report Writing
*   **Report Writer Node & Agent:** Drafts the comprehensive final markdown report.
    *   **Adaptive Generation:** If the compiled Knowledge and Insights JSON payload exceeds strict token thresholds (e.g., 30k tokens), the agent dynamically switches to generating the report **section-by-section** (Executive Summary, Market Trends, Risks, etc.) and concatenates them to circumvent model context limits.

### 8. Quality Control & Formatting
*   **Review Agent Node:** Reviews the final report against the extracted facts for quality and hallucinatory statements.
*   **Citation Formatter Node:** Ensures all claims are properly cited using the tracking map generated by the Reference Manager.

---

## Shared Infrastructure Services

*   **GeminiService:** A centralized interface for all LLM calls. It utilizes a **Prompt Budget System**: before any request, it estimates tokens. If a prompt is oversized, it automatically splits it into manageable chunks, processes them independently, and concatenates the output to guarantee stability.
*   **Research Decision Service:** Evaluates intent routing logic dynamically.
*   **State Management (`GraphState`):** Uses Python `TypedDict` and `operator.add` annotations to maintain an immutable, traceable log of all agent actions, metadata, execution time, and errors throughout the graph execution.

### Intelligent Multi-Model Orchestration

The platform uses a centralized **Model Router** that dynamically orchestrates multiple Google Gemini models instead of relying on a single model.

The Model Router automatically selects the optimal model based on:

- Query complexity
- Prompt size
- Context window requirements
- Structured output requirements
- Reasoning complexity
- Latency
- Model health
- Rate limits
- API availability

The router distributes work across different Gemini models:

- **Gemini 2.5 Flash** → Fast tasks such as query understanding, intent detection, planning, search strategy, duplicate detection, and validation.
- **Gemini 2.5 Pro** → Knowledge synthesis, deep reasoning, competitor analysis, and complex inference.
- **Gemini 3 Pro / Deep Research models** → Long-form report generation, enterprise-scale analysis, and very large context workloads.

If a preferred model becomes unavailable due to rate limits, API errors, or service interruptions, the router automatically fails over to another compatible model without interrupting the workflow.

This architecture optimizes speed, cost, reliability, and reasoning quality while ensuring no single model becomes a bottleneck.

### Intelligent Search Strategy

Before executing searches, the Search Strategy Agent analyzes the research plan and dynamically selects only the most relevant search tools.

The strategy considers:

- Query intent
- Technology domain
- Time sensitivity
- Required evidence type
- Confidence target
- Tool health
- Estimated execution cost

The agent prioritizes official documentation, GitHub, research papers, technology news, and startup databases while avoiding unnecessary searches.

Early stopping is triggered once sufficient high-confidence evidence has been collected.

### Fault Tolerance & Resiliency

The platform is designed to remain operational even when individual tools, APIs, or language models become unavailable.

Every external dependency executes inside an isolated safe execution wrapper.

Capabilities include:

- Independent asynchronous tool execution
- Automatic retry for transient failures (429, 503, timeout)
- Circuit Breaker for repeatedly failing services
- Graceful degradation
- Partial evidence generation
- Automatic search-provider fallback
- Model failover
- Execution recovery
- Global execution budget enforcement

If one or more tools fail, the workflow continues using all successfully collected evidence.

The system guarantees that a report is generated whenever at least one verified source succeeds.

### Monitoring & Observability

A centralized Monitoring Service continuously tracks the health and performance of the entire workflow.

It records:

- Current workflow stage
- Active LangGraph node
- Agent execution time
- Search tool latency
- LLM latency
- Selected Gemini model
- Prompt size
- Estimated token usage
- Retry attempts
- Tool failures
- Remaining execution budget
- Overall workflow duration

The service powers real-time progress updates, execution analytics, debugging, and production monitoring.

## Workflow Manager & Execution Engine

The entire platform is orchestrated by LangGraph's execution engine, which acts as the central workflow manager.

Responsibilities include:

- State transition management
- Conditional routing
- Parallel node execution
- Agent orchestration
- Retry coordination
- Execution budget enforcement
- Error propagation
- Checkpointing
- Recovery after transient failures
- Workflow completion detection

The execution engine ensures that every node operates independently while maintaining a consistent shared GraphState throughout the workflow.
