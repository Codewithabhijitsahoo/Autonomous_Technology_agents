# Deep Technology Agents - Architecture & Execution Documentation

## 1. COMPLETE SYSTEM ARCHITECTURE

### Mermaid
```mermaid
graph TD
  U[User / Frontend] --> API[FastAPI]
  API --> LG[LangGraph Execution Engine]
  LG --> AG[Agents]
  LG --> SV[Services]
  AG --> SV
  SV --> TL[Tools]
  SV --> MR[Model Router]
  MR --> GM[Gemini Models]
  TL --> SA[Search APIs]
  API --> R[Response]
```

### PlantUML
```plantuml
@startuml
actor User
node Frontend
node FastAPI
node LangGraph
node Agents
node Services
node Tools
node ModelRouter
cloud GeminiModels
cloud SearchAPIs
User -> Frontend
Frontend -> FastAPI
FastAPI -> LangGraph
LangGraph -> Agents
LangGraph -> Services
Agents -> Services
Services -> Tools
Services -> ModelRouter
ModelRouter -> GeminiModels
Tools -> SearchAPIs
@enduml
```

### Markdown Explanation
The system follows a layered architecture where FastAPI receives requests and triggers the LangGraph state machine. LangGraph coordinates Agents and Services. Services interface with External Tools and Gemini Models (via a Model Router).

### Short Description
High-level topology of the Deep Technology Agents platform.

### Components Involved
Frontend, FastAPI, LangGraph, Agents, Services, Tools, Model Router, Gemini Models, Search APIs.

### Data Flow
User Input -> FastAPI -> LangGraph -> Agents -> Services -> Models/Tools -> Response.

### Failure Points
FastAPI overload, LangGraph state corruption, External API timeouts.

### Recovery Strategy
FastAPI rate limiting, State checkpointing, Service-level retry/circuit breakers.

## 2. LANGGRAPH EXECUTION GRAPH

### Mermaid
```mermaid
graph TD
  START((START)) --> QU[query_understanding_node]
  QU --> IR[intent_router_node]
  IR -- casual_chat_node --> CC[casual_chat_node]
  IR -- knowledge_answer_node --> KA[knowledge_answer_node]
  IR -- hypothesis_generation_node --> HG[hypothesis_generation_node]
  CC --> END((END))
  KA --> END
  HG --> PN[planner_node]
  PN --> TS[task_splitter_node]
  TS --> TR[tool_router_node]
  TR --> PR[parallel_research_tools_node]
  PR --> EC[evidence_collector_node]
  EC --> RM[reference_manager_node]
  RM --> FG[fusion_grounding_node]
  FG --> KS[knowledge_synthesis_node]
  KS --> IG[insight_generation_node]
  IG --> RW[report_writer_node]
  RW --> RR[response_relevance_node]
  RR --> RA[review_agent_node]
  RA --> CF[citation_formatter_node]
  CF --> END
```

### PlantUML
```plantuml
@startuml
(*) --> query_understanding_node
query_understanding_node --> intent_router_node
intent_router_node --> casual_chat_node
intent_router_node --> knowledge_answer_node
intent_router_node --> hypothesis_generation_node
casual_chat_node --> (*)
knowledge_answer_node --> (*)
hypothesis_generation_node --> planner_node
planner_node --> task_splitter_node
task_splitter_node --> tool_router_node
tool_router_node --> parallel_research_tools_node
parallel_research_tools_node --> evidence_collector_node
evidence_collector_node --> reference_manager_node
reference_manager_node --> fusion_grounding_node
fusion_grounding_node --> knowledge_synthesis_node
knowledge_synthesis_node --> insight_generation_node
insight_generation_node --> report_writer_node
report_writer_node --> response_relevance_node
response_relevance_node --> review_agent_node
review_agent_node --> citation_formatter_node
citation_formatter_node --> (*)
@enduml
```

### Markdown Explanation
Exact 1:1 mapping of `builder.py` edge definitions. Routes separate deep research from casual chat. The deep research path skips modular validation (duplicate detection, credibility scoring, etc.) for performance via a fast-path.

### Short Description
Visual representation of the LangGraph DAG state machine.

### Components Involved
All node functions in `nodes.py` and state configuration in `builder.py`.

