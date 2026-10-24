# Changelog

## 1.2.0 — 2026-10-24

- Merged [PR #2](https://github.com/rihokirss/codex-loupedeck-controller/pull/2) by **bradsour**, adding four-page Loupedeck Live S support and a backup/conflict-aware Codex keybinding installer.
- Voice Chat: CT round button 8; Live S bottom-dial press. The touchscreen Dictate button still uses Windows Voice Typing.
- Native insert-only text actions now retain stable custom-icon IDs, avoiding stock clipboard icons after import/conversion.
- Refreshed all four CT README screenshots from the real Loupedeck configuration view; kept the complete CT and Live S overview diagrams.
- Corrected the CT shortcut reference for round button 8 and added package/reference/icon validation for both devices.

### Validation

Both packages build and pass `tools/validate_packages.py`: four pages, complete icon coverage, 22 native text actions, 37 shortcut actions, resolved control references and nine unique keybindings. The keybinding installer preserves unrelated bindings and refuses a conflicting target without modifying it.

The CT configuration view was inspected on the installed device profile. Voice Chat activation still needs a physical test after restarting Codex to load the added shortcut. Full Live S hardware testing remains the contributor's/manual checklist; this release does not claim that every Live S action was exercised on this machine.

### Install

Choose the LP4 for your device. Download/extract the source-code ZIP as well to obtain `src/codex-keybindings.json` and `tools/install-codex-keybindings.ps1` in their expected folders. Back up your profiles, run the shortcut installer, import the device profile and restart Codex once. See [README.md](README.md) for the full instructions.
