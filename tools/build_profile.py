#!/usr/bin/env python3
"""Build the editable Codex Controller sources into Loupedeck LP4 profiles."""

from __future__ import annotations

import base64
import argparse
import copy
import json
import math
import shutil
import textwrap
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "profile.json"
ICONS = ROOT / "src" / "icons"
DIST = ROOT / "dist"
PACKAGE = DIST / "package"
DOCS = ROOT / "docs"
LP4 = DIST / "Codex-Controller.LP4"
NAMESPACE = uuid.UUID("4cb504a4-4240-4f15-a624-f7ebf9c03a62")

FONT_REGULAR = Path("C:/Windows/Fonts/segoeui.ttf")
FONT_SEMIBOLD = Path("C:/Windows/Fonts/seguisb.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/segoeuib.ttf")

LUCIDE_ICON_ELEMENTS = {
    "arrow-left": (
        '<path d="m12 19-7-7 7-7"/>',
        '<path d="M19 12H5"/>',
    ),
    "arrow-right": (
        '<path d="M5 12h14"/>',
        '<path d="m12 5 7 7-7 7"/>',
    ),
    "square-pen": (
        '<path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>',
        '<path d="M18.375 2.625a1 1 0 0 1 3 3l-9.013 9.014a2 2 0 0 1-.853.505l-2.873.84a.5.5 0 0 1-.62-.62l.84-2.873a2 2 0 0 1 .506-.852z"/>',
    ),
    "message-circle-plus": (
        '<path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719"/>',
        '<path d="M8 12h8"/>',
        '<path d="M12 8v8"/>',
    ),
    "messages-square": (
        '<path d="M16 10a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 14.286V4a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>',
        '<path d="M20 9a2 2 0 0 1 2 2v10.286a.71.71 0 0 1-1.212.502l-2.202-2.202A2 2 0 0 0 17.172 19H10a2 2 0 0 1-2-2v-1"/>',
    ),
    "search": (
        '<path d="m21 21-4.34-4.34"/>',
        '<circle cx="11" cy="11" r="8"/>',
    ),
    "folder-open": (
        '<path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
    ),
    "command": (
        '<path d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3"/>',
    ),
    "panel-right": (
        '<rect width="18" height="18" x="3" y="3" rx="2"/>',
        '<path d="M15 3v18"/>',
    ),
    "square-terminal": (
        '<path d="m7 11 2-2-2-2"/>',
        '<path d="M11 13h4"/>',
        '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/>',
    ),
    "panel-bottom": (
        '<rect width="18" height="18" x="3" y="3" rx="2"/>',
        '<path d="M3 15h18"/>',
    ),
    "panel-left": (
        '<rect width="18" height="18" x="3" y="3" rx="2"/>',
        '<path d="M9 3v18"/>',
    ),
    "mic": (
        '<path d="M12 19v3"/>',
        '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/>',
        '<rect x="9" y="2" width="6" height="13" rx="3"/>',
    ),
    "keyboard": (
        '<path d="M10 8h.01"/>',
        '<path d="M12 12h.01"/>',
        '<path d="M14 8h.01"/>',
        '<path d="M16 12h.01"/>',
        '<path d="M18 8h.01"/>',
        '<path d="M6 8h.01"/>',
        '<path d="M7 16h10"/>',
        '<path d="M8 12h.01"/>',
        '<rect width="20" height="16" x="2" y="4" rx="2"/>',
    ),
    "message-square-dashed": (
        '<path d="M14 3h2"/>',
        '<path d="M16 19h-2"/>',
        '<path d="M2 12v-2"/>',
        '<path d="M2 16v5.286a.71.71 0 0 0 1.212.502l1.149-1.149"/>',
        '<path d="M20 19a2 2 0 0 0 2-2v-1"/>',
        '<path d="M22 10v2"/>',
        '<path d="M22 6V5a2 2 0 0 0-2-2"/>',
        '<path d="M4 3a2 2 0 0 0-2 2v1"/>',
        '<path d="M8 19h2"/>',
        '<path d="M8 3h2"/>',
    ),
    "git-fork": (
        '<circle cx="12" cy="18" r="3"/>',
        '<circle cx="6" cy="6" r="3"/>',
        '<circle cx="18" cy="6" r="3"/>',
        '<path d="M18 9v2c0 .6-.4 1-1 1H7c-.6 0-1-.4-1-1V9"/>',
        '<path d="M12 12v3"/>',
    ),
    "split": (
        '<path d="M16 3h5v5"/>',
        '<path d="M8 3H3v5"/>',
        '<path d="M12 22v-8.3a4 4 0 0 0-1.172-2.872L3 3"/>',
        '<path d="m15 9 6-6"/>',
    ),
    "archive": (
        '<rect width="20" height="5" x="2" y="3" rx="1"/>',
        '<path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/>',
        '<path d="M10 12h4"/>',
    ),
    "pin": (
        '<path d="M12 17v5"/>',
        '<path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/>',
    ),
    "clipboard-copy": (
        '<rect width="8" height="4" x="8" y="2" rx="1" ry="1"/>',
        '<path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>',
        '<path d="M16 4h2a2 2 0 0 1 2 2v4"/>',
        '<path d="M21 14H11"/>',
        '<path d="m15 10-4 4 4 4"/>',
    ),
    "activity": (
        '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    ),
    "summary": (
        '<path d="M15 4H7"/>',
        '<path d="m18 16 3 3-3 3"/>',
        '<path d="M3 4v13a2 2 0 0 0 2 2h16"/>',
        '<path d="M7 14h7"/>',
        '<path d="M7 9h12"/>',
    ),
    "lightbulb": (
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>',
        '<path d="M9 18h6"/>',
        '<path d="M10 22h4"/>',
    ),
    "brain-circuit": (
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/>',
        '<path d="M9 13a4.5 4.5 0 0 0 3-4"/>',
        '<path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/>',
        '<path d="M3.477 10.896a4 4 0 0 1 .585-.396"/>',
        '<path d="M6 18a4 4 0 0 1-1.967-.516"/>',
        '<path d="M12 13h4"/>',
        '<path d="M12 18h6a2 2 0 0 1 2 2v1"/>',
        '<path d="M12 8h8"/>',
        '<path d="M16 8V5a2 2 0 0 1 2-2"/>',
        '<circle cx="16" cy="13" r=".5"/>',
        '<circle cx="18" cy="3" r=".5"/>',
        '<circle cx="20" cy="21" r=".5"/>',
        '<circle cx="20" cy="8" r=".5"/>',
    ),
    "zap": (
        '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    ),
    "bot": (
        '<path d="M12 8V4H8"/>',
        '<rect width="16" height="12" x="4" y="8" rx="2"/>',
        '<path d="M2 14h2"/>',
        '<path d="M20 14h2"/>',
        '<path d="M15 13v2"/>',
        '<path d="M9 13v2"/>',
    ),
    "scroll-text": (
        '<path d="M15 12h-5"/>',
        '<path d="M15 8h-5"/>',
        '<path d="M19 17V5a2 2 0 0 0-2-2H4"/>',
        '<path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v2a1 1 0 0 0 1 1h3"/>',
    ),
    "type": (
        '<path d="M12 4v16"/>',
        '<path d="M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2"/>',
        '<path d="M9 20h6"/>',
    ),
    "panels-top-left": (
        '<rect width="18" height="18" x="3" y="3" rx="2"/>',
        '<path d="M3 9h18"/>',
        '<path d="M9 21V9"/>',
    ),
}

DIAL_LUCIDE_ICONS = {
    "Agents": "bot",
    "Transcript": "scroll-text",
    "Font Size": "type",
    "Reasoning": "brain-circuit",
    "Tabs": "panels-top-left",
}


LIVE_S_PAGE_BUTTONS = {
    "commands": [
        "new_chat", "quick_chat", "side_chat", "search_chats", "open_folder",
        "command_menu", "review_tab", "toggle_terminal", "toggle_bottom", "toggle_sidebar",
        "dictation", "shortcut_help", "plan_toggle", "reason_cycle", "fast_toggle",
    ],
    "agents": [
        "previous_agent", "next_agent", "search_chats", "previous_tab", "next_tab",
        "new_chat", "side_chat", "standalone_chat", "continue_new", "archive_chat",
        "toggle_pin", "copy_markdown", "agent_status", "handoff", "go_latest",
    ],
    "skills": [
        "skill_picker", "skill_openai_docs", "skill_browser", "skill_github", "skill_fix_ci",
        "skill_documents", "skill_pdf", "skill_slides", "skill_sheets", "skill_visualize",
        "review_tab", "plan_toggle", "reason_cycle", "validate_all", "finish_it",
    ],
    "quick_text": [
        "finish_it", "agent_status", "root_cause", "validate_all", "update_docs",
        "simplify", "handoff", "test_first", "edge_cases", "security_review",
        "performance_check", "explain_change", "new_chat", "plan_toggle", "reason_cycle",
    ],
}


def config_for_target(base_config: dict, target: str) -> dict:
    config = copy.deepcopy(base_config)
    if target == "ct":
        return config

    profile = config["profile"]
    profile["name"] = "Codex Controller Live S 1.1.1"
    profile["description"] = "A four-workspace Loupedeck Live S controller for the Codex desktop app."
    profile["deviceType"] = "Loupedeck50"
    profile["version"] = "1.1.1"
    for page in config["pages"]:
        page["buttons"] = LIVE_S_PAGE_BUTTONS[page["id"]]
    config["dials"] = [
        {"position": "Top", "name": "Agents", "left": "previous_agent", "right": "next_agent", "press": "search_chats"},
        {"position": "Bottom", "name": "Reasoning", "left": "reason_decrease", "right": "reason_increase", "press": "voice_chat"},
    ]
    return config


def load_font(path: Path, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default()


def stable_id(kind: str, name: str) -> str:
    return uuid.uuid5(NAMESPACE, f"{kind}/{name}").hex.upper()


def argb(hex_color: str) -> int:
    value = hex_color.removeprefix("#")
    if len(value) == 6:
        value = "FF" + value
    return int(value, 16)


def typed_dict(type_name: str, **values):
    return {"$type": type_name, **values}


def keyboard_value(key: str, label: str) -> str:
    return f"{key}___69534729___{label}___"


def editor_key(name: str, key: str, label: str) -> dict:
    return typed_dict(
        "Loupedeck.Service.MacroActionEditorCommand, LoupedeckService",
        name=name,
        templateName="$@Generic___@KeyboardKey",
        actionParameters=typed_dict(
            "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.String, System.Private.CoreLib]], System.Private.CoreLib",
            keyboardKey=keyboard_value(key, label),
        ),
    )


def key_label_for_action(action: dict) -> str:
    return action.get("keyLabel", action.get("key", ""))


def macro_for(action: dict, mode_name: str) -> dict:
    macro_id = stable_id("macro", action["id"])
    editors: list[dict] = []
    steps: list[str] = []
    kind = action["type"]

    if kind == "shortcut":
        editor_id = stable_id("editor", f"{action['id']}/key")
        editors.append(editor_key(editor_id, action["key"], key_label_for_action(action)))
        steps.append(editor_id)
    elif kind == "text":
        steps.append(f"$@Generic___@TypeText___{action['text']}")
    elif kind == "palette_command":
        open_id = stable_id("editor", f"{action['id']}/open-palette")
        enter_id = stable_id("editor", f"{action['id']}/enter")
        editors.extend(
            [
                editor_key(open_id, "ControlOrCommand+KeyK", "Ctrl+K"),
                editor_key(enter_id, "Return", "Return"),
            ]
        )
        steps.extend(
            [
                open_id,
                "$@Generic___@Sleep___450",
                f"$@Generic___@TypeText___{action['command']}",
                "$@Generic___@Sleep___300",
                enter_id,
            ]
        )
    else:
        raise ValueError(f"Unsupported action type: {kind}")

    return typed_dict(
        "Loupedeck.Service.ApplicationProfileMacroCommand, LoupedeckService",
        isCommand=True,
        name=macro_id,
        displayName=action["displayName"],
        description=action.get("description", ""),
        groupName=action.get("group", "Codex"),
        superGroupName="@macro",
        supportedOs="All",
        supportedModes=[mode_name],
        showAsSingleAction=False,
        actionEditorCommands=editors,
        isMultiState=False,
        actions=steps,
    )


def macro_ref(action_id: str) -> str:
    return f"$@Generic___@Macro___{stable_id('macro', action_id)}"


def adjustment_ref(adjustment_id: str) -> str:
    return f"$@Generic___@MacroAdjustment___{stable_id('adjustment', adjustment_id)}"


def adjustment_for(adjustment_id: str, name: str, left: dict, right: dict, mode_name: str) -> dict:
    editors: list[dict] = []

    def steps_for(action: dict, side: str) -> list[str]:
        if action["type"] == "shortcut":
            editor_id = stable_id("adjustment-editor", f"{adjustment_id}/{side}/key")
            editors.append(editor_key(editor_id, action["key"], key_label_for_action(action)))
            return [editor_id]
        if action["type"] == "palette_command":
            open_id = stable_id("adjustment-editor", f"{adjustment_id}/{side}/open-palette")
            enter_id = stable_id("adjustment-editor", f"{adjustment_id}/{side}/enter")
            editors.extend(
                [
                    editor_key(open_id, "ControlOrCommand+KeyK", "Ctrl+K"),
                    editor_key(enter_id, "Return", "Return"),
                ]
            )
            return [
                open_id,
                "$@Generic___@Sleep___450",
                f"$@Generic___@TypeText___{action['command']}",
                "$@Generic___@Sleep___300",
                enter_id,
            ]
        raise ValueError(f"Adjustment {name} cannot run {action['type']}")

    return typed_dict(
        "Loupedeck.Service.ApplicationProfileMacroAdjustment, LoupedeckService",
        isCommand=False,
        name=stable_id("adjustment", adjustment_id),
        displayName=name,
        description="",
        groupName="Codex Dials",
        superGroupName="@macro",
        supportedOs="All",
        supportedModes=[mode_name],
        showAsSingleAction=False,
        actionEditorCommands=editors,
        actionsBefore=[""],
        actionsLeft=steps_for(left, "left"),
        actionsRight=steps_for(right, "right"),
        actionsReset=[],
        clickRateLimit=2 if adjustment_id == "reasoning" else 9,
    )


def button_control(press: str | None = None, fn: str | None = None) -> dict:
    return typed_dict(
        "Loupedeck.Service.ProfileLayoutButton, LoupedeckService",
        pressAction=press,
        fnPressAction=fn,
    )


def encoder_control(press: str | None, rotate: str | None) -> dict:
    return typed_dict(
        "Loupedeck.Service.ProfileLayoutEncoder, LoupedeckService",
        pressAction=press,
        fnPressAction=None,
        rotateAction=rotate,
        fnRotateAction=None,
    )


def action_icon_png(action: dict, palette: dict) -> bytes:
    size = 180
    image = Image.new("RGBA", (size, size), palette["background"])
    draw = ImageDraw.Draw(image)
    color = palette[action.get("color", "system")]
    draw.rounded_rectangle((4, 4, size - 4, size - 4), radius=24, fill="#111827", outline=color, width=5)
    draw.rounded_rectangle((4, 4, size - 4, 22), radius=12, fill=color)
    draw.rectangle((4, 13, size - 4, 25), fill=color)

    short = action.get("shortLabel", action["displayName"][:5]).upper()
    short_size = 48 if len(short) <= 4 else 38 if len(short) <= 6 else 30
    font_short = load_font(FONT_BOLD, short_size)
    bbox = draw.textbbox((0, 0), short, font=font_short)
    draw.text(((size - (bbox[2] - bbox[0])) / 2, 37), short, font=font_short, fill=palette["foreground"])

    label_lines = action.get("label", action["displayName"]).upper().split("\n")[:2]
    font_label = load_font(FONT_SEMIBOLD, 22)
    y = 112 if len(label_lines) == 1 else 101
    for line in label_lines:
        bbox = draw.textbbox((0, 0), line, font=font_label)
        draw.text(((size - (bbox[2] - bbox[0])) / 2, y), line, font=font_label, fill="#CBD5E1")
        y += 26

    from io import BytesIO

    stream = BytesIO()
    image.save(stream, "PNG", optimize=True)
    return stream.getvalue()


def action_icon_svg(action: dict, palette: dict) -> str:
    if action.get("lucideIcon"):
        return lucide_icon_svg(action, palette)
    color = palette[action.get("color", "system")]
    short = action.get("shortLabel", action["displayName"][:5]).upper()
    lines = action.get("label", action["displayName"]).upper().split("\n")[:2]
    font_size = 48 if len(short) <= 4 else 38 if len(short) <= 6 else 30
    labels = []
    y = 124 if len(lines) == 1 else 112
    for line in lines:
        labels.append(f'<text x="90" y="{y}" class="label">{escape_xml(line)}</text>')
        y += 26
    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">',
            "<style>.short,.label{font-family:'Segoe UI',sans-serif;text-anchor:middle}.short{font-weight:700}.label{font-size:22px;font-weight:600;fill:#CBD5E1}</style>",
            f'<rect width="180" height="180" rx="24" fill="#111827" stroke="{color}" stroke-width="5"/>',
            f'<path d="M4 24V16Q4 4 16 4H164Q176 4 176 16V24Z" fill="{color}"/>',
            f'<text x="90" y="82" class="short" font-size="{font_size}" fill="{palette["foreground"]}">{escape_xml(short)}</text>',
            *labels,
            "</svg>",
        ]
    )


def lucide_icon_svg(action: dict, palette: dict) -> str:
    icon_name = action["lucideIcon"]
    elements = LUCIDE_ICON_ELEMENTS[icon_name]
    color = palette[action.get("color", "system")]
    icon_only = action.get("iconOnly", False)
    if icon_only:
        translate_x, translate_y, scale = 24, 24, 5.5
        label = None
    else:
        translate_x, translate_y, scale = 36, 16, 4.5
        label = action.get("iconLabel", action.get("shortLabel", action["displayName"])).upper()
    rotation = int(action.get("iconRotation", 0))
    rendered_elements = list(elements)
    if rotation:
        rendered_elements = [f'<g transform="rotate({rotation} 12 12)">', *rendered_elements, '</g>']
    content = ['<svg xmlns="http://www.w3.org/2000/svg" width="180" height="180" viewBox="0 0 180 180">']
    content.extend(
        [
            f'<g transform="translate({translate_x} {translate_y}) scale({scale})" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">',
            *rendered_elements,
            '</g>',
        ]
    )
    if label:
        content.extend(
            [
                "<style>.icon-label{font-family:'Segoe UI',sans-serif;font-size:20px;font-weight:700;text-anchor:middle;letter-spacing:1px}</style>",
                f'<text x="90" y="160" class="icon-label" fill="{palette["foreground"]}">{escape_xml(label)}</text>',
            ]
        )
    content.append("</svg>")
    return "\n".join(content)


def escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def ict_for(png: bytes, file_name: str, background_color: str = "#0B0F14") -> dict:
    return {
        "backgroundColor": argb(background_color),
        "items": [
            typed_dict(
                "Loupedeck.Service.ActionIconImageItem, LoupedeckShared",
                image=base64.b64encode(png).decode("ascii"),
                imageFileName=file_name,
                imageColor=argb("#FFFFFF"),
                imageRotation="None",
                isVisible=True,
                itemType="Image",
                area={"x": 0, "y": 0, "width": 100, "height": 100, "isFullScreen": True},
            )
        ],
    }


def app_icon(palette: dict) -> bytes:
    image = Image.new("RGBA", (256, 256), palette["background"])
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((10, 10, 246, 246), radius=52, fill="#111827", outline=palette["reasoning"], width=10)
    draw.arc((45, 40, 211, 206), 35, 325, fill=palette["agents"], width=15)
    font = load_font(FONT_BOLD, 92)
    text = "C/"
    bbox = draw.textbbox((0, 0), text, font=font)
    draw.text(((256 - (bbox[2] - bbox[0])) / 2, 67), text, font=font, fill=palette["foreground"])
    small = load_font(FONT_SEMIBOLD, 26)
    bbox = draw.textbbox((0, 0), "CODEX", font=small)
    draw.text(((256 - (bbox[2] - bbox[0])) / 2, 191), "CODEX", font=small, fill=palette["muted"])
    from io import BytesIO

    stream = BytesIO()
    image.save(stream, "PNG", optimize=True)
    return stream.getvalue()


def fit_text(draw: ImageDraw.ImageDraw, text: str, box_width: int, start_size: int, min_size: int = 16):
    size = start_size
    while size > min_size:
        font = load_font(FONT_SEMIBOLD, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= box_width:
            return font
        size -= 1
    return load_font(FONT_SEMIBOLD, min_size)


def reference_png(config: dict, actions: dict) -> bytes:
    palette = config["palette"]
    width, height = 2400, 3350
    image = Image.new("RGB", (width, height), palette["background"])
    draw = ImageDraw.Draw(image)
    title_font = load_font(FONT_BOLD, 74)
    h1_font = load_font(FONT_BOLD, 42)
    h2_font = load_font(FONT_SEMIBOLD, 30)
    body_font = load_font(FONT_REGULAR, 25)
    small_font = load_font(FONT_REGULAR, 21)
    draw.text((90, 65), "CODEX CONTROLLER · LOUPEDECK CT", font=title_font, fill=palette["foreground"])
    draw.text((94, 150), "Four workspaces · consistent dials · safe insert-only quick text", font=h2_font, fill=palette["muted"])

    card_w, card_h = 1080, 900
    for page_index, page in enumerate(config["pages"]):
        col, row = page_index % 2, page_index // 2
        x = 90 + col * 1140
        y = 240 + row * 960
        color = palette[page["color"]]
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=30, fill="#111827", outline=color, width=5)
        draw.text((x + 36, y + 25), f"ROUND {page_index + 1}  ·  {page['name'].upper()}", font=h1_font, fill=color)
        cell_w, cell_h = 320, 168
        for i, action_id in enumerate(page["buttons"]):
            action = actions[action_id]
            cx = x + 36 + (i % 3) * 340
            cy = y + 105 + (i // 3) * 190
            draw.rounded_rectangle((cx, cy, cx + cell_w, cy + cell_h), radius=20, fill="#0F172A", outline="#334155", width=2)
            draw.rectangle((cx, cy, cx + 10, cy + cell_h), fill=color)
            name = action["displayName"].upper()
            font = fit_text(draw, name, cell_w - 52, 26)
            draw.text((cx + 28, cy + 29), name, font=font, fill=palette["foreground"])
            detail = action.get("keyLabel") or ("INSERT ONLY" if action["type"] == "text" else "COMMAND MENU")
            draw.text((cx + 28, cy + 92), detail, font=small_font, fill=palette["muted"])

    y = 2195
    draw.rounded_rectangle((90, y, 2310, y + 505), radius=30, fill="#111827", outline=palette["system"], width=5)
    draw.text((126, y + 26), "SIX DIALS · SAME ON EVERY WORKSPACE", font=h1_font, fill=palette["system"])
    for i, dial in enumerate(config["dials"]):
        col, row = i % 3, i // 3
        x = 126 + col * 720
        cy = y + 104 + row * 178
        draw.text((x, cy), f"{dial['position']}  {dial['name']}", font=h2_font, fill=palette["foreground"])
        if "nativeAdjustment" in dial:
            detail = "turn: volume − / +    press: reset/mute"
        else:
            detail = f"turn: {actions[dial['left']]['shortLabel']} ←  → {actions[dial['right']]['shortLabel']}    press: {actions[dial['press']]['shortLabel']}"
        draw.text((x, cy + 51), detail, font=body_font, fill=palette["muted"])

    y = 2755
    draw.rounded_rectangle((90, y, 2310, y + 485), radius=30, fill="#111827", outline=palette["reasoning"], width=5)
    draw.text((126, y + 25), "CENTER WHEEL + PHYSICAL BUTTONS", font=h1_font, fill=palette["reasoning"])
    draw.text((126, y + 105), "Wheel turn", font=h2_font, fill=palette["foreground"])
    draw.text((355, y + 108), "Reasoning effort down / up", font=body_font, fill=palette["muted"])
    draw.text((126, y + 160), "Wheel touch", font=h2_font, fill=palette["foreground"])
    draw.text((355, y + 163), "PLAN  ·  CYCLE REASONING  ·  FAST", font=body_font, fill=palette["muted"])
    rounds = "   ".join(
        [
            f"{i + 1}:{item.get('workspace', item.get('action')).replace('_', ' ').upper()}"
            for i, item in enumerate(config["roundButtons"])
        ]
    )
    draw.text((126, y + 235), "Round keys", font=h2_font, fill=palette["foreground"])
    draw.text((355, y + 238), rounds, font=small_font, fill=palette["muted"])
    draw.text((126, y + 305), "Square A–D", font=h2_font, fill=palette["foreground"])
    draw.text((355, y + 308), "arrows · FN = Page Up / Home / Page Down / End", font=body_font, fill=palette["muted"])
    draw.text((126, y + 365), "Square E", font=h2_font, fill=palette["foreground"])
    draw.text((355, y + 368), "Command Menu", font=body_font, fill=palette["muted"])
    draw.text((126, 3280), "Quick text and skill prompts insert into the composer but never press Enter.", font=small_font, fill=palette["muted"])

    from io import BytesIO

    stream = BytesIO()
    image.save(stream, "PNG", optimize=True)
    return stream.getvalue()


def live_s_page_preview(config: dict, actions: dict, page_id: str) -> bytes:
    palette = config["palette"]
    page = next(item for item in config["pages"] if item["id"] == page_id)
    color = palette[page["color"]]
    image = Image.new("RGB", (1000, 720), palette["background"])
    draw = ImageDraw.Draw(image)
    title_font = load_font(FONT_BOLD, 42)
    label_font = load_font(FONT_SEMIBOLD, 19)
    small_font = load_font(FONT_REGULAR, 16)

    draw.text((45, 30), f"LIVE S  ·  {page['name'].upper()}", font=title_font, fill=color)
    draw.rounded_rectangle((40, 100, 810, 590), radius=24, fill="#111827", outline="#334155", width=4)
    cell_w, cell_h = 138, 130
    for index, action_id in enumerate(page["buttons"]):
        action = actions[action_id]
        x = 65 + (index % 5) * 148
        y = 135 + (index // 5) * 145
        draw.rounded_rectangle((x, y, x + cell_w, y + cell_h), radius=12, fill="#0F172A", outline=color, width=3)
        label = action["shortLabel"].upper()
        font = fit_text(draw, label, cell_w - 20, 20, 14)
        bbox = draw.textbbox((0, 0), label, font=font)
        draw.text((x + (cell_w - (bbox[2] - bbox[0])) / 2, y + 43), label, font=font, fill=palette["foreground"])

    draw.text((845, 135), "TOP", font=label_font, fill=palette["system"])
    draw.ellipse((850, 175, 950, 275), fill="#111827", outline=palette["system"], width=4)
    draw.text((840, 290), "TASKS", font=label_font, fill=palette["foreground"])
    draw.text((835, 320), "press: search", font=small_font, fill=palette["muted"])
    draw.text((835, 390), "BOTTOM", font=label_font, fill=palette["reasoning"])
    draw.ellipse((850, 435, 950, 535), fill="#111827", outline=palette["reasoning"], width=4)
    draw.text((820, 550), "REASONING", font=label_font, fill=palette["foreground"])
    bottom_dial = config["dials"][1]
    bottom_press = actions[bottom_dial["press"]]["shortLabel"].lower()
    draw.text((825, 580), f"press: {bottom_press}", font=small_font, fill=palette["muted"])

    button_names = ("COMMANDS", "AGENTS", "SKILLS", "QUICK TEXT")
    for index, name in enumerate(button_names):
        x = 75 + index * 215
        draw.ellipse((x, 630, x + 34, 664), fill=palette["muted"])
        draw.text((x + 46, 636), name, font=small_font, fill=palette["foreground"])

    from io import BytesIO

    stream = BytesIO()
    image.save(stream, "PNG", optimize=True)
    return stream.getvalue()


def live_s_reference_png(config: dict, actions: dict) -> bytes:
    palette = config["palette"]
    width, height = 2600, 3000
    image = Image.new("RGB", (width, height), palette["background"])
    draw = ImageDraw.Draw(image)
    title_font = load_font(FONT_BOLD, 74)
    h1_font = load_font(FONT_BOLD, 40)
    h2_font = load_font(FONT_SEMIBOLD, 28)
    body_font = load_font(FONT_REGULAR, 23)
    small_font = load_font(FONT_REGULAR, 19)
    draw.text((90, 65), "CODEX CONTROLLER · LOUPEDECK LIVE S", font=title_font, fill=palette["foreground"])
    draw.text((94, 150), "Four workspaces · 15 touch controls · two consistent dials", font=h2_font, fill=palette["muted"])

    card_w, card_h = 1170, 1030
    for page_index, page in enumerate(config["pages"]):
        col, row = page_index % 2, page_index // 2
        x = 90 + col * 1260
        y = 240 + row * 1100
        color = palette[page["color"]]
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=28, fill="#111827", outline=color, width=5)
        draw.text((x + 34, y + 24), f"BUTTON {page_index + 1}  ·  {page['name'].upper()}", font=h1_font, fill=color)
        cell_w, cell_h = 208, 245
        for index, action_id in enumerate(page["buttons"]):
            action = actions[action_id]
            cx = x + 34 + (index % 5) * 222
            cy = y + 105 + (index // 5) * 270
            draw.rounded_rectangle((cx, cy, cx + cell_w, cy + cell_h), radius=16, fill="#0F172A", outline="#334155", width=2)
            draw.rectangle((cx, cy, cx + cell_w, cy + 9), fill=color)
            name = action["displayName"].upper()
            font = fit_text(draw, name, cell_w - 30, 21, 14)
            wrapped = textwrap.wrap(name, width=16)[:3]
            for line_index, line in enumerate(wrapped):
                draw.text((cx + 16, cy + 35 + line_index * 30), line, font=font, fill=palette["foreground"])
            detail = action.get("keyLabel") or ("INSERT ONLY" if action["type"] == "text" else "COMMAND MENU")
            detail_font = fit_text(draw, detail, cell_w - 30, 17, 13)
            draw.text((cx + 16, cy + 188), detail, font=detail_font, fill=palette["muted"])

    y = 2475
    draw.rounded_rectangle((90, y, 2510, y + 390), radius=28, fill="#111827", outline=palette["system"], width=5)
    draw.text((126, y + 25), "DIALS + PHYSICAL BUTTONS", font=h1_font, fill=palette["system"])
    for index, dial in enumerate(config["dials"]):
        x = 126 + index * 1150
        draw.text((x, y + 105), f"{dial['position'].upper()} DIAL  ·  {dial['name'].upper()}", font=h2_font, fill=palette["foreground"])
        detail = f"turn: {actions[dial['left']]['shortLabel']}  /  {actions[dial['right']]['shortLabel']}    press: {actions[dial['press']]['shortLabel']}"
        draw.text((x, y + 160), detail, font=body_font, fill=palette["muted"])
    draw.text((126, y + 245), "Physical buttons", font=h2_font, fill=palette["foreground"])
    draw.text((390, y + 249), "1 Commands   2 Agents   3 Skills   4 Quick Text", font=body_font, fill=palette["muted"])
    draw.text((126, 2920), "Quick text and skill prompts insert into the composer but never press Enter.", font=small_font, fill=palette["muted"])

    from io import BytesIO

    stream = BytesIO()
    image.save(stream, "PNG", optimize=True)
    return stream.getvalue()


def reference_svg(config: dict, actions: dict) -> str:
    palette = config["palette"]
    rows = []
    y = 170
    for page_index, page in enumerate(config["pages"], 1):
        color = palette[page["color"]]
        rows.append(f'<text x="60" y="{y}" class="page" fill="{color}">ROUND {page_index} · {escape_xml(page["name"].upper())}</text>')
        y += 55
        for row in range(4):
            labels = [actions[action_id]["displayName"] for action_id in page["buttons"][row * 3 : row * 3 + 3]]
            rows.append(f'<text x="90" y="{y}" class="body">' + "  ·  ".join(escape_xml(label) for label in labels) + "</text>")
            y += 42
        y += 38
    return "\n".join(
        [
            '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1500" viewBox="0 0 1600 1500">',
            "<style>text{font-family:'Segoe UI',sans-serif}.title{font-size:54px;font-weight:700;fill:#F8FAFC}.page{font-size:32px;font-weight:700}.body{font-size:25px;fill:#CBD5E1}.note{font-size:24px;fill:#94A3B8}</style>",
            f'<rect width="1600" height="1500" fill="{palette["background"]}"/>',
            '<text x="60" y="82" class="title">CODEX CONTROLLER · LOUPEDECK CT</text>',
            *rows,
            f'<text x="60" y="{y + 10}" class="page" fill="{palette["reasoning"]}">WHEEL</text>',
            f'<text x="90" y="{y + 55}" class="body">turn: reasoning down / up · touch: Plan / Cycle Reasoning / Fast</text>',
            f'<text x="60" y="{y + 115}" class="note">Quick text and skill prompts insert only; press Enter yourself after review.</text>',
            "</svg>",
        ]
    )


def shortcut_markdown(config: dict, actions: dict) -> str:
    is_live_s = config["profile"]["deviceType"] == "Loupedeck50"
    lines = [
        "# Codex Controller shortcut reference",
        "",
        "Generated from `src/profile.json`. Quick-text and skill buttons insert text only; they never submit it.",
        "",
    ]
    for page in config["pages"]:
        lines.extend([f"## {page['name']} touch page", "", "| Position | Control | Sends |", "|---:|---|---|"])
        for i, action_id in enumerate(page["buttons"], 1):
            action = actions[action_id]
            if action["type"] == "shortcut":
                sends = f"`{action['keyLabel']}`"
            elif action["type"] == "palette_command":
                sends = f"Command menu → `{action['command']}`"
            else:
                sends = "Inserts reusable text"
            lines.append(f"| {i} | {action['displayName']} | {sends} |")
        lines.append("")

    lines.extend(
        [
            "## Dials",
            "",
            "| Dial | Turn left | Press | Turn right |",
            "|---|---|---|---|",
        ]
    )
    for dial in config["dials"]:
        if "nativeAdjustment" in dial:
            left, press, right = "Volume down", "Reset/mute volume", "Volume up"
        else:
            left = actions[dial["left"]]["displayName"]
            press = actions[dial["press"]]["displayName"]
            right = actions[dial["right"]]["displayName"]
        lines.append(f"| {dial['position']} · {dial['name']} | {left} | {press} | {right} |")
    if is_live_s:
        lines.extend(
            [
                "",
                "## Physical buttons",
                "",
                "1. Commands workspace",
                "2. Agents workspace",
                "3. Skills workspace",
                "4. Quick Text workspace",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Center wheel",
                "",
                "- Rotate left/right: decrease/increase reasoning effort.",
                "- Touch left/center/right: toggle Plan mode / cycle reasoning / toggle Fast mode.",
                "",
                "## Round buttons",
                "",
                "1. Commands workspace",
                "2. Agents workspace",
                "3. Skills workspace",
                "4. Quick Text workspace",
                "5. New Chat",
                "6. Quick Chat",
                "7. Toggle Review Panel",
                "8. Dictation",
                "",
                "## Square buttons",
                "",
                "- A–D: arrow keys; with FN: Page Up, Home, Page Down, End.",
                "- E: Command Menu.",
                "- Home, Enter/Esc, Keyboard, and FN retain their fixed Loupedeck behavior.",
            ]
        )
    lines.extend(
        [
            "",
            "## Safety choices",
            "",
            "- No physical approval button is mapped.",
            "- No quick-text or skill macro presses Enter.",
            "- Reasoning, Plan, and Fast use direct custom Codex shortcuts; only genuine command-menu actions use exact English titles.",
        ]
    )
    return "\n".join(lines) + "\n"


def build(target: str = "ct") -> None:
    global PACKAGE, LP4

    base_config = json.loads(SOURCE.read_text(encoding="utf-8"))
    config = config_for_target(base_config, target)
    is_live_s = target == "live-s"
    package_dir_name = "package-live-s" if is_live_s else "package"
    package_file_name = "Codex-Controller-Live-S.LP4" if is_live_s else "Codex-Controller.LP4"
    PACKAGE = DIST / package_dir_name
    LP4 = DIST / package_file_name
    profile_cfg = config["profile"]
    palette = config["palette"]
    actions = {action["id"]: action for action in config["actions"]}

    assert len(actions) == len(config["actions"]), "Action IDs must be unique"
    assert len(config["pages"]) == 4, "Expected four workspaces"
    expected_buttons = 15 if is_live_s else 12
    expected_dials = 2 if is_live_s else 6
    assert all(len(page["buttons"]) == expected_buttons for page in config["pages"]), f"Each touch page needs {expected_buttons} buttons"
    assert len(config["dials"]) == expected_dials, f"Expected {expected_dials} dial definitions"
    assert len(config["roundButtons"]) == 8, "Loupedeck CT needs eight round-button definitions"

    generated_paths = (PACKAGE,) if is_live_s else (PACKAGE, ICONS)
    for generated in generated_paths:
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir(parents=True)
    ICONS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    (PACKAGE / "ActionIcons").mkdir()
    (PACKAGE / "metadata").mkdir()

    profile_id = stable_id("profile", profile_cfg["name"])
    package_id = stable_id("package", profile_cfg["name"])
    mode_name = profile_cfg["modeName"]
    workspace_ids = {page["id"]: stable_id("workspace", page["id"]) for page in config["pages"]}
    action_macros = [macro_for(action, mode_name) for action in config["actions"]]

    adjustments: list[dict] = []
    dial_adjustment_ids: list[str | None] = []
    for dial in config["dials"]:
        if "nativeAdjustment" in dial:
            dial_adjustment_ids.append(None)
            continue
        adjustment_id = dial["name"].lower().replace(" ", "_")
        adjustments.append(adjustment_for(adjustment_id, dial["name"], actions[dial["left"]], actions[dial["right"]], mode_name))
        dial_adjustment_ids.append(adjustment_id)

    touch_pages = []
    encoder_pages = []
    wheel_pages = []
    workspaces = []
    for page in config["pages"]:
        touch_id = stable_id("touch-page", page["id"])
        encoder_id = stable_id("encoder-page", page["id"])
        wheel_id = stable_id("wheel-page", page["id"])
        touch_pages.append(
            typed_dict(
                "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
                name=touch_id,
                displayName=page["name"],
                description=f"Codex {page['name']} controls",
                controls=[button_control(macro_ref(action_id)) for action_id in page["buttons"]],
                dynamicPageName=None,
                dynamicPagePluginName=None,
                dynamicPageNumber=0,
            )
        )
        encoder_controls = []
        for dial, adjustment_id in zip(config["dials"], dial_adjustment_ids):
            if "nativeAdjustment" in dial:
                encoder_controls.append(encoder_control(dial["nativePress"], dial["nativeAdjustment"]))
            else:
                encoder_controls.append(encoder_control(macro_ref(dial["press"]), adjustment_ref(adjustment_id)))
        if is_live_s:
            encoder_controls.extend(encoder_control(None, None) for _ in range(6 - len(encoder_controls)))
        encoder_pages.append(
            typed_dict(
                "Loupedeck.Service.ProfileLayoutEncoderPage, LoupedeckService",
                name=encoder_id,
                displayName="Codex Dials",
                description="Consistent Codex navigation and reasoning dials",
                controls=encoder_controls,
                dynamicPageName=None,
                dynamicPagePluginName=None,
                dynamicPageNumber=0,
            )
        )
        wheel_pages.append(
            typed_dict(
                "Loupedeck.Service.ProfileLayoutWheelPage, LoupedeckService",
                name=wheel_id,
                displayName=config["wheel"]["name"],
                description="Reasoning effort with Plan and Fast mode controls",
                templateName="WheelToolGeneric3x1Horizontal",
                parameters=typed_dict(
                    "Loupedeck.StringDictionaryNoCase, PluginApi",
                    adjustment=adjustment_ref("reasoning"),
                    actions=",".join(
                        macro_ref(config["wheel"][key]) for key in ("left", "center", "right")
                    ),
                ),
            )
        )
        workspaces.append(
            typed_dict(
                "Loupedeck.Service.ProfileLayoutWorkspace20, LoupedeckService",
                name=workspace_ids[page["id"]],
                displayName=page["name"],
                description=f"Codex {page['name']} workspace",
                touchPageNames=[touch_id],
                encoderPageNames=[encoder_id],
                wheelPageNames=[wheel_id],
                activationActions=[],
            )
        )

    round_controls = []
    round_items = config["roundButtons"][:4] if is_live_s else config["roundButtons"]
    for item in round_items:
        if "workspace" in item:
            press = f"$@Generic___@ChangeWorkspace___{mode_name}|{workspace_ids[item['workspace']]}"
        else:
            press = macro_ref(item["action"])
        round_controls.append(button_control(press))
    if is_live_s:
        round_controls.extend(button_control() for _ in range(8 - len(round_controls)))

    square = [button_control() for _ in range(12)]
    square_positions = {"A": 6, "B": 7, "C": 9, "D": 10, "E": 11}
    if not is_live_s:
        for name, index in square_positions.items():
            mapping = config["squareButtons"][name]
            square[index] = button_control(
                macro_ref(mapping["press"]),
                macro_ref(mapping["fn"]) if mapping.get("fn") else None,
            )

    layout_mode = typed_dict(
        "Loupedeck.Service.ProfileLayoutMode20, LoupedeckService",
        deviceType=profile_cfg["deviceType"] if is_live_s else "None",
        modeName=mode_name,
        parentModeName=None,
        actions=None,
        dynamicButtonPages=None,
        dynamicEncoderPages=None,
        homeWorkspaceName=workspace_ids[config["pages"][0]["id"]],
        touchPages=touch_pages,
        encoderPages=encoder_pages,
        wheelPages=wheel_pages,
        workspaces=workspaces,
    )
    layout = typed_dict(
        "Loupedeck.Service.ProfileLayout20, LoupedeckService",
        deviceType=profile_cfg["deviceType"],
        profileFlags="None",
        layoutModes=[layout_mode],
        roundPage=typed_dict(
            "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
            name=stable_id("page", "round"),
            displayName="",
            description=None,
            controls=round_controls,
            dynamicPageName=None,
            dynamicPagePluginName=None,
            dynamicPageNumber=0,
        ),
        squarePage=typed_dict(
            "Loupedeck.Service.ProfileLayoutButtonPage, LoupedeckService",
            name=stable_id("page", "square"),
            displayName="",
            description=None,
            controls=square,
            dynamicPageName=None,
            dynamicPagePluginName=None,
            dynamicPageNumber=0,
        ),
    )

    profile_info = typed_dict(
        "Loupedeck.Service.ApplicationProfile, LoupedeckService",
        name=profile_id,
        profileFlags="None",
        displayName=profile_cfg["name"],
        description=profile_cfg["description"],
        deviceType=profile_cfg["deviceType"],
        applicationName=profile_cfg["applicationName"],
        nativePluginName=None,
        hasNativePlugin=False,
        additionalNativePluginNames=["DefaultWin"],
        lastModifiedTimeUtc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        profileSettings=typed_dict(
            "Loupedeck.DictionaryNoCase`1[[System.String, System.Private.CoreLib]], PluginApi"
        ),
        actionImages90=None,
        actionImages60=None,
        wheelImages=None,
        actionColors=None,
        layout=layout,
        macroCommands=action_macros,
        macroAdjustments=adjustments,
        profileCommands=[],
        profileAdjustments=[],
        conversionHistory="",
        packageName=package_id,
        packageVersion=profile_cfg["version"],
        profileActions=[],
    )
    app_info = typed_dict(
        "Loupedeck.Service.SupportedApplicationInfo, LoupedeckService",
        name=profile_cfg["applicationName"],
        displayName=profile_cfg["applicationDisplayName"],
        description=profile_cfg["description"],
        deviceType=profile_cfg["deviceType"],
        nativePluginName=None,
        hasNativePlugin=False,
        processOrBundleName=profile_cfg["processOrBundleName"],
        modes=[
            typed_dict(
                "Loupedeck.Service.ApplicationMode, LoupedeckService",
                name=mode_name,
                parentModeName=None,
                displayName=mode_name,
            )
        ],
        defaultProfileName=profile_id,
        isEnabled=True,
    )

    (PACKAGE / "ProfileInfo.json").write_text(json.dumps(profile_info, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    (PACKAGE / "ApplicationInfo.json").write_text(json.dumps(app_info, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
    (PACKAGE / "ApplicationIcon.png").write_bytes(app_icon(palette))
    (PACKAGE / "metadata" / "AdvancedInfo.json").write_text('{\n  "additionalPluginNames": []\n}\n', encoding="utf-8")
    (PACKAGE / "metadata" / "LoupedeckPackage.yaml").write_text(
        f"type: Profile5\nname: {profile_id}\ndisplayName: {profile_cfg['name']}\nversion: {profile_cfg['version']}\n",
        encoding="utf-8",
    )
    (PACKAGE / "metadata" / "ProfilePreview.json").write_text('{\n  "buttonPages": [],\n  "encoderPages": []\n}\n', encoding="utf-8")

    for action in config["actions"]:
        svg = action_icon_svg(action, palette)
        (ICONS / f"{action['id']}.svg").write_text(svg, encoding="utf-8")
        if action.get("lucideIcon"):
            image = svg.encode("utf-8")
            image_file_name = f"{action['id']}.svg"
        else:
            image = action_icon_png(action, palette)
            image_file_name = f"{action['id']}.png"
        icon_name = f"$@Generic___@Macro___{stable_id('macro', action['id'])}.ict"
        (PACKAGE / "ActionIcons" / icon_name).write_text(
            json.dumps(ict_for(image, image_file_name, "#000000" if action.get("lucideIcon") else "#0B0F14"), indent=2) + "\n",
            encoding="utf-8",
        )

    for adjustment, dial in zip(adjustments, [d for d in config["dials"] if "nativeAdjustment" not in d]):
        icon_action = {
            "id": adjustment["name"],
            "label": dial["name"].upper(),
            "shortLabel": "R±" if dial["name"] == "Reasoning" else "↔",
            "displayName": dial["name"],
            "color": "reasoning" if dial["name"] == "Reasoning" else "system",
            "lucideIcon": DIAL_LUCIDE_ICONS[dial["name"]],
            "iconOnly": True,
        }
        svg = action_icon_svg(icon_action, palette)
        source_name = f"dial_{dial['name'].lower().replace(' ', '_')}.svg"
        (ICONS / source_name).write_text(svg, encoding="utf-8")
        icon_name = f"$@Generic___@MacroAdjustment___{adjustment['name']}.ict"
        (PACKAGE / "ActionIcons" / icon_name).write_text(
            json.dumps(ict_for(svg.encode("utf-8"), source_name, "#000000"), indent=2) + "\n",
            encoding="utf-8",
        )

    docs_dir = DOCS / "live-s" if is_live_s else DOCS
    docs_dir.mkdir(parents=True, exist_ok=True)
    if is_live_s:
        (docs_dir / "codex-controller-live-s-commands.png").write_bytes(live_s_page_preview(config, actions, "commands"))
        (docs_dir / "codex-controller-live-s-agents.png").write_bytes(live_s_page_preview(config, actions, "agents"))
        (docs_dir / "layout-reference.png").write_bytes(live_s_reference_png(config, actions))
    else:
        (docs_dir / "layout-reference.png").write_bytes(reference_png(config, actions))
        (docs_dir / "layout-reference.svg").write_text(reference_svg(config, actions), encoding="utf-8")
    (docs_dir / "shortcut-reference.md").write_text(shortcut_markdown(config, actions), encoding="utf-8")
    profile_map_name = "profile-map-live-s.json" if is_live_s else "profile-map.json"
    (DIST / profile_map_name).write_text(
        json.dumps(
            {
                "profileId": profile_id,
                "packageId": package_id,
                "workspaceIds": workspace_ids,
                "macroIds": {action_id: stable_id("macro", action_id) for action_id in actions},
                "adjustmentIds": {item["displayName"]: item["name"] for item in adjustments},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    if LP4.exists():
        LP4.unlink()
    with zipfile.ZipFile(LP4, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE).as_posix())
    with zipfile.ZipFile(LP4, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Corrupt zip member: {bad}")

    print(f"Built {LP4}")
    print(f"Profile ID: {profile_id}")
    print(f"Actions: {len(action_macros)}; adjustments: {len(adjustments)}; icons: {len(list(ICONS.glob('*.svg')))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("ct", "live-s", "all"), default="all")
    args = parser.parse_args()
    targets = ("ct", "live-s") if args.target == "all" else (args.target,)
    for selected_target in targets:
        build(selected_target)
