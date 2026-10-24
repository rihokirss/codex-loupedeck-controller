# Codex custom shortcuts

The installed Codex Windows app exposes Reasoning, Plan, and Fast as configurable commands, but does not list them in the Command Menu. The Loupedeck profile therefore sends these direct shortcuts:

| Codex command | Custom shortcut | Loupedeck controls |
|---|---|---|
| Decrease reasoning effort | `Ctrl+Alt+Shift+Down` | R1 left; wheel rotate left |
| Increase reasoning effort | `Ctrl+Alt+Shift+Up` | R1 right; wheel rotate right |
| Cycle reasoning effort | `Ctrl+Alt+Shift+R` | R1 press; wheel center |
| Toggle Plan mode | `Ctrl+Alt+Shift+P` | Skills page Plan; wheel left |
| Toggle Fast mode | `Ctrl+Alt+Shift+F` | Wheel right |
| Start Dictation (push-to-talk) | `Ctrl+Shift+D` | Physical keyboard only |
| Toggle Voice Chat | `Ctrl+Alt+Shift+V` | Live S bottom-dial press; CT round button 8 |
| Continue in New Chat | `Ctrl+Alt+Shift+N` | Agents position 7 |
| Copy as Markdown | `Ctrl+Alt+Shift+C` | Agents position 10 |

- Editable source: `src/codex-keybindings.json`
- Installed Codex file: `%USERPROFILE%\.codex\keybindings.json`
- Installer: `tools/install-codex-keybindings.ps1`

Run `.\tools\install-codex-keybindings.ps1` from the repository root. It preserves unrelated shortcuts, detects conflicts, backs up an existing file, performs an atomic write, and verifies the installed mappings. Use `-WhatIf` to preview the target without writing it.

Codex reads these mappings when its shortcut state is loaded. After replacing the installed file outside Codex, restart the Codex app once, then open Settings > Keyboard Shortcuts and confirm all nine entries above.

Review uses Codex's built-in Toggle Review Panel shortcut `Ctrl+Alt+B`.

The installed Codex command ID for Voice Chat is `composer.startVoiceMode`. It is assigned to `Ctrl+Alt+Shift+V`; the app describes this command as starting or stopping Voice Chat. The Live S bottom-dial press and CT round button 8 send that shortcut.

The installed Codex command ID for Dictation is `composer.startDictation`. It is assigned explicitly to `Ctrl+Shift+D` in `keybindings.json` for keyboard push-to-talk use. Physical testing confirmed that Codex listens only while this chord is held, whereas a Loupedeck shortcut is an atomic press/release. The Commands-page Dictate control therefore continues to use Windows Voice Typing (`Win+H`) as a reliable press-on/press-off text-entry control. Restart Codex once after installing or changing the native keybinding file.
