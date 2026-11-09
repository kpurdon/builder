# Native agents

Builder owns [watcher.toml](../../../agents/watcher.toml), including its model, reasoning effort, and worker instructions. Codex plugin installation does not register native agents. Use the bundled installer to copy the definition into the selected user `CODEX_HOME/agents` or trusted project's `.codex/agents` directory. Do not add agent paths to the plugin manifest or change global subagent defaults.

Run a read-only check from the installed Builder package:

```sh
python3 /path/to/builder/skills/setup/scripts/agents.py check --agents-dir /path/to/codex-home/agents
```

For an explicitly requested agent installation or update, run the same command with `install`. It creates the directory if needed, installs missing definitions, and updates unchanged Builder-managed files. Rerun after updating the plugin; upgrading a plugin alone does not refresh copied agent files. `check` reports `current`, `missing`, `stale`, `modified`, `unmanaged`, or `conflict`; only `current` passes. A fingerprint in the installed file links it to the bundled definition without depending on a versioned plugin-cache path.

Local edits, including model overrides, are preserved and reported as `modified`. Existing unmarked files and symlinks are also preserved. Show the local and bundled differences to the user for an explicit reconciliation; do not reset the fingerprint or overwrite edits to make a check pass. To replace a modified definition, move it to a user-selected backup location before installing the new one. An explicitly requested `remove` deletes only an unchanged managed definition; it preserves modified, unmarked, or symlinked files. Disabling or uninstalling the plugin does not automatically remove a separately installed agent.

## Runtime readiness

File installation is not runtime proof. Start a fresh session in the intended client and verify that its native spawn tool exposes named roles and discovers `watcher`. Test selection by role name, without explicit model or effort overrides, then verify the child's runtime model and effort against the installed TOML. Use a bounded synthetic wait before relying on monitoring. A role name or agent self-report is not sufficient evidence.

Some clients expose only explicit model overrides and no named-role selector. Mark named-agent monitoring unavailable there; do not copy model parameters into skill prose, silently substitute a generic agent, or change runtime feature flags. The owner may run the bounded helper locally with a disclosed fallback. Check user and project scopes for a shadowing role when discovery or runtime settings differ from the installed definition.

Official references: [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) and [plugin packaging](https://developers.openai.com/plugins/build/plugins#plugin-structure).
