import os
import random
import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Álgebra Master | Desafío Matemático",
    page_icon="🧮",
    layout="centered",
)

# Estilos CSS con contraste visual elevado
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Poppins', sans-serif;
        color: #f8fafc;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 800;
        letter-spacing: 1px;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        background-color: #334155;
        color: #f8fafc;
        border: 2px solid #38bdf8;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        border-color: #4ade80;
        background-color: #1e293b;
        color: #ffffff;
        transform: scale(1.01);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Persistencia local de participantes
RANKING_FILE = "ranking_matematica.csv"


def cargar_ranking():
  if os.path.exists(RANKING_FILE):
    try:
      return pd.read_csv(RANKING_FILE)
    except Exception:
      return pd.DataFrame(columns=["Nombre", "Puntaje", "Resultado"])
  return pd.DataFrame(columns=["Nombre", "Puntaje", "Resultado"])


def guardar_participante(nombre, puntaje, victoria):
  df = cargar_ranking()
  nuevo_registro = pd.DataFrame([{
      "Nombre": nombre,
      "Puntaje": puntaje,
      "Resultado": "Ganador 🏆" if victoria else "Finalizado ⏹️",
  }])
  df = pd.concat([df, nuevo_registro], ignore_index=True)
  df = df.sort_values(by="Puntaje", ascending=False).reset_index(drop=True)
  df.to_csv(RANKING_FILE, index=False)


# Efectos de Sonido Web Audio API
SFX_SCRIPT = """
<script>
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playTone(freq, type, duration) {
    if (audioCtx.state === 'suspended') { audioCtx.resume(); }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + duration);
    osc.stop(audioCtx.currentTime + duration);
}

function sfxCorrect() {
    playTone(523.25, 'sine', 0.1);
    setTimeout(() => playTone(659.25, 'sine', 0.15), 100);
    setTimeout(() => playTone(783.99, 'sine', 0.3), 200);
}

function sfxWrong() {
    playTone(180, 'sawtooth', 0.2);
    setTimeout(() => playTone(110, 'sawtooth', 0.4), 150);
}

function sfxPowerup() {
    playTone(400, 'triangle', 0.1);
    setTimeout(() => playTone(800, 'triangle', 0.2), 80);
}
</script>
"""

