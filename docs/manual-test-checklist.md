# Manual hardware test checklist

Use a disposable Codex chat with no unsaved prompt text. Check off each item only after observing the result in the live app.

## Profile switching and display

- [ ] Click the Codex window: the CT switches to `Codex Controller`.
- [ ] Click a different application: the CT leaves the Codex profile and follows that application/System.
- [ ] Re-focus Codex: the last Codex workspace returns without a service restart.
- [ ] All touchscreen labels are readable at normal viewing distance and none are visibly clipped.
- [ ] Workspace colors are distinct: blue Commands, cyan Agents, purple Skills, green Quick Text.
- [ ] The center wheel clearly shows Lightbulb / BrainCircuit / Zap for Plan / Reasoning / Fast.
- [ ] The five custom dial displays clearly show Bot / ScrollText / Type / BrainCircuit / PanelsTopLeft; System Volume still shows Loupedeck's native icon.

## Round buttons

- [ ] 1 opens Commands.
- [ ] 2 opens Agents.
- [ ] 3 opens Skills.
- [ ] 4 opens Quick Text.
- [ ] 5 starts a New Chat.
- [ ] 6 opens Quick Chat.
- [ ] 7 toggles the Review panel.
- [ ] 8 starts Codex Voice Chat; pressing it again stops the active Voice Chat.

## Commands touchscreen page

- [ ] New Chat
- [ ] Quick Chat
- [ ] Side Chat
- [ ] Search Chats
- [ ] Open Folder
- [ ] Command Menu
- [ ] Review Panel
- [ ] Terminal
- [ ] Bottom Panel
- [ ] Sidebar
- [ ] Dictation
- [ ] Keyboard Shortcuts

## Agents touchscreen page

- [ ] Previous Agent moves to the previous task/chat.
- [ ] Next Agent moves to the next task/chat.
- [ ] Search Chats
- [ ] New Chat
- [ ] Side Chat
- [ ] Standalone Chat
- [ ] Continue New opens a new continuation.
- [ ] Archive Chat works only in the disposable test chat.
- [ ] Pin/Unpin toggles and can be restored to its original state.
- [ ] Copy Markdown places Markdown on the clipboard.
- [ ] Status Check inserts text and does not submit.
- [ ] Handoff Summary inserts text and does not submit.

## Skills touchscreen page

- [ ] Skill Picker inserts `$` and opens the picker when supported by the active composer.
- [ ] OpenAI Docs inserts its complete prompt without submitting.
- [ ] Browser inserts its complete prompt without submitting.
- [ ] GitHub inserts its complete prompt without submitting.
- [ ] Fix CI inserts its complete prompt without submitting.
- [ ] Documents inserts its complete prompt without submitting.
- [ ] PDF inserts its complete prompt without submitting.
- [ ] Presentations inserts its complete prompt without submitting.
- [ ] Spreadsheets inserts its complete prompt without submitting.
- [ ] Visualize inserts its complete prompt without submitting.
- [ ] Review toggles the review panel.
- [ ] Plan toggles Plan mode. Toggle it back after the test.

## Quick Text touchscreen page

- [ ] Finish It
- [ ] Status Check
- [ ] Root Cause
- [ ] Validate All
- [ ] Update Docs
- [ ] Simplify
- [ ] Handoff
- [ ] Test First
- [ ] Edge Cases
- [ ] Security Review
- [ ] Performance Check
- [ ] Explain Change

For every item above, confirm the full text appears once, no newline is appended, and the prompt is not submitted.

## Dials

- [ ] L1 left/right moves to previous/next agent; press opens Search Chats.
- [ ] L2 left/right pages the transcript up/down; press jumps to the latest content.
- [ ] L3 left/right decreases/increases font size; press opens Shortcut Help.
- [ ] R1 left/right decreases/increases reasoning effort; press cycles reasoning effort.
- [ ] R2 left/right decreases/increases system volume; press resets/mutes as shown by Loupedeck.
- [ ] R3 left/right moves to previous/next tab; press toggles the bottom panel.

## Input mode

- [ ] Focus an empty Codex composer, then press Dictation (`Win+H`); confirm Windows Voice Typing starts, speech is inserted only into the composer, and a second press stops listening.
- [ ] Stop Dictation from its visible control after the test.
- [ ] Windows microphone access remains allowed for Codex.

## Center wheel

- [ ] Rotate left decreases reasoning effort once per detent at a usable pace.
- [ ] Rotate right increases reasoning effort once per detent at a usable pace.
- [ ] Touch left toggles Plan mode.
- [ ] Touch center cycles reasoning effort.
- [ ] Touch right toggles Fast mode.
- [ ] Reasoning, Plan, and Fast react immediately without opening the Command Menu or typing into the composer.

## Custom Codex shortcuts

- [ ] Settings > Keyboard Shortcuts shows Reasoning Down as `Ctrl+Alt+Shift+Down`.
- [ ] Settings > Keyboard Shortcuts shows Reasoning Up as `Ctrl+Alt+Shift+Up`.
- [ ] Settings > Keyboard Shortcuts shows Cycle Reasoning as `Ctrl+Alt+Shift+R`.
- [ ] Settings > Keyboard Shortcuts shows Toggle Plan Mode as `Ctrl+Alt+Shift+P`.
- [ ] Settings > Keyboard Shortcuts shows Toggle Fast Mode as `Ctrl+Alt+Shift+F`.
- [ ] Settings > Keyboard Shortcuts shows Continue in New Chat as `Ctrl+Alt+Shift+N`.
- [ ] Settings > Keyboard Shortcuts shows Copy as Markdown as `Ctrl+Alt+Shift+C`.
- [ ] Settings > Keyboard Shortcuts shows Toggle Voice Chat as `Ctrl+Alt+Shift+V`.

## Square and fixed buttons

- [ ] A/B/C/D send Up/Left/Down/Right.
- [ ] FN+A/B/C/D send Page Up/Home/Page Down/End.
- [ ] E opens the Command Menu.
- [ ] Fixed Home retains its normal Loupedeck behavior.
- [ ] Fixed Enter/Esc retains its normal Loupedeck behavior.
- [ ] Fixed Keyboard retains its normal Loupedeck behavior.
- [ ] FN works both alone and with A–D as expected.

Record any failed item with the active workspace, exact control, visible Codex state, and whether a second attempt behaved differently. Direct-shortcut failures are most likely caused by a stale Codex session, focus, or a shortcut conflict.