### Data Flow
GraphState is passed linearly down the pipeline, accumulating arrays of data.

### Failure Points
Node execution errors interrupting the pipeline flow.

### Recovery Strategy
Graph-level checkpointing and internal exception catching (appending to `errors` array in GraphState).

## 3. COMPLETE EXECUTION FLOW

### Mermaid
```mermaid
sequenceDiagram
  actor User
  participant FastAPI
  participant LangGraph
  participant Nodes
  participant GeminiService
  participant Monitor
  User->>FastAPI: Query
  FastAPI->>LangGraph: invoke(GraphState)
  LangGraph->>Nodes: Execute Node
  Nodes->>Monitor: log_node_start(Budget Check)
  Nodes->>GeminiService: chat/structured_chat
  GeminiService->>GeminiService: Check Prompt Budget
  GeminiService->>GeminiService: Route Model (Flash/Pro)
  GeminiService-->>Nodes: LLM Response
  Nodes-->>LangGraph: Updated GraphState
  LangGraph-->>FastAPI: Final State
  FastAPI-->>User: Response
```

### PlantUML
```plantuml
@startuml
actor User
participant FastAPI
participant LangGraph
participant Nodes
participant GeminiService
participant MonitoringService
User -> FastAPI: Query
FastAPI -> LangGraph: Start Graph
LangGraph -> Nodes: Execute Node
Nodes -> MonitoringService: Check Budget & Log
Nodes -> GeminiService: Call LLM
GeminiService -> GeminiService: Apply Budgets & Route Model
GeminiService --> Nodes: Result
Nodes --> LangGraph: State Update
LangGraph --> FastAPI: Completion
FastAPI --> User: Result
@enduml
```

### Markdown Explanation
End-to-end execution flow emphasizing cross-cutting concerns like Monitoring, Execution Budget enforcement, and Prompt Budgets handled dynamically during Node execution.

### Short Description
Detailed sequential flow of an interaction.

### Components Involved
User, FastAPI, LangGraph, All Nodes, GeminiService, MonitoringService.

### Data Flow
Queries flow inward, execute via LLM routing, and cascade state updates backward.

### Failure Points
Execution Budget Timeout, Prompt size overflows.

### Recovery Strategy
Nodes preemptively exit loop if budget < 30s; GeminiService chunk-splits massive prompts automatically.

## 4. SEQUENCE DIAGRAM

### Mermaid
```mermaid
sequenceDiagram
  actor User
  participant Front as Frontend
  participant API as FastAPI
  participant LG as LangGraph
  participant QA as QueryUnderstandingAgent
  participant PA as PlannerAgent
  participant RO as ResearchOrchestrator
  participant T as Search Tools
  participant KS as KnowledgeSynthesisAgent
  participant RW as ReportWriterAgent
  participant GS as Gemini Models
  User->>Front: Enter query
  Front->>API: POST /research
  API->>LG: invoke(state)
  LG->>QA: understand_query()
  QA->>GS: structured_chat()
  GS-->>QA: Intent & Complexity
  QA-->>LG: state
  LG->>PA: generate_plan()
  PA->>GS: structured_chat()
  GS-->>PA: Plan
  PA-->>LG: state
  LG->>RO: execute_plan()
  RO->>T: run_tool_safely()
  T-->>RO: Raw Evidence
  RO-->>LG: state
  LG->>KS: synthesize()
  KS->>GS: structured_chat() / hierarchy
  GS-->>KS: KnowledgeGraph
  KS-->>LG: state
  LG->>RW: write_report()
  RW->>GS: invoke() [section-by-section]
  GS-->>RW: Markdown Report
  RW-->>LG: state
  LG-->>API: final_report
  API-->>Front: response
  Front-->>User: Display Report
```

### PlantUML
```plantuml
@startuml
actor User
participant Frontend
participant FastAPI
participant LangGraph
participant Agents
participant Tools
participant GeminiService
User -> Frontend: Query
Frontend -> FastAPI: HTTP
FastAPI -> LangGraph: Invoke
LangGraph -> Agents: Process
Agents -> GeminiService: Call LLM
GeminiService --> Agents: LLM Response
Agents -> Tools: Execute Search
Tools --> Agents: Search Results
Agents --> LangGraph: GraphState
LangGraph --> FastAPI: Report
FastAPI --> Frontend: Response
Frontend --> User: View
@enduml
```