# BANCO COMPLETO DE PREGUNTAS (Incluye los ejercicios obligatorios + adicionales complejos)
QUESTION_BANK = [
    # Preguntas exactas requeridas
    {
        "topic": "Ecuación Lineal",
        "q": "Determina el valor de x:\n\n$$4(2x - 3) - 3(x + 2) = 2x + 7$$",
        "o": ["22/3", "23/3", "25/3", "27/3"],
        "a": 2,
        "e": (
            "**Resolución:**\n\n$$4(2x - 3) - 3(x + 2) = 2x + 7$$\n\n$$8x - 12 -"
            " 3x - 6 = 2x + 7$$\n\n$$5x - 18 = 2x + 7$$\n\n$$3x = 25$$\n\n$$x ="
            " 25/3$$"
        ),
    },
    {
        "topic": "Ecuación Lineal con Fracciones",
        "q": "Resuelve:\n\n$$\\frac{3x - 2}{4} + \\frac{x + 1}{2} = 7$$",
        "o": ["26/5", "28/5", "30/5", "32/5"],
        "a": 1,
        "e": (
            "**Resolución:**\n\nMultiplicamos toda la ecuación por"
            " 4:\n\n$$3x - 2 + 2(x + 1) = 28$$\n\n$$3x - 2 + 2x + 2 ="
            " 28$$\n\n$$5x = 28$$\n\n$$x = 28/5$$"
        ),
    },
    {
        "topic": "Ecuación Lineal con Paréntesis",
        "q": (
            "Determina el valor de x:\n\n$$7(x - 2) - 2(3x + 1) = 4(x - 5) +"
            " 9$$"
        ),
        "o": ["-5/3", "-4/3", "5/3", "4/3"],
        "a": 0,
        "e": (
            "**Resolución:**\n\n$$7x - 14 - 6x - 2 = 4x - 20 + 9$$\n\n$$x - 16"
            " = 4x - 11$$\n\n$$x - 4x = -11 + 16$$\n\n$$-3x = 5$$\n\n$$x ="
            " -5/3$$"
        ),
    },
    {
        "topic": "Ecuación Cuadrática",
        "q": "Resuelve:\n\n$$x^2 - 9x + 20 = 0$$",
        "o": ["x = 2, 10", "x = 4, 5", "x = 3, 6", "x = -4, -5"],
        "a": 1,
        "e": (
            "**Resolución:**\n\n$$x^2 - 9x + 20 = 0$$\n\n$$(x - 4)(x - 5) ="
            " 0$$\n\n$$x = 4 \\quad \\text{o} \\quad x = 5$$"
        ),
    },
    {
        "topic": "Ecuación Cuadrática",
        "q": "Determina las soluciones:\n\n$$2x^2 - 7x + 3 = 0$$",
        "o": ["x = 3, 1/2", "x = 2, 3/2", "x = -3, 1/2", "x = 3, -1/2"],
        "a": 0,
        "e": (
            "**Resolución:**\n\n$$2x^2 - 7x + 3 = 0$$\n\n$$(2x - 1)(x - 3) ="
            " 0$$\n\n$$2x - 1 = 0 \\implies x = 1/2$$\n\n$$x - 3 = 0 \\implies"
            " x = 3$$"
        ),
    },
    {
        "topic": "Ecuación Cuadrática Contextualizada",
        "q": (
            "El área de un terreno rectangular es de 84 m². Su largo mide 5"
            " metros más que su ancho. ¿Cuál es el ancho del terreno?"
        ),
        "o": ["6 m", "7 m", "8 m", "9 m"],
        "a": 1,
        "e": (
            "**Resolución:**\n\nSea $x$ el ancho. Largo = $x + 5$.\n\nÁrea ="
            " largo × ancho $\\implies x(x + 5) = 84$\n\n$$x^2 + 5x - 84 ="
            " 0$$\n\n$$(x + 12)(x - 7) = 0$$\n\n$$x = -12 \\quad \\text{o}"
            " \\quad x = 7$$\n\nComo una medida de longitud no puede ser"
            " negativa: **x = 7 m**"
        ),
    },
    {
        "topic": "Ecuación Fraccionaria",
        "q": (
            "Resuelve considerando las restricciones:\n\n$$\\frac{2}{x} +"
            " \\frac{3}{x + 1} = 2$$"
        ),
        "o": ["x = 2, -1/2", "x = 3, -1/2", "x = 2, 3/2", "x = -2, 3/2"],
        "a": 0,
        "e": (
            "**Resolución:**\n\nRestricciones: $x \\neq 0$ y $x \\neq"
            " -1$.\n\nMultiplicamos por $x(x + 1)$:\n\n$$2(x + 1) + 3x = 2x(x"
            " + 1)$$\n\n$$2x + 2 + 3x = 2x^2 + 2x$$\n\n$$2x^2 - 3x - 2 ="
            " 0$$\n\n$$(2x + 1)(x - 2) = 0$$\n\n$$x = -1/2 \\quad \\text{o}"
            " \\quad x = 2$$"
        ),
    },
    {
        "topic": "Ecuación Fraccionaria",
        "q": (
            "Determina el conjunto solución:\n\n$$\\frac{x + 2}{x - 1} +"
            " \\frac{2}{x - 1} = 3$$"
        ),
        "o": ["x = 1", "x = 5/2", "x = 7/2", "x = 4"],
        "a": 2,
        "e": (
            "**Resolución:**\n\nRestricción: $x \\neq 1$.\n\n$$\\frac{x + 2 +"
            " 2}{x - 1} = 3$$\n\n$$\\frac{x + 4}{x - 1} = 3$$\n\n$$x + 4 = 3(x"
            " - 1)$$\n\n$$x + 4 = 3x - 3$$\n\n$$7 = 2x \\implies x = 7/2$$"
        ),
    },
    {
        "topic": "Ecuación Irregional",
        "q": "Resuelve:\n\n$$\\sqrt{x + 6} = x$$",
        "o": ["x = 2", "x = 3", "x = 4", "x = 6"],
        "a": 1,
        "e": (
            "**Resolución:**\n\nElevamos al cuadrado ambos lados:\n\n$$x + 6 ="
            " x^2$$\n\n$$x^2 - x - 6 = 0$$\n\n$$(x - 3)(x + 2) = 0$$\n\n$$x = 3"
            " \\quad \\text{o} \\quad x = -2$$\n\nVerificamos en la ecuación"
            " original:\nPara $x = 3$: $\\sqrt{3+6} = 3 \\implies 3 = 3$ (V)\nPara"
            " $x = -2$: $\\sqrt{-2+6} = -2 \\implies 2 \\neq -2$ (F)\n\nPor lo"
            " tanto, **x = 3**."
        ),
    },
    {
        "topic": "Reto Final — Ecuación Irracial",
        "q": "Determina la solución válida:\n\n$$\\sqrt{x + 4} + \\sqrt{x} = 4$$",
        "o": ["x = 1", "x = 9/4", "x = 3", "x = 4"],
        "a": 1,
        "e": (
            "**Resolución:**\n\n$$\\sqrt{x + 4} = 4 - \\sqrt{x}$$\n\nElevamos"
            " al cuadrado:\n\n$$x + 4 = 16 - 8\\sqrt{x} + x$$\n\n$$4 = 16 -"
            " 8\\sqrt{x}$$\n\n$$8\\sqrt{x} = 12 \\implies \\sqrt{x} ="
            " 3/2$$\n\n$$x = (3/2)^2 = 9/4$$\n\nVerificación:\n$$\\sqrt{9/4 +"
            " 4} + \\sqrt{9/4} = \\sqrt{25/4} + 3/2 = 5/2 + 3/2 = 4$$ (V)\n\nPor"
            " lo tanto: **x = 9/4**."
        ),
    },
    # Adicionales de alta dificultad para banco expandido
    {
        "topic": "Ecuación Fraccionaria Avanzada",
        "q": (
            "Encuentra las soluciones reales:\n\n$$\\frac{x}{x-2} +"
            " \\frac{1}{x+2} = \\frac{8}{x^2-4}$$"
        ),
        "o": ["x = 2, -3", "x = -3", "x = 2", "x = 3, -2"],
        "a": 1,
        "e": (
            "**Resolución:**\n\nMultiplicamos por el MCM = $(x-2)(x+2)$ con $x"
            " \\neq \\pm 2$:\n\n$$x(x+2) + 1(x-2) = 8$$\n\n$$x^2 + 2x + x - 2 ="
            " 8$$\n\n$$x^2 + 3x - 10 = 0$$\n\n$$(x+5)(x-2) = 0 \\implies x = -5"
            " \\quad \\text{o} \\quad x = 2$$\n\nComo $x \\neq 2$ por"
            " restricción de dominio, descartamos $x=2$.\n\nSolución: **x ="
            " -5**."
        ),
    },
    {
        "topic": "Ecuación Irracial Doble",
        "q": "Resuelve para x:\n\n$$\\sqrt{2x + 3} - \\sqrt{x + 1} = 1$$",
        "o": ["x = -1, 3", "x = 3", "x = 0, 3", "x = 1"],
        "a": 2,
        "e": (
            "**Resolución:**\n\n$$\\sqrt{2x + 3} = 1 + \\sqrt{x +"
            " 1}$$\n\nElevamos al cuadrado:\n\n$$2x + 3 = 1 + 2\\sqrt{x + 1} +"
            " x + 1$$\n\n$$x + 1 = 2\\sqrt{x + 1}$$\n\nElevamos al cuadrado de"
            " nuevo:\n\n$$(x + 1)^2 = 4(x + 1)$$\n\n$$(x + 1)^2 - 4(x + 1) ="
            " 0$$\n\n$$(x + 1)(x - 3) = 0 \\implies x = -1 \\quad \\text{o}"
            " \\quad x = 3$$\n\nProbando valores: $x=0 \\implies \\sqrt{3}-1"
            " \\neq 1$; para $x=3 \\implies \\sqrt{9}-\\sqrt{4} = 3-2=1$ (V);\n"
            "para $x=-1 \\implies \\sqrt{1}-0 = 1$ (V).\nSolución válida: **x"
            " = -1, 3**."
        ),
    },
]

