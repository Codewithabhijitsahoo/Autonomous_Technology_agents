import asyncio
import httpx
import json
import time
from rich.console import Console
from rich.panel import Panel

console = Console()
API_URL = "http://localhost:8000/api/chat"

async def run_test(name, query, expected_mode):
    console.print(f"\n[bold cyan]Starting Test:[/bold cyan] {name}")
    console.print(f"Query: '{query}'")
    
    start_time = time.time()
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(API_URL, json={"query": query})
            
            if response.status_code != 200:
                console.print(f"[bold red]Failed: HTTP {response.status_code}[/bold red]")
                console.print(response.text)
                return False
                
            data = response.json()
            duration = time.time() - start_time
            
            actual_mode = data.get("mode", "unknown")
            success = actual_mode == expected_mode
            
            if success:
                console.print(f"[bold green]Passed![/bold green] (Mode: {actual_mode}) in {duration:.2f}s")
                console.print(Panel(data.get("response", "")[:500] + "..."))
                return True
            else:
                console.print(f"[bold red]Failed Routing![/bold red] Expected {expected_mode}, got {actual_mode}")
                return False
                
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            return False

async def main():
    console.print("[bold yellow]Starting Deep Research Agent Integration Tests...[/bold yellow]")
    
    tests = [
        {
            "name": "Test 1: Casual Chat Routing",
            "query": "hi there! how are you?",
            "expected_mode": "casual_chat"
        },
        {
            "name": "Test 2: Knowledge Answer Routing",
            "query": "What is the capital of France and what is its population?",
            "expected_mode": "knowledge_answer"
        },
        {
            "name": "Test 3: Deep Research Routing",
            "query": "Provide a quick summary of recent advancements in solid-state batteries in 2023.",
            "expected_mode": "deep_research"
        }
    ]
    
    results = []
    for test in tests:
        res = await run_test(test["name"], test["query"], test["expected_mode"])
        results.append(res)
        await asyncio.sleep(2) # brief pause between tests
        
    console.print("\n[bold]Test Summary:[/bold]")
    for i, res in enumerate(results):
        status = "[green]PASS[/green]" if res else "[red]FAIL[/red]"
        console.print(f"Test {i+1}: {status}")

if __name__ == "__main__":
    asyncio.run(main())
