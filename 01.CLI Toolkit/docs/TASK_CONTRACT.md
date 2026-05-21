# Task Contract

A task is a callable automation workload that can be executed by the CLI runtime.

## Required Interface

Each task must expose a callable using this shape:

def run(artifact_dir, params) -> TaskResult

## Inputs

- artifact_dir: pathlib.Path or path-like directory provided by the runtime for this run
- params: dict of parsed runtime parameters

## Outputs

Each task must return a TaskResult describing execution outcome.

TaskResult semantics:

- success = True → full success
- success = False → failure
- partial = True → degraded success

The runtime determines exit codes and lifecycle metadata from this result.

## Task Responsibilities

Tasks are responsible for:

- validating task-specific inputs
- interpreting runtime parameters
- executing workload logic
- handling task-level retries or resilience
- writing business artifacts into artifact_dir
- returning a meaningful execution message
- defining partial vs full success semantics when applicable

## Pipeline Compatibility

- tasks are validated across all portfolio systems for pipeline compatibility
- contract is proven stable across ingestion, transformation, evaluation, and reporting domains

## Runtime Responsibilities

The CLI runtime is responsible for:

- CLI parsing and command dispatch
- task registry and registry validation
- deterministic artifact run-directory creation
- execution lifecycle metadata writing
- execution duration measurement
- artifact retention policy enforcement
- exit code semantics
- run history inspection commands

## Constraints

- tasks must write artifacts only inside artifact_dir
- tasks must not create their own run root outside runtime control
- tasks must not duplicate global lifecycle behavior
- tasks must remain independently executable under the runtime contract

## Architectural Goal

This contract enables:

- independent task development
- future extraction of tasks into standalone automation tools
- runtime orchestration of externally developed tasks
- scheduler and pipeline integration without redesign