### Markdown Explanation
A strict UML Sequence diagram showing synchronous and asynchronous interactions between distinct actors, software boundaries, and models.

### Short Description
End-to-end API interaction sequence.

### Components Involved
Frontend, API, Graph, Specific Agents, Tools, Gemini API.

### Data Flow
Request payload -> GraphState mutation -> Output payload.

### Failure Points
Network failures between Frontend/FastAPI or Tools.

### Recovery Strategy
Frontend retry mechanism; Tool isolated safe wrappers return empty/error statuses gracefully.

## 5. GRAPHSTATE DIAGRAM

### Mermaid
```mermaid
classDiagram
  class GraphState {
    +str query
    +list messages
    +str response
    +list steps
    +dict metadata
    +list errors
    +list sources
    +float execution_time
    +list subtask_evidence
    +dict structured_query
    +dict hypothesis_draft
    +dict grounded_draft
    +dict relevance_metrics
    +dict reference_map
    +list citations
    +list evidence_traceability
    +str intent
    +int research_score
    +str mode
    +dict research_plan
    +list tasks
    +list keywords
    +str domain
    +str complexity
    +list recommended_tools
    +list research_results
    +list completed_tools
    +list failed_tools
    +list raw_evidence
    +int evidence_count
    +dict tool_statistics
    +dict collection_metadata
    +list unique_evidence
    +list duplicate_groups
    +dict credibility_scores
    +list conflicts
    +dict confidence_scores
    +list validated_evidence
    +list discarded_evidence
    +dict validation_report
    +str validation_summary
    +dict knowledge
    +str executive_summary
    +list topic_summaries
    +list entities
    +list facts
    +list timelines
    +list relationships
    +list statistics
    +list terminology
    +dict knowledge_graph
    +list insights
    +list trend_analysis
    +list comparisons
    +list risks
    +list opportunities
    +list limitations
    +list future_research
    +list strategic_takeaways
    +str final_report
    +str reviewed_report
    +dict quality_scores
    +dict quality_report
    +str review_summary
    +list improvements
    +list issues_found
  }
```

### PlantUML
```plantuml
@startuml
class GraphState {
  +query
  +metadata
  +complexity
  +tasks
  +raw_evidence
  +knowledge
  +final_report
}
note right of GraphState: Passed linearly through all LangGraph nodes
@enduml
```

### Markdown Explanation
The `GraphState` is a Python `TypedDict` containing every state variable mapped via `operator.add` for lists or overwritten for strings/dicts. `query_understanding_node` sets `metadata`, `query`, `complexity`. `planner_node` sets `tasks`, `research_plan`. `parallel_research_tools_node` sets `subtask_evidence`, `raw_evidence`. `knowledge_synthesis_node` sets `knowledge`.

### Short Description
The immutable data structure driving the pipeline.

### Components Involved
`state.py`, all `nodes.py`.

### Data Flow
Passed explicitly into every async node function.

### Failure Points
Type mismatches if an agent returns unexpected JSON schemas.

### Recovery Strategy
Pydantic schema validation inside `GeminiService` forces strict compliance before appending to GraphState.

## 6. AGENT INTERACTION DIAGRAM

### Mermaid
```mermaid
graph LR
  Q[QueryUnderstandingAgent] --> I[IntentRouterAgent]
  I --> H[HypothesisGenerationAgent]
  H --> P[PlannerAgent]
  P --> RO[ResearchOrchestrator]
  RO --> E[EvidenceCollectorAgent]
  E --> RM[ReferenceManagerAgent]
  RM --> FG[FusionGroundingAgent]
  FG --> KS[KnowledgeSynthesisAgent]
  KS --> IN[InsightGenerationAgent]
  IN --> RW[ReportWriterAgent]
  RW --> RE[ResponseRelevanceAgent]
  RE --> RV[ReviewAgent]
  RV --> CF[CitationFormatterAgent]
```

