import os

def generate_docs():
    filepath = r"d:\Deep technology agents\ARCHITECTURE_AND_EXECUTION_DOCS.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Deep Technology Agents - Architecture & Execution Documentation\n\n")

        # --------------------------------------------------------
        # 1. COMPLETE SYSTEM ARCHITECTURE
        # --------------------------------------------------------
        f.write("## 1. COMPLETE SYSTEM ARCHITECTURE\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  U[User / Frontend] --> API[FastAPI]\n")
        f.write("  API --> LG[LangGraph Execution Engine]\n")
        f.write("  LG --> AG[Agents]\n")
        f.write("  LG --> SV[Services]\n")
        f.write("  AG --> SV\n")
        f.write("  SV --> TL[Tools]\n")
        f.write("  SV --> MR[Model Router]\n")
        f.write("  MR --> GM[Gemini Models]\n")
        f.write("  TL --> SA[Search APIs]\n")
        f.write("  API --> R[Response]\n")
        f.write("```\n\n")
        
        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("actor User\nnode Frontend\nnode FastAPI\nnode LangGraph\nnode Agents\nnode Services\nnode Tools\nnode ModelRouter\ncloud GeminiModels\ncloud SearchAPIs\n")
        f.write("User -> Frontend\nFrontend -> FastAPI\nFastAPI -> LangGraph\nLangGraph -> Agents\nLangGraph -> Services\nAgents -> Services\nServices -> Tools\nServices -> ModelRouter\nModelRouter -> GeminiModels\nTools -> SearchAPIs\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nThe system follows a layered architecture where FastAPI receives requests and triggers the LangGraph state machine. LangGraph coordinates Agents and Services. Services interface with External Tools and Gemini Models (via a Model Router).\n\n")
        f.write("### Short Description\nHigh-level topology of the Deep Technology Agents platform.\n\n")
        f.write("### Components Involved\nFrontend, FastAPI, LangGraph, Agents, Services, Tools, Model Router, Gemini Models, Search APIs.\n\n")
        f.write("### Data Flow\nUser Input -> FastAPI -> LangGraph -> Agents -> Services -> Models/Tools -> Response.\n\n")
        f.write("### Failure Points\nFastAPI overload, LangGraph state corruption, External API timeouts.\n\n")
        f.write("### Recovery Strategy\nFastAPI rate limiting, State checkpointing, Service-level retry/circuit breakers.\n\n")

        # --------------------------------------------------------
        # 2. LANGGRAPH EXECUTION GRAPH
        # --------------------------------------------------------
        f.write("## 2. LANGGRAPH EXECUTION GRAPH\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  START((START)) --> QU[query_understanding_node]\n")
        f.write("  QU --> IR[intent_router_node]\n")
        f.write("  IR -- casual_chat_node --> CC[casual_chat_node]\n")
        f.write("  IR -- knowledge_answer_node --> KA[knowledge_answer_node]\n")
        f.write("  IR -- hypothesis_generation_node --> HG[hypothesis_generation_node]\n")
        f.write("  CC --> END((END))\n")
        f.write("  KA --> END\n")
        f.write("  HG --> PN[planner_node]\n")
        f.write("  PN --> TS[task_splitter_node]\n")
        f.write("  TS --> TR[tool_router_node]\n")
        f.write("  TR --> PR[parallel_research_tools_node]\n")
        f.write("  PR --> EC[evidence_collector_node]\n")
        f.write("  EC --> RM[reference_manager_node]\n")
        f.write("  RM --> FG[fusion_grounding_node]\n")
        f.write("  FG --> KS[knowledge_synthesis_node]\n")
        f.write("  KS --> IG[insight_generation_node]\n")
        f.write("  IG --> RW[report_writer_node]\n")
        f.write("  RW --> RR[response_relevance_node]\n")
        f.write("  RR --> RA[review_agent_node]\n")
        f.write("  RA --> CF[citation_formatter_node]\n")
        f.write("  CF --> END\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("(*) --> query_understanding_node\n")
        f.write("query_understanding_node --> intent_router_node\n")
        f.write("intent_router_node --> casual_chat_node\n")
        f.write("intent_router_node --> knowledge_answer_node\n")
        f.write("intent_router_node --> hypothesis_generation_node\n")
        f.write("casual_chat_node --> (*)\n")
        f.write("knowledge_answer_node --> (*)\n")
        f.write("hypothesis_generation_node --> planner_node\n")
        f.write("planner_node --> task_splitter_node\n")
        f.write("task_splitter_node --> tool_router_node\n")
        f.write("tool_router_node --> parallel_research_tools_node\n")
        f.write("parallel_research_tools_node --> evidence_collector_node\n")
        f.write("evidence_collector_node --> reference_manager_node\n")
        f.write("reference_manager_node --> fusion_grounding_node\n")
        f.write("fusion_grounding_node --> knowledge_synthesis_node\n")
        f.write("knowledge_synthesis_node --> insight_generation_node\n")
        f.write("insight_generation_node --> report_writer_node\n")
        f.write("report_writer_node --> response_relevance_node\n")
        f.write("response_relevance_node --> review_agent_node\n")
        f.write("review_agent_node --> citation_formatter_node\n")
        f.write("citation_formatter_node --> (*)\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nExact 1:1 mapping of `builder.py` edge definitions. Routes separate deep research from casual chat. The deep research path skips modular validation (duplicate detection, credibility scoring, etc.) for performance via a fast-path.\n\n")
        f.write("### Short Description\nVisual representation of the LangGraph DAG state machine.\n\n")
        f.write("### Components Involved\nAll node functions in `nodes.py` and state configuration in `builder.py`.\n\n")
        f.write("### Data Flow\nGraphState is passed linearly down the pipeline, accumulating arrays of data.\n\n")
        f.write("### Failure Points\nNode execution errors interrupting the pipeline flow.\n\n")
        f.write("### Recovery Strategy\nGraph-level checkpointing and internal exception catching (appending to `errors` array in GraphState).\n\n")

        # --------------------------------------------------------
        # 3. COMPLETE EXECUTION FLOW
        # --------------------------------------------------------
        f.write("## 3. COMPLETE EXECUTION FLOW\n\n")
        f.write("### Mermaid\n```mermaid\nsequenceDiagram\n")
        f.write("  actor User\n")
        f.write("  participant FastAPI\n")
        f.write("  participant LangGraph\n")
        f.write("  participant Nodes\n")
        f.write("  participant GeminiService\n")
        f.write("  participant Monitor\n")
        f.write("  User->>FastAPI: Query\n")
        f.write("  FastAPI->>LangGraph: invoke(GraphState)\n")
        f.write("  LangGraph->>Nodes: Execute Node\n")
        f.write("  Nodes->>Monitor: log_node_start(Budget Check)\n")
        f.write("  Nodes->>GeminiService: chat/structured_chat\n")
        f.write("  GeminiService->>GeminiService: Check Prompt Budget\n")
        f.write("  GeminiService->>GeminiService: Route Model (Flash/Pro)\n")
        f.write("  GeminiService-->>Nodes: LLM Response\n")
        f.write("  Nodes-->>LangGraph: Updated GraphState\n")
        f.write("  LangGraph-->>FastAPI: Final State\n")
        f.write("  FastAPI-->>User: Response\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("actor User\nparticipant FastAPI\nparticipant LangGraph\nparticipant Nodes\nparticipant GeminiService\nparticipant MonitoringService\n")
        f.write("User -> FastAPI: Query\nFastAPI -> LangGraph: Start Graph\nLangGraph -> Nodes: Execute Node\nNodes -> MonitoringService: Check Budget & Log\nNodes -> GeminiService: Call LLM\nGeminiService -> GeminiService: Apply Budgets & Route Model\nGeminiService --> Nodes: Result\nNodes --> LangGraph: State Update\nLangGraph --> FastAPI: Completion\nFastAPI --> User: Result\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nEnd-to-end execution flow emphasizing cross-cutting concerns like Monitoring, Execution Budget enforcement, and Prompt Budgets handled dynamically during Node execution.\n\n")
        f.write("### Short Description\nDetailed sequential flow of an interaction.\n\n")
        f.write("### Components Involved\nUser, FastAPI, LangGraph, All Nodes, GeminiService, MonitoringService.\n\n")
        f.write("### Data Flow\nQueries flow inward, execute via LLM routing, and cascade state updates backward.\n\n")
        f.write("### Failure Points\nExecution Budget Timeout, Prompt size overflows.\n\n")
        f.write("### Recovery Strategy\nNodes preemptively exit loop if budget < 30s; GeminiService chunk-splits massive prompts automatically.\n\n")

        # --------------------------------------------------------
        # 4. SEQUENCE DIAGRAM
        # --------------------------------------------------------
        f.write("## 4. SEQUENCE DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\nsequenceDiagram\n")
        f.write("  actor User\n  participant Front as Frontend\n  participant API as FastAPI\n  participant LG as LangGraph\n  participant QA as QueryUnderstandingAgent\n  participant PA as PlannerAgent\n  participant RO as ResearchOrchestrator\n  participant T as Search Tools\n  participant KS as KnowledgeSynthesisAgent\n  participant RW as ReportWriterAgent\n  participant GS as Gemini Models\n")
        f.write("  User->>Front: Enter query\n")
        f.write("  Front->>API: POST /research\n")
        f.write("  API->>LG: invoke(state)\n")
        f.write("  LG->>QA: understand_query()\n")
        f.write("  QA->>GS: structured_chat()\n")
        f.write("  GS-->>QA: Intent & Complexity\n")
        f.write("  QA-->>LG: state\n")
        f.write("  LG->>PA: generate_plan()\n")
        f.write("  PA->>GS: structured_chat()\n")
        f.write("  GS-->>PA: Plan\n")
        f.write("  PA-->>LG: state\n")
        f.write("  LG->>RO: execute_plan()\n")
        f.write("  RO->>T: run_tool_safely()\n")
        f.write("  T-->>RO: Raw Evidence\n")
        f.write("  RO-->>LG: state\n")
        f.write("  LG->>KS: synthesize()\n")
        f.write("  KS->>GS: structured_chat() / hierarchy\n")
        f.write("  GS-->>KS: KnowledgeGraph\n")
        f.write("  KS-->>LG: state\n")
        f.write("  LG->>RW: write_report()\n")
        f.write("  RW->>GS: invoke() [section-by-section]\n")
        f.write("  GS-->>RW: Markdown Report\n")
        f.write("  RW-->>LG: state\n")
        f.write("  LG-->>API: final_report\n")
        f.write("  API-->>Front: response\n")
        f.write("  Front-->>User: Display Report\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("actor User\nparticipant Frontend\nparticipant FastAPI\nparticipant LangGraph\nparticipant Agents\nparticipant Tools\nparticipant GeminiService\n")
        f.write("User -> Frontend: Query\nFrontend -> FastAPI: HTTP\nFastAPI -> LangGraph: Invoke\nLangGraph -> Agents: Process\nAgents -> GeminiService: Call LLM\nGeminiService --> Agents: LLM Response\nAgents -> Tools: Execute Search\nTools --> Agents: Search Results\nAgents --> LangGraph: GraphState\nLangGraph --> FastAPI: Report\nFastAPI --> Frontend: Response\nFrontend --> User: View\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nA strict UML Sequence diagram showing synchronous and asynchronous interactions between distinct actors, software boundaries, and models.\n\n")
        f.write("### Short Description\nEnd-to-end API interaction sequence.\n\n")
        f.write("### Components Involved\nFrontend, API, Graph, Specific Agents, Tools, Gemini API.\n\n")
        f.write("### Data Flow\nRequest payload -> GraphState mutation -> Output payload.\n\n")
        f.write("### Failure Points\nNetwork failures between Frontend/FastAPI or Tools.\n\n")
        f.write("### Recovery Strategy\nFrontend retry mechanism; Tool isolated safe wrappers return empty/error statuses gracefully.\n\n")

        # --------------------------------------------------------
        # 5. GRAPHSTATE DIAGRAM
        # --------------------------------------------------------
        f.write("## 5. GRAPHSTATE DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\nclassDiagram\n")
        f.write("  class GraphState {\n")
        f.write("    +str query\n    +list messages\n    +str response\n    +list steps\n    +dict metadata\n    +list errors\n    +list sources\n    +float execution_time\n    +list subtask_evidence\n    +dict structured_query\n    +dict hypothesis_draft\n    +dict grounded_draft\n    +dict relevance_metrics\n    +dict reference_map\n    +list citations\n    +list evidence_traceability\n    +str intent\n    +int research_score\n    +str mode\n    +dict research_plan\n    +list tasks\n    +list keywords\n    +str domain\n    +str complexity\n    +list recommended_tools\n    +list research_results\n    +list completed_tools\n    +list failed_tools\n    +list raw_evidence\n    +int evidence_count\n    +dict tool_statistics\n    +dict collection_metadata\n    +list unique_evidence\n    +list duplicate_groups\n    +dict credibility_scores\n    +list conflicts\n    +dict confidence_scores\n    +list validated_evidence\n    +list discarded_evidence\n    +dict validation_report\n    +str validation_summary\n    +dict knowledge\n    +str executive_summary\n    +list topic_summaries\n    +list entities\n    +list facts\n    +list timelines\n    +list relationships\n    +list statistics\n    +list terminology\n    +dict knowledge_graph\n    +list insights\n    +list trend_analysis\n    +list comparisons\n    +list risks\n    +list opportunities\n    +list limitations\n    +list future_research\n    +list strategic_takeaways\n    +str final_report\n    +str reviewed_report\n    +dict quality_scores\n    +dict quality_report\n    +str review_summary\n    +list improvements\n    +list issues_found\n  }\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("class GraphState {\n  +query\n  +metadata\n  +complexity\n  +tasks\n  +raw_evidence\n  +knowledge\n  +final_report\n}\n")
        f.write("note right of GraphState: Passed linearly through all LangGraph nodes\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nThe `GraphState` is a Python `TypedDict` containing every state variable mapped via `operator.add` for lists or overwritten for strings/dicts. `query_understanding_node` sets `metadata`, `query`, `complexity`. `planner_node` sets `tasks`, `research_plan`. `parallel_research_tools_node` sets `subtask_evidence`, `raw_evidence`. `knowledge_synthesis_node` sets `knowledge`.\n\n")
        f.write("### Short Description\nThe immutable data structure driving the pipeline.\n\n")
        f.write("### Components Involved\n`state.py`, all `nodes.py`.\n\n")
        f.write("### Data Flow\nPassed explicitly into every async node function.\n\n")
        f.write("### Failure Points\nType mismatches if an agent returns unexpected JSON schemas.\n\n")
        f.write("### Recovery Strategy\nPydantic schema validation inside `GeminiService` forces strict compliance before appending to GraphState.\n\n")

        # --------------------------------------------------------
        # 6. AGENT INTERACTION DIAGRAM
        # --------------------------------------------------------
        f.write("## 6. AGENT INTERACTION DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\ngraph LR\n")
        f.write("  Q[QueryUnderstandingAgent] --> I[IntentRouterAgent]\n")
        f.write("  I --> H[HypothesisGenerationAgent]\n")
        f.write("  H --> P[PlannerAgent]\n")
        f.write("  P --> RO[ResearchOrchestrator]\n")
        f.write("  RO --> E[EvidenceCollectorAgent]\n")
        f.write("  E --> RM[ReferenceManagerAgent]\n")
        f.write("  RM --> FG[FusionGroundingAgent]\n")
        f.write("  FG --> KS[KnowledgeSynthesisAgent]\n")
        f.write("  KS --> IN[InsightGenerationAgent]\n")
        f.write("  IN --> RW[ReportWriterAgent]\n")
        f.write("  RW --> RE[ResponseRelevanceAgent]\n")
        f.write("  RE --> RV[ReviewAgent]\n")
        f.write("  RV --> CF[CitationFormatterAgent]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("agent PlannerAgent\nagent EvidenceCollectorAgent\nagent KnowledgeSynthesisAgent\nagent ReportWriterAgent\n")
        f.write("PlannerAgent -> EvidenceCollectorAgent: Provides Search Tasks\nEvidenceCollectorAgent -> KnowledgeSynthesisAgent: Provides Validated Evidence\nKnowledgeSynthesisAgent -> ReportWriterAgent: Provides Structured Knowledge\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nShows the logical dependency chain between Agents. While they don't directly call each other's code (LangGraph mediates), their input/output shapes are inherently coupled.\n\n")
        f.write("### Short Description\nLogical dependency mapping of all agents.\n\n")
        f.write("### Components Involved\nAll files in `app/agents/`.\n\n")
        f.write("### Data Flow\nAgent -> LangGraph -> Agent.\n\n")
        f.write("### Failure Points\nAgent hallucinates an output breaking downstream agent assumptions.\n\n")
        f.write("### Recovery Strategy\nDownstream agents have strict schema parsers or fallback logic (e.g. ReportWriter returns a generic fallback if knowledge is empty).\n\n")

        # --------------------------------------------------------
        # 7. SERVICE INTERACTION DIAGRAM
        # --------------------------------------------------------
        f.write("## 7. SERVICE INTERACTION DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  AG[All Agents] --> GS[GeminiService]\n")
        f.write("  GS --> MS[MonitoringService]\n")
        f.write("  AG --> MS\n")
        f.write("  nodes --> RO[ResearchOrchestrator]\n")
        f.write("  RO --> ES[EvidenceService]\n")
        f.write("  RO --> MS\n")
        f.write("  nodes --> RDS[ResearchDecisionService]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("component Agents\ncomponent GeminiService\ncomponent MonitoringService\ncomponent ResearchOrchestrator\n")
        f.write("Agents --> GeminiService: LLM inference\nGeminiService --> MonitoringService: Log tokens/latency\nAgents --> MonitoringService: Log node timing\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nHighlights utility services shared across nodes. `GeminiService` handles all AI via a Model Router. `MonitoringService` acts as a global singleton capturing telemetry.\n\n")
        f.write("### Short Description\nDependencies between Agents and core Services.\n\n")
        f.write("### Components Involved\n`app/services/*`.\n\n")
        f.write("### Data Flow\nAgents pass string/schemas to Services, Services perform side-effects or network calls.\n\n")
        f.write("### Failure Points\nService singleton bottlenecks or thread safety (asyncio handles this natively).\n\n")
        f.write("### Recovery Strategy\nServices wrap network calls in `try/except`.\n\n")

        # --------------------------------------------------------
        # 8. MODEL ROUTER FLOW
        # --------------------------------------------------------
        f.write("## 8. MODEL ROUTER FLOW\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  REQ[Incoming LLM Request] --> CL[Task Classification]\n")
        f.write("  CL -- Fast Tasks / Validation --> F[Gemini 2.5 Flash]\n")
        f.write("  CL -- Deep Reasoning / Complex --> P[Gemini 2.5 Pro]\n")
        f.write("  CL -- Very Complex Reports --> P3[Gemini 3 Pro / Deep Research]\n")
        f.write("  F --> PB[Prompt Budget Check]\n")
        f.write("  P --> PB\n")
        f.write("  P3 --> PB\n")
        f.write("  PB -- < 30k Tokens --> EX[Execute Model]\n")
        f.write("  PB -- > 30k Tokens --> SPLIT[Split Prompt into Chunks]\n")
        f.write("  SPLIT --> EX\n")
        f.write("  EX -- Success --> RES[Response]\n")
        f.write("  EX -- 429/503 --> FB[Fallback Model Trigger]\n")
        f.write("  FB --> EX\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("start\n:Incoming LLM Request;\nif (Task Type?) then (Fast/Validation)\n  :Select Gemini 2.5 Flash;\nelseif (Deep Reasoning)\n  :Select Gemini 2.5 Pro;\nelse (Very Complex)\n  :Select Gemini 3 Pro;\nendif\nif (Prompt > 30k Tokens?) then (Yes)\n  :Split into Chunks;\nelse (No)\nendif\n:Execute Model;\nif (Error?) then (Yes)\n  :Trigger Fallback Model;\nelse (No)\nendif\n:Return Response;\nstop\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nThe `route_model` in `GeminiService` assigns the optimal LLM based on task type and complexity parameter. It enforces token budgets and uses LangChain fallbacks for resiliency.\n\n")
        f.write("### Short Description\nDynamic intelligence routing.\n\n")
        f.write("### Components Involved\n`GeminiService.route_model`, `GeminiService.chat`, `GeminiService.structured_chat`.\n\n")
        f.write("### Data Flow\nTask Type/Complexity -> Model Selection -> Chunking -> API Call -> Fallback -> Result.\n\n")
        f.write("### Failure Points\nAll models in the fallback chain fail.\n\n")
        f.write("### Recovery Strategy\nRaise exception, caught by Node execution wrapper, logs error to GraphState, pipeline degrades gracefully.\n\n")

        # --------------------------------------------------------
        # 9. SEARCH PIPELINE
        # --------------------------------------------------------
        f.write("## 9. SEARCH PIPELINE\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  PL[Planner Node / Task Splitter] --> OR[Research Orchestrator]\n")
        f.write("  OR --> W[Web Search]\n")
        f.write("  OR --> N[News Search]\n")
        f.write("  OR --> A[Arxiv Search]\n")
        f.write("  OR --> WK[Wikipedia Search]\n")
        f.write("  W --> EC[Evidence Collector]\n")
        f.write("  N --> EC\n")
        f.write("  A --> EC\n")
        f.write("  WK --> EC\n")
        f.write("  EC --> RM[Reference Manager]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("component Orchestrator\ncomponent WebSearch\ncomponent ArxivSearch\ncomponent EvidenceCollector\n")
        f.write("Orchestrator -> WebSearch: Execute\nOrchestrator -> ArxivSearch: Execute\nWebSearch --> EvidenceCollector: Raw Data\nArxivSearch --> EvidenceCollector: Raw Data\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nTools are executed concurrently via `asyncio.gather` in `ResearchOrchestrator`. Tool selection is recommended by `PlannerAgent`. All raw output funnels into `EvidenceCollectorAgent` for normalization into `EvidenceItem` schemas.\n\n")
        f.write("### Short Description\nParallel data ingestion pipeline.\n\n")
        f.write("### Components Involved\n`PlannerAgent`, `ResearchOrchestrator`, `tools/*`, `EvidenceCollectorAgent`.\n\n")
        f.write("### Data Flow\nQueries -> Tools -> Array of dictionaries -> Normalization -> GraphState.\n\n")
        f.write("### Failure Points\nRate limits on APIs (e.g., DuckDuckGo, Arxiv).\n\n")
        f.write("### Recovery Strategy\nOrchestrator staggers requests (delay logic) and uses `try/except` per tool. A failure in one tool does not kill the others.\n\n")

        # --------------------------------------------------------
        # 10. REPORT GENERATION FLOW
        # --------------------------------------------------------
        f.write("## 10. REPORT GENERATION FLOW\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  K[Knowledge / Insights] --> RW[Report Writer Agent]\n")
        f.write("  RW --> SZ{Payload > 30k chars?}\n")
        f.write("  SZ -- Yes --> CH[Generate Section-by-Section]\n")
        f.write("  SZ -- No --> SO[Generate Full Report]\n")
        f.write("  CH --> MER[Merge Sections]\n")
        f.write("  SO --> REV[Review Agent]\n")
        f.write("  MER --> REV\n")
        f.write("  REV --> CF[Citation Formatter]\n")
        f.write("  CF --> FR[Final Markdown Report]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("start\n:Read Knowledge;\nif (Payload > 30k?) then (Yes)\n  :Generate Exec Summary;\n  :Generate Trends;\n  :Merge;\nelse (No)\n  :Generate Full;\nendif\n:Review;\n:Add Citations;\nstop\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nShows Adaptive Report Writing. To avoid exceeding context limits for Massive documents, `ReportWriterAgent` splits the task into structural loops (Executive Summary, Risks, etc.) and concatenates them before review.\n\n")
        f.write("### Short Description\nAdaptive structural document generation.\n\n")
        f.write("### Components Involved\n`ReportWriterAgent`, `ReviewAgent`, `CitationFormatterAgent`.\n\n")
        f.write("### Data Flow\nJSON Knowledge -> Section Iteration / Full Prompt -> Markdown -> Markdown with Footnotes.\n\n")
        f.write("### Failure Points\nLLM refuses to generate a specific section.\n\n")
        f.write("### Recovery Strategy\nAgent traps failure per section, skips it, and merges the rest, guaranteeing a partial report.\n\n")

        # --------------------------------------------------------
        # 11. FAULT TOLERANCE FLOW
        # --------------------------------------------------------
        f.write("## 11. FAULT TOLERANCE FLOW\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  subgraph External API Failure\n")
        f.write("  T[Tool Execution] --> F{Fails?}\n")
        f.write("  F -- Yes --> C[Catch Exception, Log]\n")
        f.write("  C --> CO[Continue without Tool]\n")
        f.write("  end\n")
        f.write("  subgraph LLM Failure\n")
        f.write("  L[Gemini Request] --> LF{Fails?}\n")
        f.write("  LF -- 429/503 --> FB[Fallback Model]\n")
        f.write("  FB --> L2{Fails?}\n")
        f.write("  L2 -- Yes --> LG[Log Error to GraphState]\n")
        f.write("  LG --> GD[Graceful Degradation]\n")
        f.write("  end\n")
        f.write("  subgraph Execution Timeout\n")
        f.write("  ND[Node Loop] --> TM{Time > 150s?}\n")
        f.write("  TM -- Yes --> BR[Break Loop / Stop Searches]\n")
        f.write("  BR --> SYN[Proceed to Synthesis]\n")
        f.write("  end\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("node Tool\nnode CatchBlock\nTool --> CatchBlock: Exception\nCatchBlock --> Tool: Proceed with others\nnode Gemini\nnode Fallback\nGemini --> Fallback: 429 Error\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nVisualizes the three pillars of resilience: Tool Isolation, LLM Model Failover (via LangChain fallbacks), and Global Execution Budget constraints (stopping loops preemptively).\n\n")
        f.write("### Short Description\nResilience and recovery diagrams.\n\n")
        f.write("### Components Involved\n`ResearchOrchestrator`, `GeminiService`, `nodes.py` (Timer checks).\n\n")
        f.write("### Data Flow\nErrors -> Catch -> Log via Monitor -> State modification or continuation.\n\n")

        # --------------------------------------------------------
        # 12. MONITORING FLOW
        # --------------------------------------------------------
        f.write("## 12. MONITORING FLOW\n\n")
        f.write("### Mermaid\n```mermaid\ngraph LR\n")
        f.write("  N[LangGraph Nodes] -->|log_node_start| MS[MonitoringService]\n")
        f.write("  GS[GeminiService] -->|log_llm_execution| MS\n")
        f.write("  RO[ResearchOrchestrator] -->|log_tool_execution| MS\n")
        f.write("  MS --> LOG[Terminal/Log Files]\n")
        f.write("  MS --> MET[Metrics Dictionary]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("component Nodes\ncomponent MonitoringService\nNodes -> MonitoringService: Push Telemetry\nMonitoringService -> Logs: Flush\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nThe `MonitoringService` acts as a central telemetry sink for node timings, LLM latencies, prompt sizes, and tool failures.\n\n")
        f.write("### Components Involved\n`MonitoringService`, `app/utils/logger.py`.\n\n")

        # --------------------------------------------------------
        # 13. COMPONENT DEPENDENCY DIAGRAM
        # --------------------------------------------------------
        f.write("## 13. COMPONENT DEPENDENCY DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  API[app/main.py] --> G[app/graph/builder.py]\n")
        f.write("  G --> N[app/graph/nodes.py]\n")
        f.write("  N --> A[app/agents/*.py]\n")
        f.write("  N --> S[app/services/*.py]\n")
        f.write("  A --> S\n")
        f.write("  A --> SC[app/schemas/*.py]\n")
        f.write("  A --> P[app/prompts/*.py]\n")
        f.write("  S --> T[app/tools/*.py]\n")
        f.write("  S --> U[app/utils/*.py]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("package API\npackage Graph\npackage Agents\npackage Services\npackage Schemas\npackage Tools\nAPI --> Graph\nGraph --> Agents\nGraph --> Services\nAgents --> Services\nAgents --> Schemas\nServices --> Tools\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nStrict hierarchical dependency graph ensuring no circular imports. Agents rely on Services, which rely on Utilities/Tools. Schemas and Prompts are leaf nodes.\n\n")

        # --------------------------------------------------------
        # 14. DIRECTORY STRUCTURE DIAGRAM
        # --------------------------------------------------------
        f.write("## 14. DIRECTORY STRUCTURE DIAGRAM\n\n")
        f.write("### Mermaid\n```mermaid\ngraph LR\n")
        f.write("  R[Root] --> B[backend/]\n")
        f.write("  B --> APP[app/]\n")
        f.write("  APP --> AG[agents/]\n")
        f.write("  APP --> AP[api/]\n")
        f.write("  APP --> CF[config/]\n")
        f.write("  APP --> GR[graph/]\n")
        f.write("  APP --> PR[prompts/]\n")
        f.write("  APP --> SC[schemas/]\n")
        f.write("  APP --> SV[services/]\n")
        f.write("  APP --> TL[tools/]\n")
        f.write("  APP --> UT[utils/]\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("folder backend {\n  folder app {\n    folder agents\n    folder services\n    folder graph\n  }\n}\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nVisual tree mapping of the Python FastAPI/LangGraph backend modular design.\n\n")

        # --------------------------------------------------------
        # 15. END-TO-END RUNTIME FLOW
        # --------------------------------------------------------
        f.write("## 15. END-TO-END RUNTIME FLOW\n\n")
        f.write("### Mermaid\n```mermaid\ngraph TD\n")
        f.write("  START((User Query)) --> QA[Understanding & Intent]\n")
        f.write("  QA --> ROUTE{Deep Research?}\n")
        f.write("  ROUTE -- No --> FAST[Fast LLM Reply] --> END((Response))\n")
        f.write("  ROUTE -- Yes --> PLAN[Planning & Task Splitting]\n")
        f.write("  PLAN --> LP[Parallel Search Loop]\n")
        f.write("  LP --> T1[Tool 1] & T2[Tool 2] & T3[Tool 3]\n")
        f.write("  T1 --> EV[Evidence Collection]\n")
        f.write("  T2 --> EV\n")
        f.write("  T3 --> EV\n")
        f.write("  EV --> HKS[Hierarchical Knowledge Synthesis]\n")
        f.write("  HKS --> INS[Insight Extraction]\n")
        f.write("  INS --> REP[Adaptive Report Generation]\n")
        f.write("  REP --> REV[Review & Citations]\n")
        f.write("  REV --> END\n")
        f.write("```\n\n")

        f.write("### PlantUML\n```plantuml\n@startuml\n")
        f.write("(*) --> Understanding\nUnderstanding --> Planning\nPlanning --> ParallelSearch\nParallelSearch --> Synthesis\nSynthesis --> ReportGeneration\nReportGeneration --> (*)\n")
        f.write("@enduml\n```\n\n")

        f.write("### Markdown Explanation\nThe absolute highest-level, most exhaustive representation of the complete pipeline processing a complex user request, highlighting parallel branches converging on synthesis.\n\n")
        f.write("### Components Involved\nEntire Backend Architecture.\n\n")
        f.write("### Data Flow\nRaw Text -> Structured Intent -> Array of Subtasks -> Array of Evidence Arrays -> Merged Knowledge Graph -> Sectioned Markdown -> Final Formatted Markdown.\n")
        
    print(f"Generated {filepath}")

if __name__ == '__main__':
    generate_docs()
