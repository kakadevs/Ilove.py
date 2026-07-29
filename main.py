"""
tbm me amas? -- edição especial
================================

Versão aprimorada do clássico "app da declaração" em Tkinter.

Novidades em relação à versão original:
    - Fundo com gradiente animado (rosa -> roxo -> quase preto)
    - Corações flutuando ao fundo, em looping suave
    - Botão "eu não" foge de verdade do cursor (não só quando clicado)
      e fica cada vez mais rápido / menor / com frases diferentes
    - Botão "claro!!" pulsa (efeito de respiração) para chamar atenção
    - Contador de tentativas com mensagens que escalam de forma divertida
    - Tela de celebração com confete animado quando ela aceita
    - Botão para reiniciar a experiência
    - Janela é centralizada na tela e é redimensionável

Nenhuma dependência externa é necessária: só a biblioteca padrão do Python
(tkinter, random, math).

Como rodar:
    python main.py
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from dataclasses import dataclass, field
from tkinter import font as tkfont


# --------------------------------------------------------------------------- #
# Configuração geral
# --------------------------------------------------------------------------- #

WINDOW_TITLE = "tbm me amas? 💌"
WINDOW_W, WINDOW_H = 720, 640

# Paleta de cores (do topo para a base do gradiente)
GRADIENT_TOP = (76, 12, 46)      # roxo/vinho escuro
GRADIENT_BOTTOM = (10, 4, 15)    # quase preto

COLOR_ACCENT = "#ff4d8d"         # rosa vibrante (título / confete)
COLOR_ACCENT_SOFT = "#ffb3c6"    # rosa claro (subtítulo)
COLOR_BTN_YES = "#ff4d8d"
COLOR_BTN_YES_HOVER = "#ff2f77"
COLOR_BTN_NO = "#ffffff"

FONT_FAMILY_CANDIDATES = ["Montserrat", "Poppins", "Segoe UI", "Helvetica", "Arial"]

# Frases que aparecem no botão "eu não" conforme ele foge mais vezes
DODGE_PHRASES = [
    "eu não",
    "hmm, não...",
    "quase!",
    "tenta de novo",
    "ainda não!",
    "impossível 😏",
    "desiste? kk",
    "SÓ CLICA NO OUTRO",
]

# Mensagens que aparecem acima do botão conforme as tentativas aumentam
ESCALATION_MESSAGES = [
    "Eu te amo ❤️",
    "Tem certeza? 🥺",
    "Olha bem pro botão da direita... 👉",
    "O botão 'eu não' não quer ser clicado 😅",
    "Ele já nem sabe mais fugir pra onde 🏃‍♂️💨",
    "Só falta você aceitar o óbvio 💘",
]


def pick_available_font(root: tk.Tk) -> str:
    """Escolhe a primeira fonte disponível no sistema dentre os candidatos."""
    available = set(tkfont.families(root))
    for candidate in FONT_FAMILY_CANDIDATES:
        if candidate in available:
            return candidate
    return "Helvetica"


def lerp_color(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> str:
    """Interpola linearmente entre duas cores RGB e devolve um hex string."""
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


# --------------------------------------------------------------------------- #
# Partículas (corações de fundo + confete de celebração)
# --------------------------------------------------------------------------- #

@dataclass
class FloatingHeart:
    x: float
    y: float
    speed: float
    size: int
    drift: float
    alpha_phase: float
    item: int | None = None


@dataclass
class ConfettiPiece:
    x: float
    y: float
    vx: float
    vy: float
    size: int
    color: str
    rotation: float
    spin: float
    item: int | None = None


# --------------------------------------------------------------------------- #
# Aplicação principal
# --------------------------------------------------------------------------- #

class LoveApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.root.minsize(480, 480)
        self._center_window()

        self.font_family = pick_available_font(self.root)

        self.canvas = tk.Canvas(
            self.root, width=WINDOW_W, height=WINDOW_H,
            highlightthickness=0, bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Estado
        self.width = WINDOW_W
        self.height = WINDOW_H
        self.attempts = 0
        self.no_button_scale = 1.0
        self.pulse_phase = 0.0
        self.hearts: list[FloatingHeart] = []
        self.confetti: list[ConfettiPiece] = []
        self.celebrating = False

        self._build_background()
        self._build_hearts(count=22)
        self._build_scene_widgets()

        self.canvas.bind("<Configure>", self._on_resize)
        self.canvas.bind("<Motion>", self._on_mouse_move)

        self._animate()
        self.root.mainloop()

    # ----------------------------------------------------------------- #
    # Setup
    # ----------------------------------------------------------------- #

    def _center_window(self) -> None:
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WINDOW_W) // 2
        y = (sh - WINDOW_H) // 2
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")

    def _build_background(self) -> None:
        self.bg_lines = []
        steps = 60
        for i in range(steps):
            t = i / (steps - 1)
            color = lerp_color(GRADIENT_TOP, GRADIENT_BOTTOM, t)
            line_id = self.canvas.create_rectangle(
                0, 0, self.width, 0, fill=color, outline=color
            )
            self.bg_lines.append(line_id)
        self._layout_background()

    def _layout_background(self) -> None:
        steps = len(self.bg_lines)
        band_h = max(1, self.height / steps)
        for i, line_id in enumerate(self.bg_lines):
            y0 = i * band_h
            y1 = y0 + band_h + 1
            self.canvas.coords(line_id, 0, y0, self.width, y1)

    def _build_hearts(self, count: int) -> None:
        for _ in range(count):
            h = FloatingHeart(
                x=random.uniform(0, self.width),
                y=random.uniform(0, self.height),
                speed=random.uniform(0.3, 1.1),
                size=random.randint(10, 26),
                drift=random.uniform(-0.4, 0.4),
                alpha_phase=random.uniform(0, math.tau),
            )
            h.item = self.canvas.create_text(
                h.x, h.y, text="❤", fill=COLOR_ACCENT_SOFT,
                font=(self.font_family, h.size),
            )
            self.hearts.append(h)

    def _build_scene_widgets(self) -> None:
        cx = self.width / 2

        self.title_text = self.canvas.create_text(
            cx, self.height * 0.30, text=ESCALATION_MESSAGES[0],
            fill=COLOR_ACCENT, font=(self.font_family, 30, "bold"),
        )
        self.subtitle_text = self.canvas.create_text(
            cx, self.height * 0.30 + 42, text="responde aí 👀",
            fill=COLOR_ACCENT_SOFT, font=(self.font_family, 13),
        )

        # Botão "claro!!" -- fixo, pulsante
        self.yes_btn = tk.Button(
            self.canvas, text="claro!! 💖", bg=COLOR_BTN_YES, fg="white",
            activebackground=COLOR_BTN_YES_HOVER, activeforeground="white",
            relief="flat", bd=0, font=(self.font_family, 15, "bold"),
            padx=22, pady=10, cursor="hand2", command=self._on_accept,
        )
        self.yes_window = self.canvas.create_window(
            cx - 70, self.height * 0.55, window=self.yes_btn
        )

        # Botão "eu não" -- foge do cursor
        self.no_button_base_font = 11
        self.no_btn = tk.Button(
            self.canvas, text=DODGE_PHRASES[0], bg=COLOR_BTN_NO, fg="#590d22",
            relief="flat", bd=0, font=(self.font_family, self.no_button_base_font, "bold"),
            padx=14, pady=8, cursor="hand2", command=self._on_dodge_click,
        )
        self.no_x = cx + 70
        self.no_y = self.height * 0.55
        self.no_window = self.canvas.create_window(
            self.no_x, self.no_y, window=self.no_btn
        )

        self.attempts_text = self.canvas.create_text(
            cx, self.height * 0.90, text="", fill="#9a7b8c",
            font=(self.font_family, 10),
        )

    # ----------------------------------------------------------------- #
    # Eventos
    # ----------------------------------------------------------------- #

    def _on_resize(self, event: tk.Event) -> None:
        if event.width < 10 or event.height < 10:
            return
        self.width, self.height = event.width, event.height
        self._layout_background()
        cx = self.width / 2
        self.canvas.coords(self.title_text, cx, self.height * 0.30)
        self.canvas.coords(self.subtitle_text, cx, self.height * 0.30 + 42)
        self.canvas.coords(self.attempts_text, cx, self.height * 0.90)
        if not self.celebrating:
            self.canvas.coords(self.yes_window, cx - 70, self.height * 0.55)
            self.no_x = min(max(self.no_x, 40), self.width - 40)
            self.no_y = min(max(self.no_y, 40), self.height - 40)
            self.canvas.coords(self.no_window, self.no_x, self.no_y)

    def _on_mouse_move(self, event: tk.Event) -> None:
        if self.celebrating:
            return
        dx = event.x - self.no_x
        dy = event.y - self.no_y
        dist = math.hypot(dx, dy)
        danger_radius = 90 - min(self.attempts * 4, 40)  # fica mais "esperto" com o tempo
        if dist < danger_radius:
            self._flee(event.x, event.y)

    def _on_dodge_click(self) -> None:
        # Se por acaso conseguir clicar, também conta como tentativa e foge de novo
        self._flee(self.no_x, self.no_y, forced=True)

    def _flee(self, from_x: float, from_y: float, forced: bool = False) -> None:
        self.attempts += 1

        margin = 30
        # tenta achar uma posição longe do cursor
        for _ in range(20):
            nx = random.uniform(margin, self.width - margin)
            ny = random.uniform(margin + self.height * 0.15, self.height - margin - self.height * 0.08)
            if math.hypot(nx - from_x, ny - from_y) > 140:
                break
        self.no_x, self.no_y = nx, ny
        self.canvas.coords(self.no_window, self.no_x, self.no_y)

        # Diminui um pouco o botão a cada fuga (até um limite) e troca a frase
        self.no_button_scale = max(0.55, self.no_button_scale - 0.03)
        new_size = max(7, int(self.no_button_base_font * self.no_button_scale))
        phrase = DODGE_PHRASES[min(self.attempts // 2, len(DODGE_PHRASES) - 1)]
        self.no_btn.configure(font=(self.font_family, new_size, "bold"), text=phrase)

        msg = ESCALATION_MESSAGES[min(self.attempts // 3, len(ESCALATION_MESSAGES) - 1)]
        self.canvas.itemconfigure(self.title_text, text=msg)
        self.canvas.itemconfigure(
            self.attempts_text,
            text=f"tentativas de fugir do amor: {self.attempts}",
        )
        self.root.bell() if forced else None

    def _on_accept(self) -> None:
        self.celebrating = True
        self.canvas.itemconfigure(self.title_text, text="eu sabia ❤️")
        self.canvas.itemconfigure(
            self.subtitle_text, text="obrigado por aceitar o óbvio 💘"
        )
        self.canvas.itemconfigure(self.attempts_text, text="")
        self.canvas.delete(self.no_window)
        self.no_btn.destroy()

        cx = self.width / 2
        self.canvas.coords(self.yes_window, cx, self.height * 0.55)
        self.yes_btn.configure(text="de novo! 🔁", command=self._restart)

        self._spawn_confetti(120)

    def _restart(self) -> None:
        self.celebrating = False
        self.attempts = 0
        self.no_button_scale = 1.0
        self.confetti.clear()
        self.canvas.itemconfigure(self.title_text, text=ESCALATION_MESSAGES[0])
        self.canvas.itemconfigure(self.subtitle_text, text="responde aí 👀")

        cx = self.width / 2
        self.canvas.coords(self.yes_window, cx - 70, self.height * 0.55)
        self.yes_btn.configure(text="claro!! 💖", command=self._on_accept)

        self.no_btn = tk.Button(
            self.canvas, text=DODGE_PHRASES[0], bg=COLOR_BTN_NO, fg="#590d22",
            relief="flat", bd=0, font=(self.font_family, self.no_button_base_font, "bold"),
            padx=14, pady=8, cursor="hand2", command=self._on_dodge_click,
        )
        self.no_x = cx + 70
        self.no_y = self.height * 0.55
        self.no_window = self.canvas.create_window(
            self.no_x, self.no_y, window=self.no_btn
        )

    # ----------------------------------------------------------------- #
    # Confete
    # ----------------------------------------------------------------- #

    def _spawn_confetti(self, count: int) -> None:
        colors = [COLOR_ACCENT, COLOR_ACCENT_SOFT, "#ffe066", "#ffffff", "#9d4edd"]
        cx, cy = self.width / 2, self.height * 0.4
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(3, 9)
            piece = ConfettiPiece(
                x=cx, y=cy,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed - 3,
                size=random.randint(4, 9),
                color=random.choice(colors),
                rotation=random.uniform(0, 360),
                spin=random.uniform(-8, 8),
            )
            piece.item = self.canvas.create_rectangle(
                piece.x, piece.y, piece.x + piece.size, piece.y + piece.size,
                fill=piece.color, outline="",
            )
            self.confetti.append(piece)

    # ----------------------------------------------------------------- #
    # Loop de animação
    # ----------------------------------------------------------------- #

    def _animate(self) -> None:
        self._update_hearts()
        self._update_pulse()
        if self.celebrating:
            self._update_confetti()
        self.root.after(16, self._animate)

    def _update_hearts(self) -> None:
        for h in self.hearts:
            h.y -= h.speed
            h.x += h.drift
            h.alpha_phase += 0.02
            if h.y < -20:
                h.y = self.height + 20
                h.x = random.uniform(0, self.width)
            if h.x < -20:
                h.x = self.width + 20
            elif h.x > self.width + 20:
                h.x = -20
            self.canvas.coords(h.item, h.x, h.y)

    def _update_pulse(self) -> None:
        self.pulse_phase += 0.08
        scale = 1.0 + 0.05 * math.sin(self.pulse_phase)
        size = max(13, int(15 * scale))
        try:
            self.yes_btn.configure(font=(self.font_family, size, "bold"))
        except tk.TclError:
            pass

    def _update_confetti(self) -> None:
        gravity = 0.25
        alive: list[ConfettiPiece] = []
        for p in self.confetti:
            p.vy += gravity
            p.x += p.vx
            p.y += p.vy
            p.rotation += p.spin
            self.canvas.coords(p.item, p.x, p.y, p.x + p.size, p.y + p.size)
            if p.y < self.height + 30:
                alive.append(p)
            else:
                self.canvas.delete(p.item)
        self.confetti = alive
        # renova confete ocasionalmente para manter a festa por mais tempo
        if random.random() < 0.04 and len(self.confetti) < 150:
            self._spawn_confetti(12)


if __name__ == "__main__":
    LoveApp()