### PlantUML
```plantuml
@startuml
agent PlannerAgent
agent EvidenceCollectorAgent
agent KnowledgeSynthesisAgent
agent ReportWriterAgent
PlannerAgent -> EvidenceCollectorAgent: Provides Search Tasks
EvidenceCollectorAgent -> KnowledgeSynthesisAgent: Provides Validated Evidence
KnowledgeSynthesisAgent -> ReportWriterAgent: Provides Structured Knowledge
@enduml
```

### Markdown Explanation
Shows the logical dependency chain between Agents. While they don't directly call each other's code (LangGraph mediates), their input/output shapes are inherently coupled.

### Short Description
Logical dependency mapping of all agents.

### Components Involved
All files in `app/agents/`.

### Data Flow
Agent -> LangGraph -> Agent.

### Failure Points
Agent hallucinates an output breaking downstream agent assumptions.

### Recovery Strategy
Downstream agents have strict schema parsers or fallback logic (e.g. ReportWriter returns a generic fallback if knowledge is empty).

## 7. SERVICE INTERACTION DIAGRAM

### Mermaid
```mermaid
graph TD
  AG[All Agents] --> GS[GeminiService]
  GS --> MS[MonitoringService]
  AG --> MS
  nodes --> RO[ResearchOrchestrator]
  RO --> ES[EvidenceService]
  RO --> MS
  nodes --> RDS[ResearchDecisionService]
```

### PlantUML
```plantuml
@startuml
component Agents
component GeminiService
component MonitoringService
component ResearchOrchestrator
Agents --> GeminiService: LLM inference
GeminiService --> MonitoringService: Log tokens/latency
Agents --> MonitoringService: Log node timing
@enduml
```

### Markdown Explanation
Highlights utility services shared across nodes. `GeminiService` handles all AI via a Model Router. `MonitoringService` acts as a global singleton capturing telemetry.

### Short Description
Dependencies between Agents and core Services.

### Components Involved
`app/services/*`.

### Data Flow
Agents pass string/schemas to Services, Services perform side-effects or network calls.

### Failure Points
Service singleton bottlenecks or thread safety (asyncio handles this natively).

### Recovery Strategy
Services wrap network calls in `try/except`.

## 8. MODEL ROUTER FLOW

### Mermaid
```mermaid
graph TD
  REQ[Incoming LLM Request] --> CL[Task Classification]
  CL -- Fast Tasks / Validation --> F[Gemini 2.5 Flash]
  CL -- Deep Reasoning / Complex --> P[Gemini 2.5 Pro]
  CL -- Very Complex Reports --> P3[Gemini 3 Pro / Deep Research]
  F --> PB[Prompt Budget Check]
  P --> PB
  P3 --> PB
  PB -- < 30k Tokens --> EX[Execute Model]
  PB -- > 30k Tokens --> SPLIT[Split Prompt into Chunks]
  SPLIT --> EX
  EX -- Success --> RES[Response]
  EX -- 429/503 --> FB[Fallback Model Trigger]
  FB --> EX
```

### PlantUML
```plantuml
@startuml
start
:Incoming LLM Request;
if (Task Type?) then (Fast/Validation)
  :Select Gemini 2.5 Flash;
elseif (Deep Reasoning)
  :Select Gemini 2.5 Pro;
else (Very Complex)
  :Select Gemini 3 Pro;
endif
if (Prompt > 30k Tokens?) then (Yes)
  :Split into Chunks;
else (No)
endif
:Execute Model;
if (Error?) then (Yes)
  :Trigger Fallback Model;
else (No)
endif
:Return Response;
stop
@enduml
```

### Markdown Explanation
The `route_model` in `GeminiService` assigns the optimal LLM based on task type and complexity parameter. It enforces token budgets and uses LangChain fallbacks for resiliency.

### Short Description
Dynamic intelligence routing.

### Components Involved
`GeminiService.route_model`, `GeminiService.chat`, `GeminiService.structured_chat`.

### Data Flow
Task Type/Complexity -> Model Selection -> Chunking -> API Call -> Fallback -> Result.

### Failure Points
All models in the fallback chain fail.

### Recovery Strategy
Raise exception, caught by Node execution wrapper, logs error to GraphState, pipeline degrades gracefully.

## 9. SEARCH PIPELINE

