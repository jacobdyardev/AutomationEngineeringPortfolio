# External Tasks

This document defines how automation tasks developed outside the CLI Automation Toolkit repository integrate with the runtime.

The runtime is designed to execute independently developed automation workloads without owning their implementation.

## Execution Model

External automation tools must expose a runtime-compatible callable using the standard task contract:

def run(artifact_dir, params) -> TaskResult

The CLI runtime invokes this callable during task execution.

## Registration Strategy

External tasks must conform to the task contract, but are now discovered dynamically instead of manually registered.

## Runtime Responsibilities

The CLI runtime remains responsible for:

- command parsing and task dispatch
- deterministic artifact run-directory creation
- execution lifecycle metadata writing
- execution duration measurement
- artifact retention policy enforcement
- structured exit code semantics
- run history inspection commands

External tools must not attempt to replace or duplicate these behaviors.

## External Tool Responsibilities

External automation tools are responsible for:

- parameter validation and interpretation
- workload execution logic
- resilience and retry strategies
- writing business artifacts into the provided artifact directory
- returning a meaningful TaskResult outcome

Tools must remain compatible with the runtime execution contract.

## Artifact Constraints

External tools must:

- write artifacts only inside the provided run directory
- avoid creating independent runtime state outside the execution context
- produce deterministic outputs suitable for observability and debugging

## Architectural Goal

This integration model enables:

- independent automation tool development
- extraction of validated tasks into standalone projects
- runtime orchestration of externally packaged workloads
- future scheduler and pipeline integration without redesign

## Current State

- external plugin execution is validated
- tasks integrate into pipeline_runner
- artifact chaining works across internal + external tasks
- all portfolio automation systems operate as runtime-compatible external modules