# Inicialización del estado
if "screen" not in st.session_state:
  st.session_state.screen = "home"
if "player_name" not in st.session_state:
  st.session_state.player_name = "Estudiante"
if "score" not in st.session_state:
  st.session_state.score = 0
if "streak" not in st.session_state:
  st.session_state.streak = 0
if "player_hp" not in st.session_state:
  st.session_state.player_hp = 100
if "boss_hp" not in st.session_state:
  st.session_state.boss_hp = 100
if "q_index" not in st.session_state:
  st.session_state.q_index = 0
if "questions" not in st.session_state:
  st.session_state.questions = []
if "answered" not in st.session_state:
  st.session_state.answered = False

if "shield" not in st.session_state:
  st.session_state.shield = False
if "time_freeze" not in st.session_state:
  st.session_state.time_freeze = False
if "disabled_options" not in st.session_state:
  st.session_state.disabled_options = []

# Música de fondo opcional via audio component
components.html(
    f"""
    {SFX_SCRIPT}
    <audio id="bg-music" loop autoplay>
        <source src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>
    <script>
        var audio = document.getElementById("bg-music");
        if (audio) {{ audio.volume = 0.12; }}
    </script>
""",
    height=0,
)


def start_game():
  # Selecciona 10 preguntas al azar del banco completo
  st.session_state.questions = random.sample(
      QUESTION_BANK, min(10, len(QUESTION_BANK))
  )
  st.session_state.q_index = 0
  st.session_state.score = 0
  st.session_state.streak = 0
  st.session_state.player_hp = 100
  st.session_state.boss_hp = 100
  st.session_state.shield = False
  st.session_state.time_freeze = False
  st.session_state.disabled_options = []
  st.session_state.answered = False
  st.session_state.start_time = time.time()
  st.session_state.screen = "game"


