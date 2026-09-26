# Loop Workspace Layout

```text
loop/                                                  # Installable orchestration skill
├── README.md                                          
├── SKILL.md                                           # Execution policy and orchestration diagrams creation
└── references/                                        # Orchestration guidelines
    ├── dependency-workflow-algorithm.md               # Worker tasks and DAG definition criteria, mermaid style conventions
    ├── dependency-diagram-example.md                  # Reference example of a worker-oriented dependency diagram
    ├── gantt-scheduling-algorithm.md                  # Executable DAG tasks distribution across Gantt time units
    ├── worker-memory-template.md                      # Expected structure and durable content for MEMORY.md
    └── worker-prompt-template.md                      # Expected orchestrator-to-worker prompt structure

.loop/                                                 # Repository-specific configuration
├── artifacts/                                         # Supporting rules, conventions, references, and context
│   ├── RULES.md                                       # General rules every orchestrator and worker MUST read
│   └── **/                                            
│       └── <context-document>.md                      # Any repository-specific supporting document
├── jobs/                                              # Shared reusable work definitions
│   └── **/<job-name>/
│       └── JOB.md                                     # Atomic work step with input, process, and output
└── orchestration/                                     # Isolated orchestration flows
    └── <flow-name>/                                   # One implementation, review, audit, or other flow
        ├── dependency-diagram.md                      # Shared worker ownership, outputs, and prerequisites
        ├── gantt-diagram.md                           # Optional full-flow execution plan
        ├── gantt-diagram.<scope>.md                   # Optional scoped execution plan sharing this flow's dependencies
        └── workers/                                   # Workers scoped to this orchestration flow
            └── worker-<number>-<responsibility>/
                └── MEMORY.md                          # Durable learnings for similar future worker instances
```