### Mermaid
```mermaid
graph TD
  PL[Planner Node / Task Splitter] --> OR[Research Orchestrator]
  OR --> W[Web Search]
  OR --> N[News Search]
  OR --> A[Arxiv Search]
  OR --> WK[Wikipedia Search]
  W --> EC[Evidence Collector]
  N --> EC
  A --> EC
  WK --> EC
  EC --> RM[Reference Manager]
```

### PlantUML
```plantuml
@startuml
component Orchestrator
component WebSearch
component ArxivSearch
component EvidenceCollector
Orchestrator -> WebSearch: Execute
Orchestrator -> ArxivSearch: Execute
WebSearch --> EvidenceCollector: Raw Data
ArxivSearch --> EvidenceCollector: Raw Data
@enduml
```

### Markdown Explanation
Tools are executed concurrently via `asyncio.gather` in `ResearchOrchestrator`. Tool selection is recommended by `PlannerAgent`. All raw output funnels into `EvidenceCollectorAgent` for normalization into `EvidenceItem` schemas.

### Short Description
Parallel data ingestion pipeline.

### Components Involved
`PlannerAgent`, `ResearchOrchestrator`, `tools/*`, `EvidenceCollectorAgent`.

### Data Flow
Queries -> Tools -> Array of dictionaries -> Normalization -> GraphState.

### Failure Points
Rate limits on APIs (e.g., DuckDuckGo, Arxiv).

### Recovery Strategy
Orchestrator staggers requests (delay logic) and uses `try/except` per tool. A failure in one tool does not kill the others.

## 10. REPORT GENERATION FLOW

### Mermaid
```mermaid
graph TD
  K[Knowledge / Insights] --> RW[Report Writer Agent]
  RW --> SZ{Payload > 30k chars?}
  SZ -- Yes --> CH[Generate Section-by-Section]
  SZ -- No --> SO[Generate Full Report]
  CH --> MER[Merge Sections]
  SO --> REV[Review Agent]
  MER --> REV
  REV --> CF[Citation Formatter]
  CF --> FR[Final Markdown Report]
```

### PlantUML
```plantuml
@startuml
start
:Read Knowledge;
if (Payload > 30k?) then (Yes)
  :Generate Exec Summary;
  :Generate Trends;
  :Merge;
else (No)
  :Generate Full;
endif
:Review;
:Add Citations;
stop
@enduml
```

### Markdown Explanation
Shows Adaptive Report Writing. To avoid exceeding context limits for Massive documents, `ReportWriterAgent` splits the task into structural loops (Executive Summary, Risks, etc.) and concatenates them before review.

### Short Description
Adaptive structural document generation.

### Components Involved
`ReportWriterAgent`, `ReviewAgent`, `CitationFormatterAgent`.

### Data Flow
JSON Knowledge -> Section Iteration / Full Prompt -> Markdown -> Markdown with Footnotes.

### Failure Points
LLM refuses to generate a specific section.

### Recovery Strategy
Agent traps failure per section, skips it, and merges the rest, guaranteeing a partial report.

## 11. FAULT TOLERANCE FLOW

### Mermaid
```mermaid
graph TD
  subgraph External API Failure
  T[Tool Execution] --> F{Fails?}
  F -- Yes --> C[Catch Exception, Log]
  C --> CO[Continue without Tool]
  end
  subgraph LLM Failure
  L[Gemini Request] --> LF{Fails?}
  LF -- 429/503 --> FB[Fallback Model]
  FB --> L2{Fails?}
  L2 -- Yes --> LG[Log Error to GraphState]
  LG --> GD[Graceful Degradation]
  end
  subgraph Execution Timeout
  ND[Node Loop] --> TM{Time > 150s?}
  TM -- Yes --> BR[Break Loop / Stop Searches]
  BR --> SYN[Proceed to Synthesis]
  end
```

### PlantUML
```plantuml
@startuml
node Tool
node CatchBlock
Tool --> CatchBlock: Exception
CatchBlock --> Tool: Proceed with others
node Gemini
node Fallback
Gemini --> Fallback: 429 Error
@enduml
```

### Markdown Explanation
Visualizes the three pillars of resilience: Tool Isolation, LLM Model Failover (via LangChain fallbacks), and Global Execution Budget constraints (stopping loops preemptively).