def apply_powerup(kind):
  components.html(f"{SFX_SCRIPT}<script>sfxPowerup();</script>", height=0)
  if kind == "shield":
    st.session_state.shield = True
  elif kind == "freeze":
    st.session_state.time_freeze = True
  elif kind == "bomb":
    q = st.session_state.questions[st.session_state.q_index]
    wrong = [i for i in range(len(q["o"])) if i != q["a"]]
    st.session_state.disabled_options = random.sample(wrong, 2)


def check_answer(opt_idx, timeout=False):
  if st.session_state.answered:
    return
  st.session_state.answered = True
  q = st.session_state.questions[st.session_state.q_index]

  # Asignación progresiva de puntos según el número de pregunta
  idx = st.session_state.q_index
  if idx < 3:
    base_pts = 100
  elif idx < 6:
    base_pts = 150
  elif idx < 9:
    base_pts = 200
  else:
    base_pts = 300

  if timeout or opt_idx != q["a"]:
    if st.session_state.shield:
      st.session_state.shield = False
      st.session_state.last_result = "shield_absorbed"
      components.html(
          f"{SFX_SCRIPT}<script>sfxPowerup();</script>", height=0
      )
    else:
      components.html(f"{SFX_SCRIPT}<script>sfxWrong();</script>", height=0)
      st.session_state.player_hp -= 20
      st.session_state.streak = 0
      st.session_state.last_result = "timeout" if timeout else "wrong"
  else:
    components.html(f"{SFX_SCRIPT}<script>sfxCorrect();</script>", height=0)
    st.session_state.streak += 1
    damage = 10 + (st.session_state.streak * 5)
    st.session_state.boss_hp = max(0, st.session_state.boss_hp - damage)
    st.session_state.score += base_pts + (st.session_state.streak * 20)
    st.session_state.last_result = "correct"


def next_question():
  st.session_state.answered = False
  st.session_state.time_freeze = False
  st.session_state.disabled_options = []
  st.session_state.q_index += 1

  if (
      st.session_state.q_index >= len(st.session_state.questions)
      or st.session_state.player_hp <= 0
  ):
    guardar_participante(
        st.session_state.player_name,
        st.session_state.score,
        st.session_state.player_hp > 0,
    )
    st.session_state.screen = "result"
  else:
    st.session_state.start_time = time.time()


st.title("🧮 ÁLGEBRA MASTER")
st.caption("Desafío Universitario de Ecuaciones & Álgebra Avanzada")

# PANTALLA PRINCIPAL
if st.session_state.screen == "home":
  st.subheader("📝 Registro de Participante")
  st.write(
      "Pon a prueba tus conocimientos en ecuaciones lineales, cuadráticas,"
      " fraccionarias e irracionales."
  )
  st.session_state.player_name = st.text_input(
      "Ingresa tu Nombre / Código de Estudiante:",
      value=st.session_state.player_name,
  )

  c1, c2 = st.columns(2)
  with c1:
    if st.button("🚀 Iniciar Reto"):
      start_game()
      st.rerun()
  with c2:
    if st.button("🏆 Tabla de Participantes"):
      st.session_state.screen = "ranking"
      st.rerun()

