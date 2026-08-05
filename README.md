# Também me amas? 💌 — Edição Especial

Versão totalmente redesenhada e interativa do clássico "app da declaração"
em Python + Tkinter. O objetivo continua o mesmo (fazer a pessoa clicar em
"claro!!"), mas agora com layout, animações e experiência muito mais ricos.

![status](https://img.shields.io/badge/status-pronto%20para%20usar-ff4d8d)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![deps](https://img.shields.io/badge/depend%C3%AAncias-nenhuma-success)

---

## ✨ O que mudou em relação à versão original

| Antes | Agora |
|---|---|
| Fundo preto liso | Gradiente animado (vinho → roxo → preto) |
| Sem elementos decorativos | Corações flutuando suavemente ao fundo |
| Botão "eu não" só fugia quando clicado bem no centro | Foge de verdade sempre que o cursor se aproxima, ficando mais ágil e menor a cada tentativa |
| Texto fixo "Eu te amo ❤️" | Mensagens que vão mudando conforme o número de tentativas |
| `messagebox.showinfo` genérico ao aceitar | Tela de celebração dentro da própria janela, com **confete animado** |
| Sem forma de repetir | Botão "de novo! 🔁" reinicia toda a experiência |
| Janela em posição aleatória da tela | Janela centralizada automaticamente e redimensionável |
| Fonte fixa (podia não existir no sistema) | Detecção automática de uma fonte disponível (Montserrat, Poppins, Segoe UI, etc.) |

---

## 🖥️ Como rodar

Não há nenhuma dependência externa — apenas a biblioteca padrão do Python.

```bash
# 1. Certifique-se de ter o Tkinter instalado
#    (no Linux, às vezes precisa instalar separadamente)
sudo apt-get install python3-tk        # Debian/Ubuntu
# no Windows e macOS o Tkinter já vem junto com o Python padrão

# 2. Rode o programa
python main.py
```

Requer **Python 3.8+**.

---

## 🎮 Como funciona a experiência

1. A janela abre centralizada, com um fundo em gradiente e corações
   flutuando ao fundo.
2. O botão rosa **"claro!! 💖"** fica pulsando suavemente, chamando atenção.
3. O botão branco **"eu não"** foge assim que o cursor se aproxima dele —
   não é preciso clicar nele para ele fugir.
4. A cada fuga:
   - o contador de tentativas aumenta;
   - o botão "eu não" fica um pouco menor e mais rápido de reagir;
   - a frase dentro dele muda (fica cada vez mais "sem graça");
   - a mensagem principal acima também evolui, incentivando a aceitar.
5. Ao clicar em **"claro!! 💖"**, a tela vira uma celebração: mensagem de
   agradecimento, confete caindo com física simples (gravidade + rotação) e
   um botão para reiniciar tudo do zero.

---

## 🗂️ Estrutura do projeto

```
.
├── main.py       # aplicação inteira (UI, animações e lógica de estado)
└── README.md     # este arquivo
```

O código está organizado em uma única classe, `LoveApp`, dividida por
responsabilidade:

- **Setup** — criação da janela, canvas, fundo em gradiente e widgets.
- **Eventos** — resposta a movimento do mouse, cliques e redimensionamento
  da janela.
- **Confete** — geração e física das partículas de celebração.
- **Loop de animação** — atualizado a cada ~16 ms (~60 FPS) via
  `root.after`, cuidando dos corações de fundo, do pulso do botão e do
  confete.

Duas pequenas classes de dados (`FloatingHeart` e `ConfettiPiece`) guardam o
estado de cada partícula (posição, velocidade, tamanho, etc.).

---

## 🔧 Personalizando

Praticamente tudo pode ser ajustado no topo do `main.py`, na seção
**"Configuração geral"**:

- `WINDOW_TITLE`, `WINDOW_W`, `WINDOW_H` — título e tamanho inicial da janela.
- `GRADIENT_TOP` / `GRADIENT_BOTTOM` — cores do gradiente de fundo (RGB).
- `COLOR_ACCENT`, `COLOR_ACCENT_SOFT`, `COLOR_BTN_YES`, `COLOR_BTN_NO` —
  paleta de cores dos textos e botões.
- `DODGE_PHRASES` — lista de frases que aparecem no botão "eu não" conforme
  ele foge mais vezes.
- `ESCALATION_MESSAGES` — lista de mensagens principais que vão mudando com
  o número de tentativas.
- `FONT_FAMILY_CANDIDATES` — ordem de preferência de fontes; o programa usa
  a primeira que existir no sistema.

Não é necessário mexer no restante do código para trocar textos, cores ou
tamanhos.

---

## 🐞 Solução de problemas

- **`ModuleNotFoundError: No module named 'tkinter'`** — instale o pacote
  do Tkinter para o seu sistema (no Ubuntu/Debian:
  `sudo apt-get install python3-tk`).
- **As fontes parecem "genéricas"** — o programa escolhe automaticamente
  entre as fontes disponíveis; instale Montserrat ou Poppins no sistema
  para o visual mais próximo do pretendido.
- **Muito confete deixando tudo lento** — reduza o valor passado em
  `self._spawn_confetti(120)` dentro de `_on_accept`.

---

Feito com ❤️ (e um pouco de Tkinter).