### Short Description
Resilience and recovery diagrams.

### Components Involved
`ResearchOrchestrator`, `GeminiService`, `nodes.py` (Timer checks).

### Data Flow
Errors -> Catch -> Log via Monitor -> State modification or continuation.

## 12. MONITORING FLOW

### Mermaid
```mermaid
graph LR
  N[LangGraph Nodes] -->|log_node_start| MS[MonitoringService]
  GS[GeminiService] -->|log_llm_execution| MS
  RO[ResearchOrchestrator] -->|log_tool_execution| MS
  MS --> LOG[Terminal/Log Files]
  MS --> MET[Metrics Dictionary]
```

### PlantUML
```plantuml
@startuml
component Nodes
component MonitoringService
Nodes -> MonitoringService: Push Telemetry
MonitoringService -> Logs: Flush
@enduml
```

### Markdown Explanation
The `MonitoringService` acts as a central telemetry sink for node timings, LLM latencies, prompt sizes, and tool failures.

### Components Involved
`MonitoringService`, `app/utils/logger.py`.

## 13. COMPONENT DEPENDENCY DIAGRAM

### Mermaid
```mermaid
graph TD
  API[app/main.py] --> G[app/graph/builder.py]
  G --> N[app/graph/nodes.py]
  N --> A[app/agents/*.py]
  N --> S[app/services/*.py]
  A --> S
  A --> SC[app/schemas/*.py]
  A --> P[app/prompts/*.py]
  S --> T[app/tools/*.py]
  S --> U[app/utils/*.py]
```

### PlantUML
```plantuml
@startuml
package API
package Graph
package Agents
package Services
package Schemas
package Tools
API --> Graph
Graph --> Agents
Graph --> Services
Agents --> Services
Agents --> Schemas
Services --> Tools
@enduml
```

### Markdown Explanation
Strict hierarchical dependency graph ensuring no circular imports. Agents rely on Services, which rely on Utilities/Tools. Schemas and Prompts are leaf nodes.

## 14. DIRECTORY STRUCTURE DIAGRAM

### Mermaid
```mermaid
graph LR
  R[Root] --> B[backend/]
  B --> APP[app/]
  APP --> AG[agents/]
  APP --> AP[api/]
  APP --> CF[config/]
  APP --> GR[graph/]
  APP --> PR[prompts/]
  APP --> SC[schemas/]
  APP --> SV[services/]
  APP --> TL[tools/]
  APP --> UT[utils/]
```

### PlantUML
```plantuml
@startuml
folder backend {
  folder app {
    folder agents
    folder services
    folder graph
  }
}
@enduml
```

### Markdown Explanation
Visual tree mapping of the Python FastAPI/LangGraph backend modular design.

## 15. END-TO-END RUNTIME FLOW

### Mermaid
```mermaid
graph TD
  START((User Query)) --> QA[Understanding & Intent]
  QA --> ROUTE{Deep Research?}
  ROUTE -- No --> FAST[Fast LLM Reply] --> END((Response))
  ROUTE -- Yes --> PLAN[Planning & Task Splitting]
  PLAN --> LP[Parallel Search Loop]
  LP --> T1[Tool 1] & T2[Tool 2] & T3[Tool 3]
  T1 --> EV[Evidence Collection]
  T2 --> EV
  T3 --> EV
  EV --> HKS[Hierarchical Knowledge Synthesis]
  HKS --> INS[Insight Extraction]
  INS --> REP[Adaptive Report Generation]
  REP --> REV[Review & Citations]
  REV --> END
```

### PlantUML
```plantuml
@startuml
(*) --> Understanding
Understanding --> Planning
Planning --> ParallelSearch
ParallelSearch --> Synthesis
Synthesis --> ReportGeneration
ReportGeneration --> (*)
@enduml
```

### Markdown Explanation
The absolute highest-level, most exhaustive representation of the complete pipeline processing a complex user request, highlighting parallel branches converging on synthesis.

### Components Involved
Entire Backend Architecture.

### Data Flow
Raw Text -> Structured Intent -> Array of Subtasks -> Array of Evidence Arrays -> Merged Knowledge Graph -> Sectioned Markdown -> Final Formatted Markdown.