# PANTALLA DE JUEGO
elif st.session_state.screen == "game":
  col_hp1, col_hp2 = st.columns(2)
  with col_hp1:
    st.write(f"❤️ **Vida:** {st.session_state.player_hp}%")
    st.progress(max(0, st.session_state.player_hp) / 100)
  with col_hp2:
    st.write(
        f"📌 **Pregunta:** {st.session_state.q_index + 1} /"
        f" {len(st.session_state.questions)}"
    )
    st.progress((st.session_state.q_index + 1) / 10)

  m1, m2, m3 = st.columns(3)
  m1.metric("Puntuación", st.session_state.score)
  m2.metric("Racha", f"x{st.session_state.streak}")
  m3.metric("Escudo", "🛡️ ACTIVO" if st.session_state.shield else "INACTIVO")

  st.write("---")
  st.caption("Comodines disponibles:")
  p1, p2, p3 = st.columns(3)
  if p1.button(
      "🛡️ Escudo",
      disabled=st.session_state.shield or st.session_state.answered,
  ):
    apply_powerup("shield")
    st.rerun()
  if p2.button(
      "⚡ Congelar Tiempo",
      disabled=st.session_state.time_freeze or st.session_state.answered,
  ):
    apply_powerup("freeze")
    st.rerun()
  if p3.button(
      "💣 50 / 50",
      disabled=len(st.session_state.disabled_options) > 0
      or st.session_state.answered,
  ):
    apply_powerup("bomb")
    st.rerun()

  # Temporizador dinámico
  TIME_LIMIT = 25
  if not st.session_state.answered and not st.session_state.time_freeze:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(TIME_LIMIT - elapsed))

    st.progress(remaining / TIME_LIMIT, text=f"⏱️ Tiempo restante: {remaining}s")

    if remaining <= 0:
      check_answer(None, timeout=True)
      st.rerun()
    else:
      time.sleep(1)
      st.rerun()

  elif st.session_state.time_freeze and not st.session_state.answered:
    st.info("⚡ ¡TIEMPO CONGELADO PARA ESTA PREGUNTA!")

  st.divider()
  q = st.session_state.questions[st.session_state.q_index]
  st.caption(f"Tema: **{q['topic']}**")
  st.markdown(f"### {q['q']}")

  # Renderizado de alternativas
  for idx, opt in enumerate(q["o"]):
    label = f"{chr(65+idx)}) {opt}"
    if idx in st.session_state.disabled_options:
      st.button(f"🚫 {opt}", key=f"opt_{idx}", disabled=True)
    else:
      if st.button(label, key=f"opt_{idx}", disabled=st.session_state.answered):
        check_answer(idx)
        st.rerun()

  # Retroalimentación con colores diferenciados
  if st.session_state.answered:
    correct_option_text = f"{chr(65 + q['a'])}) {q['o'][q['a']]}"

    if st.session_state.last_result == "correct":
      st.success(
          "✅ **¡Respuesta Correcta!**\n\n"
          f"**Opción Elegida:** {correct_option_text}\n\n"
          f"{q['e']}"
      )
    elif st.session_state.last_result == "shield_absorbed":
      st.info(
          "🛡️ **¡Escudo Activado! Se evito la penalización de vida.**\n\n"
          f"**Respuesta Correcta:** {correct_option_text}\n\n"
          f"{q['e']}"
      )
    elif st.session_state.last_result == "timeout":
      st.error(
          "⏰ **¡SE TE ACABÓ EL TIEMPO!**\n\n"
          f"La respuesta correcta era: **{correct_option_text}**\n\n"
          f"{q['e']}"
      )
    else:
      st.error(
          "❌ **Respuesta Incorrecta.**\n\n"
          f"La respuesta correcta era: **{correct_option_text}**\n\n"
          f"{q['e']}"
      )

    if st.button("Siguiente Pregunta ➔"):
      next_question()
      st.rerun()

# PANTALLA DE RESULTADOS
elif st.session_state.screen == "result":
  if st.session_state.player_hp > 0:
    st.balloons()
    st.title("🎉 ¡FELICITACIONES! DESAFÍO COMPLETADO")
    st.write(
        "Has demostrado un gran dominio de las ecuaciones universitarias."
    )
  else:
    st.title("⏹️ INTENTO FINALIZADO")
    st.write("Sigue practicando para mejorar tu puntuación en la materia.")

  r1, r2 = st.columns(2)
  r1.metric("Puntuación Total", st.session_state.score)
  r2.metric("Participante", st.session_state.player_name)

  c1, c2 = st.columns(2)
  if c1.button("🔁 Intentar de Nuevo"):
    start_game()
    st.rerun()
  if c2.button("🏆 Ver Registro de Participantes"):
    st.session_state.screen = "ranking"
    st.rerun()

# TABLA DE PARTICIPANTES (RANKING)
elif st.session_state.screen == "ranking":
  st.subheader("🏆 Registro de Participantes")
  df_ranking = cargar_ranking()

  if not df_ranking.empty:
    st.dataframe(df_ranking, use_container_width=True)
  else:
    st.info("Aún no hay participantes registrados.")

  if st.button("Volver al Inicio"):
    st.session_state.screen = "home"
    st.rerun()
