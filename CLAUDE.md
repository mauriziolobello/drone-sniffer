# CLAUDE.md — Drone Packet Sniffer & Injector

## Language
All text in this project must be written in **English**: documentation, code comments,
docstrings, CLI messages, and log output. No exceptions.

## Code language
All code is written in **Python** (≥ 3.10).
Do not introduce other languages without explicit approval.

## Architectural principles — SOLID (mandatory)
Every module, class and function must strictly follow the SOLID principles:

- **S — Single Responsibility**: each class/module has a single responsibility.
  Examples: `sniffer.py` captures only; `parser.py` analyses only; `injector.py` crafts/sends only.
- **O — Open/Closed**: code is open for extension (new drone profiles), closed for modification of the core.
  The profile system (`src/profiles/`) is the designated extension point.
- **L — Liskov Substitution**: profiles must be interchangeable.
  Every profile must expose the same interface (`parse()`, `get_predefined_command()`).
- **I — Interface Segregation**: do not force profiles to implement methods they do not use.
  Prefer small, specific interfaces over monolithic ones.
- **D — Dependency Inversion**: high-level modules (`parser`, `injector`) must not depend on
  concrete profiles. Depend on abstractions (ABC or `typing.Protocol`).

## Testing
- Use `pytest`. Always start with deterministic cases (fixed-byte parsing, checksums).
- No physical hardware dependency in tests: hex payloads are hardcoded in fixtures.
- Suggest tests before implementing a feature (TDD).

## Tech stack
- `scapy` — sniffing and packet crafting.
- `colorama` — coloured terminal output.
- `pytest` — unit and integration tests.

## Conventions
- Short docstrings only when the "why" is not obvious from the code.
- No comments that describe the "what" — names already do that.
- Avoid `isinstance()` / `if profile_name == "..."`: prefer dispatch via polymorphic objects.
