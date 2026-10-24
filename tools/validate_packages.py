#!/usr/bin/env python3
"""Validate both generated profiles without installing them or sending any keys."""
import base64
import json
import re
import zipfile
from pathlib import Path
from build_profile import config_for_target, action_ref

ROOT = Path(__file__).resolve().parents[1]


def validate(target):
    config = config_for_target(json.loads((ROOT/'src/profile.json').read_text(encoding='utf-8')), target)
    actions = {a['id']: a for a in config['actions']}
    filename = 'Codex-Controller-Live-S.LP4' if target == 'live-s' else 'Codex-Controller.LP4'
    with zipfile.ZipFile(ROOT/'dist'/filename) as z:
        assert z.testzip() is None, 'Corrupt package'
        assert len(z.namelist()) == len(set(z.namelist())), 'Duplicate members'
        assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
        p = json.loads(z.read('ProfileInfo.json')); app = json.loads(z.read('ApplicationInfo.json'))
        assert app['deviceType'] == config['profile']['deviceType']
        assert app['processOrBundleName'].lower() == 'chatgpt'
        mode = p['layout']['layoutModes'][0]
        assert len(mode['workspaces']) == 4 and len(mode['touchPages']) == 4
        assert all(len(page['controls']) == (15 if target == 'live-s' else 12) for page in mode['touchPages'])
        macros = {'$@Generic___@Macro___'+a['name']: a for a in p['macroCommands']}
        native = {a['name']: a for a in p['profileActions']}
        adjustments = {'$@Generic___@MacroAdjustment___'+a['name'] for a in p['macroAdjustments']}
        refs = re.findall(r'\$@Generic___@(?:Macro|MacroAdjustment|ProfileAction)___[A-F0-9]+', json.dumps(p['layout']))
        assert all(ref in set(macros)|set(native)|adjustments for ref in refs), 'Unresolved control'
        for action in actions.values():
            ref = action_ref(action['id'], actions)
            assert ref in macros or ref in native
            icon = json.loads(z.read('ActionIcons/'+ref+'.ict'))
            assert icon['items'] and all(i.get('isVisible') for i in icon['items'])
            for item in icon['items']:
                image = base64.b64decode(item['image'], validate=True)
                assert image.startswith(b'\x89PNG') or b'<svg' in image[:300]
            if action['type'] == 'text':
                n = native[ref]
                assert n['templateActionName'] == '$@Generic___@SendText'
                params = n['actionParameters']['parameters']
                assert params['text'] == action['text'] and params['useClipboard'] == 'false'
                assert '\n' not in params['text'] and '\r' not in params['text']
        assert len(native) == sum(a['type'] == 'text' for a in actions.values())
        assert not any(a['type'] == 'palette_command' for a in actions.values())
        voice_ref = action_ref('voice_chat', actions)
        voice = macros[voice_ref]
        assert len(voice['actionEditorCommands']) == 1
        assert voice['actionEditorCommands'][0]['actionParameters']['keyboardKey'].startswith('ControlOrCommand+AltOrOption+Shift+KeyV___')
        if target == 'ct':
            assert p['layout']['roundPage']['controls'][7]['pressAction'] == voice_ref
        else:
            assert all(page['controls'][1]['pressAction'] == voice_ref for page in mode['encoderPages'])
        print(f'PASS {target}: 4 pages, {len(macros)} shortcuts, {len(native)} native text actions, complete custom icons, all controls resolve')


if __name__ == '__main__':
    for target in ('ct','live-s'): validate(target)
    bindings = json.loads((ROOT/'src/codex-keybindings.json').read_text(encoding='utf-8'))
    assert len({b['command'] for b in bindings}) == len(bindings) == 9
    assert len({b['key'].lower() for b in bindings}) == 9
    assert any(b['command'] == 'composer.startVoiceMode' and b['key'] == 'Ctrl+Alt+Shift+V' for b in bindings)
    print('PASS keybindings: 9 unique commands and shortcuts; Voice Chat configured')
