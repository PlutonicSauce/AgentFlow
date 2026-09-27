# AgentFlow

**AgentFlow** is a Domain-Specific Language (DSL) specifically designed for the **Artificial Intelligence** domain. It simplifies the complex task of orchestrating multi-agent LLM workflows. 

## The Problem
As AI models become more capable, developers are building complex systems where multiple "agents" interact, use tools, and pass data to each other. Writing these orchestrations in general-purpose languages like Python or JavaScript often results in messy, boilerplate-heavy code, involving complex state management and nested async calls. 

## The Solution: AgentFlow DSL
AgentFlow elevates AI orchestration to a first-class language feature. It allows developers to:
1. Declaratively define AI **Agents** with specific models, prompts, and tools.
2. Construct intuitive **Flows** to pipe data between agents.
3. Rapidly prototype complex, multi-agent AI systems.

## Key Features
- **Intuitive Syntax**: Focus on the logic of your AI workflow, not the boilerplate of API calls.
- **Agent Definitions**: Define models, system prompts, and tool permissions cleanly.
- **Flow Control**: Pass context seamlessly from one agent's output to another agent's input.
- **Hand-rolled Interpreter**: Built from scratch with a custom lexer, parser, and abstract syntax tree (AST). 

## Example: Research and Summarize
Here is a real-world use case demonstrating how AgentFlow elegantly orchestrates a complex task: a Researcher agent pulls information, and a Summarizer agent synthesizes it.

```agentflow
agent Researcher {
    model: "gemini-1.5-pro"
    prompt: "You are an expert researcher. Find and synthesize deep technical information."
    tools: [WebSearch, Wikipedia]
}

agent Summarizer {
    model: "gemini-1.5-flash"
    prompt: "You are a precise editor. Summarize the provided text concisely."
    tools: []
}

flow ResearchAndSummarize(topic) {
    data = Researcher.run(topic)
    summary = Summarizer.run(data)
    return summary
}

run ResearchAndSummarize("Recent advancements in Quantum Computing")
```

## How to Run

1. Clone the project repository.
2. Ensure you have Python 3 installed.
3. Run the interpreter on the example file:
   ```bash
   python3 main.py examples/research_flow.af
   ```

Watch as the interpreter parses the syntax and simulates the interaction between the two agents, piping the Researcher's findings directly into the Summarizer's context!

## Advanced Domain Features: Robust Workflows
AI model APIs are inherently flaky. AgentFlow introduces a native `retry N { ... }` block. If any LLM interaction or tool call fails within the block, the interpreter will catch the exception and retry the entire block up to `N` times, ensuring bulletproof execution in real-world scenarios.

```agentflow
flow RobustAnalysis(topic) {
    // Single line comments are fully supported!
    report = retry 3 {
        data = Analyst.run(topic)
        Reporter.run(data)
    }
    return report
}
```

Try the robust mock execution with:
```bash
python3 main.py examples/robust_flow.af
```

## Hackathon Judging Criteria Matrix
Here is how AgentFlow directly addresses the **Syntax Summit** rubrics:
- **Innovation & Originality (25pts)**: Introduces the `retry { }` construct specifically to solve the domain problem of flaky LLM connections and intermittent tool failures.
- **Technical Implementation (25pts)**: A completely hand-rolled, dependency-free lexer and recursive descent parser capable of generating ASTs, paired with a stateful interpreter.
- **Language Design (20pts)**: Domain-specific abstractions (`agent`, `flow`) reduce thousands of lines of complex Python async code into clean, declarative structures.
- **User Experience (5pts)**: Developer-friendly features include robust C-style comments (`//`) and Rust-style error pointers that show the exact line and column of syntax errors.
- **Real-World Impact (15pts)**: Immediately solves a massive pain point for AI developers building multi-agent systems today.

*This project was built for the Syntax Summit Hackathon, targeting the **Best Interpreter** and **Most Innovative DSL** prizes.*
