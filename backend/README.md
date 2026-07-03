# Deep Research Agent Backend

This is the backend architecture for a production-grade Deep Research Agent. It is an advanced, autonomous AI research system powered by a multi-agent architecture. It takes a user query, formulates a comprehensive research plan, parallelizes data gathering across multiple search modalities, and rigorously evaluates the evidence before synthesizing a final, reviewed report.

## System Workflow Diagram

The system utilizes a state graph (LangGraph) to orchestrate various specialized AI agents and tools. Below is the workflow diagram illustrating how a user query traverses through the system:

```mermaid
graph TD
    %% Define styles
    classDef agent fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef tool fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px;
    classDef process fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef endpoint fill:#fff3e0,stroke:#ff9800,stroke-width:2px,rx:20px,ry:20px;

    %% Nodes
    Start([User Query]) ::: endpoint
    Planner[Planner Agent] ::: agent
    Orchestrator{Research Orchestrator} ::: process
    
    WebSearch[Web Search<br>Tavily / DDG] ::: tool
    NewsSearch[News Search<br>DDG] ::: tool
    ArxivSearch[Arxiv Search] ::: tool
    WikiSearch[Wikipedia Search] ::: tool
    
    Collector[Evidence Collector] ::: process
    Dedup[Duplicate Detection] ::: agent
    Credibility[Source Credibility] ::: agent
    Conflict[Conflict Detection] ::: agent
    Scoring[Confidence Scoring] ::: agent
    Validation[Validation Coordinator] ::: process
    Synthesis[Knowledge Synthesis] ::: agent
    Insights[Insight Generation] ::: agent
    Report[Report Writer] ::: agent
    Review[Review Agent] ::: agent
    Output([Final Reviewed Report]) ::: endpoint

    %% Edges
    Start --> Planner
    Planner -- Generates Plan & Keywords --> Orchestrator
    
    Orchestrator --> WebSearch
    Orchestrator --> NewsSearch
    Orchestrator --> ArxivSearch
    Orchestrator --> WikiSearch
    
    WebSearch --> Collector
    NewsSearch --> Collector
    ArxivSearch --> Collector
    WikiSearch --> Collector
    
    Collector -- Normalizes Data --> Dedup
    Dedup --> Credibility
    Credibility --> Conflict
    Conflict --> Scoring
    Scoring --> Validation
    Validation -- Discards Invalid Data --> Synthesis
    Synthesis -- Builds Knowledge Graph --> Insights
    Insights --> Report
    Report --> Review
    Review --> Output
```

## How It Works

1. **Planner Phase**: The **Planner Agent** analyzes the initial user query to understand the complexity, extract keywords, and recommend the best tools for the job.
2. **Parallel Research**: The **Research Orchestrator** fires off concurrent requests to multiple search tools:
   * **Web Search**: Uses Tavily (with a DuckDuckGo fallback).
   * **News Search**: Fetches recent articles via DuckDuckGo News.
   * **Arxiv Search**: Retrieves academic and scientific papers.
   * **Wikipedia Search**: Gathers verified, encyclopedic summaries.
3. **Evidence Processing**: The **Evidence Collector** normalizes the raw data. The data then passes through a rigorous gauntlet of agents:
   * **Duplicate Detection**: Merges redundant information.
   * **Source Credibility**: Evaluates the trustworthiness of the source.
   * **Conflict Detection**: Identifies contradictory evidence across sources.
   * **Confidence Scoring**: Assigns a reliability score based on credibility and conflicts.
   * **Validation**: The **Validation Coordinator** filters out low-confidence or highly contradictory data.
4. **Synthesis & Writing**: 
   * The **Knowledge Synthesis Agent** maps the validated evidence into a cohesive structure.
   * The **Insight Generation Agent** looks for trends, risks, and strategic takeaways.
   * The **Report Writer** drafts the final response.
5. **Review Phase**: Finally, the **Review Agent** grades the report for quality, suggesting improvements or catching potential hallucinations before presenting it to the user.

## Project Structure

The project follows a modular, scalable architecture with clear separation of concerns:

- `app/api/`: FastAPI route handlers (endpoints)
- `app/agents/`: LLM agents (e.g., Planner, Search, Validator)
- `app/graph/`: LangGraph workflow definitions
- `app/services/`: Core business logic and orchestration
- `app/tools/`: Custom tools for agents (e.g., search, scraper, PDF reader)
- `app/prompts/`: LLM system prompts and templates
- `app/schemas/`: Pydantic models for data validation
- `app/config/`: Configuration management using Pydantic Settings
- `app/middleware/`: FastAPI middleware (e.g., rate limiting, auth)
- `app/utils/`: Shared utilities (e.g., logger)

## Setup

1. Configure your `.env` file with `GOOGLE_API_KEY` and `TAVILY_API_KEY`.
2. Activate your virtual environment
3. Install requirements: `pip install -r requirements.txt`
4. Run the server: `uvicorn app.main:app --reload`
