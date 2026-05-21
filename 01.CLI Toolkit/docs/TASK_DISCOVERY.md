# Task Discovery Model

Defines how the Automation CLI Runtime locates, loads, and validates automation tasks.

This document establishes the long-term transition from manual task registration toward dynamic capability discovery.

---

## Purpose

The Automation CLI Runtime is intended to function as an execution platform for multiple independent automation tools.

Rather than permanently hard-coding task imports inside the runtime, the system will evolve toward structured task discovery that enables:

- modular tool development
- external automation plugin integration
- simplified portfolio project separation
- runtime extensibility without core modification
- cleaner long-term maintenance

This document defines the discovery philosophy and expected evolution path.

---

## Current Model (Manual Registry)

Early runtime versions use an explicit registry pattern.

Tasks are imported and registered manually:

TASKS = {
    "apiaggregator": apiaggregator,
    "dirinventory": dirinventory,
    "csvkpi": csvkpi,
}

This approach is intentionally simple and deterministic.

Advantages:

- clear execution behavior
- easy debugging
- minimal abstraction overhead
- fast architectural validation during early projects

This model is considered temporary.

---

## Transitional Goal

As automation tools mature into standalone projects, the runtime should no longer require direct source imports.

Instead, the runtime should be capable of discovering available tasks automatically.

This enables:

- independent project repositories
- runtime-as-platform architecture
- dynamic capability expansion
- easier packaging and distribution

---

## Future Discovery Mechanisms

Multiple discovery strategies may be introduced progressively.

### Filesystem-Based Discovery

Runtime scans predefined directories such as:

automation_tasks/
plugins/
external_tools/

Each valid module exposing a task contract becomes loadable.

This is expected to be the first discovery implementation.

---

### Entry Point Discovery

Tasks may later be distributed as installable Python packages exposing entry points.

Example concept:

automation.tasks = csvkpi_task = mypackage.csvkpi:run

This allows third-party automation tools to integrate into the runtime without modifying core code.

---

### Configuration-Based Registration

The runtime may optionally support configuration-driven task loading.

Example:

tasks.yaml

This enables controlled capability exposure in production environments.

---

## Task Validation During Discovery

All discovered tasks must pass runtime validation before registration.

Validation includes:

- callable verification
- parameter contract compliance
- deterministic execution expectations
- artifact lifecycle compatibility

Invalid tasks must be rejected gracefully.

Discovery must never compromise runtime stability.

---

## Naming Rules

Discovered task names must:

- remain short
- avoid symbols
- be CLI-friendly
- avoid collisions with existing domains or commands

Runtime should fail fast if name conflicts occur.

---

## Isolation Philosophy

Automation tasks should remain independent of runtime internal structure.

The runtime owns:

- execution lifecycle
- artifact management
- metadata tracking
- param enforcement
- scheduling integration

Tasks own:

- business logic
- external data interaction
- artifact content generation

Discovery must preserve this separation.

---

## Long-Term Vision

The Automation CLI Runtime is expected to evolve into a capability host that:

- dynamically loads automation tools
- orchestrates multi-domain workflows
- integrates scheduling and monitoring systems
- supports external plugin ecosystems
- enables scalable automation portfolio demonstration

Dynamic task discovery is a foundational step toward this platform architecture.

## Current State

- dynamic discovery is stable
- external plugin execution is validated
- pipeline execution integrates discovered tasks
- all portfolio automation systems are successfully discoverable and executable via runtime