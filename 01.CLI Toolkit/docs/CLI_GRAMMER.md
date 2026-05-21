# CLI Grammar Blueprint

Defines the command language used by the Automation CLI Runtime and all automation tools developed within the Automation Engineering Portfolio.

This document ensures command consistency, discoverability, and long-term extensibility across all automation domains.

---

## Purpose

The Automation CLI Runtime is designed as a unified execution layer for multiple automation capabilities.

Rather than exposing unrelated command styles per project, the system establishes a predictable command grammar that:

- reduces cognitive load for users
- enables intuitive command discovery
- supports future plugin-style tool integration
- allows consistent scripting and scheduling usage
- encourages muscle-memory driven terminal workflows
- mirrors the ergonomics of mature developer tooling ecosystems

Examples of inspiration include Git, kubectl, Terraform, and AWS CLI.

---

## Core Grammar Pattern

Commands should follow a consistent structure:

automation <domain> <verb> <object> [parameters]

Where:

- domain represents a capability area (runtime, api, etl, report, pipeline, etc.)
- verb represents an action (run, list, show, generate, inspect, etc.)
- object represents the target of the action (task, pipeline, source, template, etc.)

For simple runtime execution, the domain may be omitted:

automation run <task>

---

## Canonical Runtime Commands

These commands form the permanent foundation of the CLI runtime.

automation run <task>

automation tasks list
automation tasks describe <task>

automation runs list
automation runs show <task> <run_id>

These commands must remain stable across future system evolution.

---

## Domain Expansion Model

Future automation systems extend the CLI grammar through domains while preserving verb consistency.

### API Domain

automation api run aggregator  
automation api sources list  
automation api sources add  
automation api sources remove  
automation api inspect <source>

### ETL Domain

automation etl run <pipeline>  
automation etl pipelines list  
automation etl pipelines inspect  
automation etl step test  

### Reporting Domain

automation report generate kpi  
automation report templates list  
automation report preview  
automation report export  

### Scheduling Domain

automation schedule add  
automation schedule list  
automation schedule remove  

automation worker status  
automation worker run-now  

### Web Automation Domain

automation web run <job>  
automation web jobs list  
automation web record  
automation web inspect  

### Document Intelligence Domain

automation pdf extract  
automation pdf analyze  
automation pdf classify  
automation pdf batch-run  

### Monitoring Domain

automation monitor run  
automation monitor rules list  
automation monitor alerts show  
automation monitor health  

### Pipeline Orchestration Domain

automation pipeline run <name>  
automation pipeline simulate  
automation pipeline inspect  
automation pipeline artifacts  

### Risk Automation Domain

automation risk evaluate  
automation risk reports list  
automation risk dashboard  
automation risk alerts  

---

## Alias Strategy

Short aliases may be introduced for high-frequency commands to improve ergonomics.

Examples:

automation r <task> → run  
automation ls → runs list  
automation t ls → tasks list  

Aliases must never replace canonical commands.

Documentation, automation scripts, and CI usage should always rely on explicit command forms.

Aliases are considered optional usability enhancements.

---

## Parameter Strategy

Early runtime versions support parameter injection via key-value blobs:

automation run csvkpi -p "path=data.csv,limit=1000"

Future evolution may introduce:

- structured flags
- per-task parameter binding
- configuration templates
- environment-driven execution

Grammar stability must be preserved throughout parameter system evolution.

---

## Discoverability Rules

Every domain should support at least one of the following:

- list command
- describe or inspect command
- deterministic help output

Users must be able to explore capabilities directly from the CLI without external documentation.

---

## Extensibility Rules

New domains or commands must:

- preserve verb naming consistency
- avoid introducing novel grammar patterns unnecessarily
- integrate into existing execution philosophy
- avoid alias conflicts
- prioritize predictability over creativity

The CLI should feel like a natural extension of itself.

---

## Long-Term Vision

The Automation CLI Runtime is intended to evolve into a unified automation execution layer capable of:

- executing standalone automation tools
- orchestrating multi-step pipelines
- supporting scheduled and event-driven execution
- enabling monitoring and reporting workflows
- integrating externally developed automation modules

A stable CLI grammar is critical to achieving this vision.

## Current State

- CLI successfully executes all portfolio automation systems
- pipeline execution is validated across all integrated tools
- dynamic workflow composition is production-stable within current scope