# Working on builder

Keep builder self-contained. User configuration and runtime state belong outside the plugin.

- Keep each skill independently usable and one accountable lead per managed project.
- Keep project coordination, session ownership, and terminal mechanics separate.
- Use generic examples and user-supplied paths.
- Do not launch sessions, change user configuration, or install the plugin merely for inspection.

## Instruction brevity

- Keep only useful preferences and non-obvious constraints that change a capable model's decisions. Trust model judgment and host rules; do not restate them.
- Give shared rules one owner. Justify added detail with a concrete need, measure substantial changes, and review outcomes rather than preservation of old clauses.
