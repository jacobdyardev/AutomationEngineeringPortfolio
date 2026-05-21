# Universal Web Automation Framework — Context

## Program Context

The Universal Web Automation Framework is a modular automation system integrated into the CLI Automation Toolkit.

It is designed as a config-driven execution engine for web data extraction, supporting multiple scraping strategies and structured data output.

The framework replaces one-off scrapers with a unified system capable of adapting to different sites through configuration and layered execution.


## Core Capability

- Execute web scraping tasks via CLI
- Support config-driven scraping behavior
- Support multiple fetch strategies (static, browser-ready)
- Extract structured data using selector + field configuration
- Produce deterministic JSON artifacts
- Integrate into pipeline execution with artifact chaining


## Architectural Model

The framework is built as a layered system:

### Strategy Layer

Controls how content is fetched.

- Static fetch (requests)
- Browser fetch (planned)
- Session / cookie-based fetch (planned)
- Stealth / anti-bot behavior (planned)


### Extraction Layer

Controls how data is parsed.

- CSS selector extraction
- Field configuration parsing
- Attribute extraction (text, href, etc.)
- Nested extraction support


### Crawl Layer

Controls traversal behavior.

- Pagination (planned)
- Detail page crawling (planned)
- Infinite scroll (planned)


### Reliability Layer

Controls execution stability.

- Retry logic (planned integration)
- Delay / rate control (planned)
- Failure visibility (HTML dump, screenshot planned)


### Config Layer

Controls system behavior.

- CLI parameter input
- TOML / JSON config profiles
- No hardcoded site logic


## Execution Model

task.py  
→ load config (file or params)  
→ run_engine(config)  
→ write artifact output  
→ return TaskResult  

The engine orchestrates execution but does not implement scraping logic.


## Architectural Constraints

- No site-specific conditional logic
- All behavior must be config-driven
- Engine layer must remain orchestration-only
- Tasks must return structured, deterministic output
- Partial failures must not terminate execution when avoidable


## Output Expectations

All executions produce structured records:

[
  {
    "field": "...",
    "value": "...",
    "source": "..."
  }
]

Artifacts are written to timestamped directories consistent with CLI runtime standards.


## Current Capability

- Static HTML scraping (requests-based)
- Selector-based element extraction
- Field configuration parsing
- JSON artifact generation
- CLI task integration
- Pipeline compatibility


## System Position

The framework operates as a standard automation plugin within the CLI runtime.

- Fully compatible with pipeline_runner
- Supports dynamic pipeline execution via `steps`
- Produces artifacts consumable by downstream systems (ETL, KPI, reporting)


## Evolution Path

The system will expand through validated capability additions:

Phase 2:
- Pagination handling
- Detail page crawling

Phase 3:
- Browser-based scraping (Playwright)
- JavaScript-rendered page support

Phase 4:
- Session handling (cookies, login flows)
- Retry + delay integration

Phase 5:
- Proxy support
- Stealth / anti-bot enhancements


## Engineering Doctrine Alignment

- No monolithic scrapers
- No per-site hardcoding
- Behavior defined through configuration
- System evolves through real execution use cases


## Summary

The Universal Web Automation Framework is a config-driven scraping engine integrated into the CLI Automation Toolkit.

It provides a structured, extensible approach to web data extraction, enabling rapid adaptation to new targets without rewriting core logic.