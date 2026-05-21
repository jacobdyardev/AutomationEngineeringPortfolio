# Automation Engineering Portfolio

Modular Python CLI automation framework supporting configurable end-to-end pipelines through reusable plugin modules that can be combined into custom workflows for ETL, web automation, reporting, monitoring, and async processing.

## Demonstration

Example configurable workflow:

```text
API Aggregator
        ↓
Mini ETL
        ↓
Data Inspector
        ↓
Risk KPI
        ↓
Excel KPI Generator
```

Example execution:

```bash
auto run pipeline_runner -p "steps=api_aggregator|mini_etl|risk_kpi|excel_kpi"
```

## Key Features

- Fully modular CLI runtime architecture
- Configurable end-to-end pipelines
- Plugin-based task system
- Async API aggregation
- Config-driven ETL processing
- Excel KPI reporting
- Web automation framework support
- Structured artifact generation
- Runtime observability and monitoring

## Architecture

```text
api_aggregator
      ↓
mini_etl
      ↓
data_inspector
      ↓
risk_kpi
      ↓
excel_kpi
```

## Portfolio Modules

| Module | Purpose |
|----------|----------|
| CLI Toolkit | Core runtime and execution layer |
| Async API Aggregator | Multi-source asynchronous ingestion |
| Mini ETL Pipeline | Data transformation and normalization |
| Excel KPI Generator | Reporting and exports |
| Scheduler + Worker System | Background execution |
| Universal Web Automation Framework | Configurable scraping |
| PDF Intelligence Processor | Document workflows |
| Data Monitoring System | Observability |
| End-to-End Pipeline | Full workflow orchestration |
| Risk KPI Engine | Rule-based evaluation |

---

## Technical Reference


### CLI Automation Toolkit — Usage & Command Reference


## Program Context

This document defines the command structure, plugin capabilities, and parameter system for the CLI Automation Toolkit runtime.

The CLI serves as the execution layer for all automation plugins and supports both single-task execution and dynamic pipeline workflows.


## Command Model

All execution is performed through the CLI runtime using:

auto run <task_name> -p "key=value,key=value"

Parameters are passed as a single string and parsed at runtime.


## Core Commands

### Execute Task

auto run <task_name> -p "key=value,key=value"

Runs a single automation task with provided parameters.


### Execute Pipeline

auto run pipeline_runner -p "steps=task1|task2|task3,key=value"

Runs multiple tasks sequentially.

Tasks are executed in order and share parameters.

- additional parameters can be appended using comma-separated key=value pairs


### List Tasks

auto tasks list

Displays all registered tasks discovered by the runtime.


### List Runs

auto runs list <task_name>

Displays historical executions for a task.


### Inspect Run

auto runs show <task_name> <run_id>

Displays execution details and artifacts for a specific run.


## Parameter System

Parameters follow this structure:

-p "key=value,key=value"

Rules:

- comma separates parameters
- equals assigns values
- pipe (|) separates pipeline steps
- parameters are globally accessible to all pipeline steps


## Pipeline Behavior

- steps are defined using the `steps` parameter
- execution is sequential
- downstream tasks receive upstream artifact paths
- pipeline continues on partial success
- pipeline fails on critical errors


## Plugin Overview

The system includes multiple automation plugins integrated into the CLI runtime.

All plugins:

- execute via CLI
- conform to the task contract
- produce deterministic artifacts
- support pipeline execution


### api_aggregator

Purpose:

Fetch data from multiple APIs asynchronously.

Parameters:

- apis_file → JSON file defining API endpoints
- retries → number of retry attempts

Behavior:

- loads API definitions from file
- performs async requests
- aggregates responses into structured JSON


### mini_etl

Purpose:

Perform extraction, transformation, and output formatting.

Parameters:

- input_path → input JSON file
- output_format → json, csv, excel
- output_mode → wide, grouped, sheets (excel only)
- fields → comma-separated fields to keep
- rename → mapping old:new
- metrics → count, sum
- mapping_file → TOML extraction configuration

Behavior:

- normalizes input data
- applies extraction layer (TOML)
- transforms structure
- computes metrics
- outputs formatted results


### excel_kpi

Purpose:

Generate formatted Excel reports.

Features:

- column auto-sizing
- status-based coloring
- filtering
- multiple output modes


### risk_kpi

Purpose:

Evaluate structured data using rule-based logic.

Used for:

- scoring
- validation
- KPI evaluation


### data_inspector

Purpose:

Inspect and evaluate data structures.

Features:

- nested field access
- rule evaluation
- debugging support


### csv_kpi

Purpose:

Process CSV datasets and compute KPI metrics.


### dir_inventory

Purpose:

Scan directories and output structured file inventory.


## Extraction Layer (mini_etl)

Extraction is defined using a TOML configuration file.

Example:

[random_user]
first_name = "results.0.name.first"
email = "results.0.email"

Behavior:

- maps nested JSON to structured fields
- defines output schema before transformation


## Output Modes (Excel)

### wide

- single table
- all fields combined
- best for consistent schemas


### grouped

- per-source sections
- repeated headers per group
- optimized for readability


### sheets

- one sheet per source
- strict data separation
- best for large datasets


## Architecture Flow

api_aggregator → mini_etl → data_inspector → risk_kpi → excel_kpi


## Responsibilities

- aggregation → data ingestion
- etl → transformation and normalization
- inspection → validation
- kpi → evaluation
- output → reporting


## Artifact System

Artifacts are generated per execution:

artifacts/<task>/<timestamp>/

Each run includes:

- processed data
- metrics (if applicable)
- execution metadata


## Execution Guarantees

- deterministic outputs
- structured artifact storage
- consistent parameter handling
- standardized task contract


## System Capability

The CLI supports:

- modular plugin execution
- dynamic pipeline composition
- config-driven data processing
- flexible output formatting
- structured automation workflows


## Example Execution

auto run pipeline_runner -p "steps=api_aggregator|mini_etl|excel_kpi,apis_file=ExampleAPI.json,mapping_file=mapping.toml,output_format=excel,output_mode=grouped"
