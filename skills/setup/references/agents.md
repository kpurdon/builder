# Worker readiness

Inspect the intended host's native watch and delegation capabilities before requiring a named agent. A host such as T3 may provide its own delegated tasks and completion notifications while using Codex as the underlying provider. Follow the host's selection, runtime inheritance, and completion rules. Named-role support and general worker support are separate capabilities.

Workers follow the shared [observation contract](../../monitor/references/observation.md). Verify the selected worker's actual model/options and access to the assigned read interface before relying on it; native tool availability in the owner does not prove worker access. Runtime tests remain within the user's requested setup scope. If no suitable native watch or worker is available, disclose a host-permitted local fallback.

## Codex named agents

Builder owns [watcher.toml](../../../agents/watcher.toml), including its model, reasoning effort, and worker instructions. Codex plugin installation does not register native agents. Use the bundled installer to copy the definition into the selected user `CODEX_HOME/agents` or trusted project's `.codex/agents` directory. Do not add agent paths to the plugin manifest or change global subagent defaults.

Run a read-only check from the installed Builder package:

```sh
python3 /path/to/builder/skills/setup/scripts/agents.py check --agents-dir /path/to/codex-home/agents
```

For an explicitly requested agent installation or update, run the same command with `install`. It creates the directory if needed, installs missing definitions, and updates unchanged Builder-managed files. Rerun after updating the plugin; upgrading a plugin alone does not refresh copied agent files. `check` reports `current`, `missing`, `stale`, `modified`, `unmanaged`, or `conflict`; only `current` passes. A fingerprint in the installed file links it to the bundled definition without depending on a versioned plugin-cache path.

Local edits, including model overrides, are preserved and reported as `modified`. Existing unmarked files and symlinks are also preserved. Show the local and bundled differences to the user for an explicit reconciliation; do not reset the fingerprint or overwrite edits to make a check pass. To replace a modified definition, move it to a user-selected backup location before installing the new one. An explicitly requested `remove` deletes only an unchanged managed definition; it preserves modified, unmarked, or symlinked files. Disabling or uninstalling the plugin does not automatically remove a separately installed agent.

### Codex runtime readiness

Check whether the host lists `watcher`. Run a test observation when troubleshooting or when asked to verify execution.

If named-role selection is unavailable, assess the host's other worker capabilities before falling back locally. Do not change runtime feature flags or silently substitute an expensive worker. For Codex named agents, check user and project scopes for a shadowing role when discovery or runtime settings differ from the installed definition.

Official references: [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents) and [plugin packaging](https://developers.openai.com/plugins/build/plugins#plugin-structure).
