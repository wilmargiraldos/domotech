"""
Animated FIGlet banners with rainbow effects for Domo-Tech.

Usage examples:
- Terminal/demo: `python -m domo_tech.ui.animated_banner` (prints short demo)
- In Textual: call `AnimatedBanner.make_rainbow_frame(...)` periodically and update a `Static` widget.

Dependencies: pyfiglet (already in pyproject), colors use ANSI truecolor escape codes.
"""
from __future__ import annotations
import time
import math
from typing import List, Tuple
from pyfiglet import Figlet

# ----------------------- FIGLET RENDERING ------------------------------

def figlet_text(text: str, font: str = "ansi_shadow", width: int | None = None) -> str:
    f = Figlet(font=font)
    if width:
        f.width = width
    return f.renderText(text)

# ----------------------- COLOR HELPERS ---------------------------------

def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    # h in [0,1], s,v in [0,1]
    i = int(h * 6)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    return int(r * 255), int(g * 255), int(b * 255)


def ansi_truecolor(r: int, g: int, b: int, bold: bool = False) -> str:
    # CSI sequence for 24-bit foreground
    return f"\x1b[38;2;{r};{g};{b}m"


def ansi_reset() -> str:
    return "\x1b[0m"

# ----------------------- RAINBOW FRAMES --------------------------------

def colorize_rainbow_lines(lines: List[str], frame: int = 0, variant: int = 0) -> str:
    """
    Apply a rainbow mapping across characters in `lines`.
    - frame: integer frame index used to shift phase
    - variant: 0,1,2 selects one of three rainbow filter presets
    Returns a single string with ANSI escapes.
    """
    out_lines: List[str] = []

    # parameters per variant (frequency, saturation, value, direction)
    presets = [
        (0.12, 0.95, 0.95, 1.0),  # bright, narrow bands
        (0.08, 0.85, 0.98, -1.0), # wider bands, reversed
        (0.06, 0.70, 0.95, 1.0),  # very smooth gradient
    ]
    freq, sat, val, direction = presets[variant % len(presets)]

    # compute maximum line length to normalize positions
    max_len = max((len(ln) for ln in lines), default=1)

    for y, ln in enumerate(lines):
        out = []
        for x, ch in enumerate(ln):
            if ch.isspace():
                out.append(ch)
                continue

            # position-based hue: combine x and y to give 2D effect
            pos = (x + y * 0.5) / max_len
            # phase from frame
            phase = (frame * 2.0 / 60.0)  # moves slowly
            hue = (pos * freq + phase * direction) % 1.0
            r, g, b = hsv_to_rgb(hue, sat, val)
            out.append(f"{ansi_truecolor(r,g,b)}{ch}{ansi_reset()}")
        out_lines.append("".join(out))
    return "\n".join(out_lines)

# ----------------------- PUBLIC FUNCTIONS -------------------------------

def make_rainbow_frame(text: str, font: str = "ansi_shadow", frame: int = 0, variant: int = 0) -> str:
    """Render `text` with FIGlet and return one ANSI-colored frame string."""
    rendered = figlet_text(text, font=font)
    lines = rendered.splitlines()
    return colorize_rainbow_lines(lines, frame=frame, variant=variant)

# ----------------------- DEMO / CLI ------------------------------------

def demo_once():
    """Print three variants in sequence (one frame each) and exit."""
    text = "Domo Tech"
    for variant in range(3):
        frame = make_rainbow_frame(text, font="ansi_shadow", frame=variant * 8, variant=variant)
        print(frame)
        time.sleep(0.65)


def demo():
    """Simple interactive demo: rotate 3 filters continuously until Ctrl-C."""
    text = "Domo Tech"
    try:
        frame = 0
        while True:
            variant = frame % 3
            out = make_rainbow_frame(text, font="ansi_shadow", frame=frame, variant=variant)
            # clear screen then print
            print("\x1b[2J\x1b[H", end="")
            print(out)
            time.sleep(0.12)
            frame += 1
    except KeyboardInterrupt:
        print(ansi_reset())
        return

# ----------------------- TEXTUAL INTEGRATION NOTES ----------------------

def textual_example_update(static_widget, text: str = "Domo Tech", font: str = "ansi_shadow"):
    """
    Example helper to be used inside a Textual App.

    In a `textual` Screen/App you can call this periodically (set_interval)
    and update a `Static` widget's content with the ANSI-colored string.

    static_widget.update(make_rainbow_frame(text, font=font, frame=current_frame, variant=variant))

    Notes: Textual supports ANSI escape codes in widget content because it uses Rich.
    Make sure the widget allows wrapping and is large enough to show the banner.
    """
    raise NotImplementedError("Call `make_rainbow_frame` and update your widget in App code.")

# Make module runnable
if __name__ == "__main__":
    # run short demo_once when executed directly
    demo_once()
