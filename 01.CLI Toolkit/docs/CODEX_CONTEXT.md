# CLI Automation Toolkit — System Context

## Core Philosophy

The toolkit provides a deterministic CLI-driven automation execution model.

Automation tools are executed via structured commands and produce predictable artifacts.

The system evolves through integration of real automation workloads.

Clarity and extensibility are prioritized over feature density.

---

## Architectural Verification

- CLI runtime and automation systems co-evolve
- Implementation is driven by real execution needs
- Premature platform abstraction is avoided
- Toolkit abstractions emerge from validated workloads

Canonical execution entrypoint:

automation run <taskname>

---

## Primary Responsibilities

The toolkit must:

- Provide CLI execution for automation tasks
- Support modular task registration via dynamic discovery
- Support parameter-driven execution
- Produce deterministic artifacts
- Return structured execution results

---

## Architectural Expectations

- CLI command routing remains minimal
- Automation logic is isolated from CLI parsing
- Tasks are independently executable modules
- Execution lifecycle is centralized
- Runtime discovery is filesystem-based

Pipeline expectations:

- Sequential execution with artifact chaining
- Downstream tasks receive upstream artifact paths automatically
- Dynamic pipeline execution via `steps` parameter is supported
- Tasks must accept upstream artifact input via params

Separation of responsibilities:

data generation → apiaggregator  
data transformation → mini_etl  
data evaluation → risk_kpi  
data presentation → excel_kpi  

---

## Runtime Observability & Introspection Layer

- Each execution produces a timestamped artifact directory
- Metadata includes status, duration, parameters, and outputs
- CLI supports:

  - automation tasks list
  - automation tasks describe
  - automation runs list
  - automation runs show

- Pipeline execution logs step-level boundaries
- Partial success does not terminate execution
- Artifact chaining is traceable across pipeline stages

---

## Implementation Notes

- Avoid monolithic scripts
- Prefer simple abstractions
- Maintain deterministic outputs
- Avoid hardcoded paths
- Preserve structure integrity

Data handling:

- Structured data must be flattened before presentation layers
- Outputs must remain compatible across pipeline stages
- Tasks must tolerate partial upstream failures

---

## Execution Protocol

Before changes:

- Review task interfaces and structure
- Maintain CLI → task separation
- Validate cross-task compatibility
- Avoid breaking contracts

Post-change:

- report modified files
- describe behavior changes
- identify edge cases

---

## Foundation Role

The toolkit now supports:

- Data ingestion systems
- ETL transformation pipelines
- Rule-based evaluation engines
- Reporting and visualization systems
- Dynamic workflow composition

---

## Current System State

The CLI runtime and all automation plugins are fully functional and integrated.

Validated systems:

- Async API Aggregator
- Mini ETL Pipeline Engine
- Excel KPI Reporting
- Scheduler + Worker System
- Web Automation Framework
- PDF Intelligence Processor
- Data Monitoring System
- End-to-End Pipeline
- Risk KPI Automation Engine

All systems:

- execute via CLI
- integrate into pipelines
- conform to task contract
- produce deterministic outputs

System evolution:

CLI runtime → modular task system → pipeline execution engine → automation platform

---

## Constraints

- Do not introduce orchestration/scheduling layers
- Maintain modularity and task independence
- Preserve deterministic execution model