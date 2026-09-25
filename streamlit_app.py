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

# Estilos CSS
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
    
    .info-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
    }

    .last-player-card {
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.15) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid #38bdf8;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
    }

    .badge-topic {
        background-color: #0284c7;
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 3px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# PERSISTENCIA Y MANEJO DE BASE DE DATOS LOCAL/GLOBAL
RANKING_FILE = "ranking_matematica.csv"


def cargar_ranking():
  """Carga la tabla de posiciones desde el archivo global persitente."""
  if os.path.exists(RANKING_FILE):
    try:
      df = pd.read_csv(RANKING_FILE)
      return df.sort_values(by="Puntaje", ascending=False).reset_index(
          drop=True
      )
    except Exception:
      return pd.DataFrame(
          columns=["Nombre", "Puntaje", "Resultado", "FechaHora"]
      )
  return pd.DataFrame(columns=["Nombre", "Puntaje", "Resultado", "FechaHora"])


def guardar_participante(nombre, puntaje, victoria):
  """Guarda el registro con marca de tiempo para identificar al último jugador."""
  df = cargar_ranking()
  fecha_actual = time.strftime("%Y-%m-%d %H:%M:%S")

  nuevo_registro = pd.DataFrame([{
      "Nombre": nombre,
      "Puntaje": puntaje,
      "Resultado": "Ganador 🏆" if victoria else "Finalizado ⏹️",
      "FechaHora": fecha_actual,
  }])

  df = pd.concat([df, nuevo_registro], ignore_index=True)
  df.to_csv(RANKING_FILE, index=False)


def obtener_ultimo_jugador():
  """Retorna los datos del último participante registrado."""
  df = cargar_ranking()
  if not df.empty and "FechaHora" in df.columns:
    df_ordenado_tiempo = df.sort_values(
        by="FechaHora", ascending=False
    ).reset_index(drop=True)
    ultimo = df_ordenado_tiempo.iloc[0]

    df_ranking = cargar_ranking()
    puesto = (
        df_ranking[df_ranking["Nombre"] == ultimo["Nombre"]].index[0] + 1
        if not df_ranking.empty
        else 1
    )

    return {
        "Nombre": ultimo["Nombre"],
        "Puntaje": ultimo["Puntaje"],
        "Resultado": ultimo["Resultado"],
        "FechaHora": ultimo["FechaHora"],
        "Puesto": puesto,
    }
  return None


# Efectos de Sonido
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

QUESTION_BANK = [
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
        "topic": "Ecuación Irracional",
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
        "topic": "Reto Final — Ecuación Irracional",
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
]

# Inicialización de estados
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

  idx = st.session_state.q_index
  base_pts = (
      100
      if idx < 3
      else (150 if idx < 6 else (200 if idx < 9 else 300))
  )

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
st.caption("Desafío Universitario Multijugador")

# PANTALLA PRINCIPAL
if st.session_state.screen == "home":
  # 1. METRICAS GENERALES EN VIVO
  df_rank = cargar_ranking()
  total_partidas = len(df_rank)
  max_puntaje = df_rank["Puntaje"].max() if not df_rank.empty else 0
  top_jugador = df_rank.iloc[0]["Nombre"] if not df_rank.empty else "Nadie aún"

  m1, m2, m3 = st.columns(3)
  m1.metric("🎮 Partidas Jugadas", total_partidas)
  m2.metric("⭐ Récord Máximo", f"{max_puntaje} pts")
  m3.metric("👑 Líder Actual", top_jugador)

  st.write("---")

  # 2. TARJETA DEL ÚLTIMO JUGADOR
  ultimo = obtener_ultimo_jugador()
  if ultimo:
    st.markdown(
        f"""
        <div class="last-player-card">
            ⚡ <b>Última actividad registrada:</b><br>
            👤 <b>Jugador:</b> {ultimo['Nombre']} &nbsp;|&nbsp; 🏆 <b>Puntaje:</b> {ultimo['Puntaje']} pts &nbsp;|&nbsp; 📊 <b>Puesto General:</b> #{ultimo['Puesto']}<br>
            🕒 <small><i>{ultimo['FechaHora']}</i></small>
        </div>
        """,
        unsafe_allow_html=True,
    )

  # 3. REGISTRO DE JUGADOR
  st.subheader("📝 Registro de Participante")
  st.session_state.player_name = st.text_input(
      "Ingresa tu Nombre o Código para figurar en la Tabla Global:",
      value=st.session_state.player_name,
  )

  c1, c2 = st.columns(2)
  with c1:
    if st.button("🚀 Iniciar Reto"):
      start_game()
      st.rerun()
  with c2:
    if st.button("🏆 Ver Tabla de Posiciones"):
      st.session_state.screen = "ranking"
      st.rerun()

  st.write("---")

  # 4. TEMARIO Y COMODINES
  col_left, col_right = st.columns(2)

  with col_left:
    st.markdown("### 📚 Temas Evaluados")
    st.markdown(
        """
        <span class="badge-topic">Ecuaciones Lineales</span>
        <span class="badge-topic">Ecuaciones Cuadráticas</span>
        <span class="badge-topic">Fracciones Algebraicas</span>
        <span class="badge-topic">Ecuaciones Irracionales</span>
        <span class="badge-topic">Problemas de Contexto</span>
        """,
        unsafe_allow_html=True,
    )

  with col_right:
    st.markdown("### 🛠️ Comodines del Juego")
    st.markdown("""
        * 🛡️ **Escudo:** Evita perder vida en un fallo.
        * ⚡ **Congelar:** Pausa el temporizador de 20s.
        * 💣 **50 / 50:** Elimina 2 alternativas incorrectas.
        """)

  # 5. REGLAS Y MECÁNICAS
  with st.expander("ℹ️ ¿Cómo funciona la puntuación y las ráfagas?"):
    st.write("""
        - **Tiempo por pregunta:** Tienes **20 segundos** para responder cada problema.
        - **Vidas:** Inicias con **100 HP**. Cada error o tiempo agotado te restará **20 HP**.
        - **Rachas de aciertos:** Responder consecutivamente multiplica tus puntos y hace más daño al tiempo de respuesta.
        - **Resoluciones paso a paso:** Al contestar (correcta o incorrectamente) obtendrás la solución desarrollada con formato matemático.
        """)

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

  # RENDERIZADO DE PREGUNTA Y OPCIONES
  st.divider()
  q = st.session_state.questions[st.session_state.q_index]
  st.caption(f"Tema: **{q['topic']}**")
  st.markdown(f"### {q['q']}")

  for idx, opt in enumerate(q["o"]):
    label = f"{chr(65+idx)}) {opt}"
    if idx in st.session_state.disabled_options:
      st.button(f"🚫 {opt}", key=f"opt_{idx}", disabled=True)
    else:
      if st.button(label, key=f"opt_{idx}", disabled=st.session_state.answered):
        check_answer(idx)
        st.rerun()

  # TEMPORIZADOR
  TIME_LIMIT = 20
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

  # RETROALIMENTACIÓN
  if st.session_state.answered:
    correct_option_text = f"{chr(65 + q['a'])}) {q['o'][q['a']]}"

    if st.session_state.last_result == "correct":
      st.success(
          "✅ **¡Respuesta Correcta!**\n\n"
          f"**Opción Elegida:** {correct_option_text}\n\n"
          f"{q['e']}"
      )
      if st.button("Siguiente Pregunta ➔"):
        next_question()
        st.rerun()

    elif st.session_state.last_result == "shield_absorbed":
      st.info(
          "🛡️ **¡Escudo Activado! Se evitó la penalización de vida.**\n\n"
          f"**Respuesta Correcta:** {correct_option_text}\n\n"
          f"{q['e']}"
      )
      if st.button("Siguiente Pregunta ➔"):
        next_question()
        st.rerun()

    elif st.session_state.last_result == "timeout":
      st.error(
          "⏰ **¡SE TE ACABÓ EL TIEMPO!**\n\n"
          f"La respuesta correcta era: **{correct_option_text}**\n\n"
          f"{q['e']}"
      )
      if st.button("Siguiente Pregunta ➔"):
        next_question()
        st.rerun()

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
  else:
    st.title("⏹️ INTENTO FINALIZADO")

  r1, r2 = st.columns(2)
  r1.metric("Puntuación Total", st.session_state.score)
  r2.metric("Participante", st.session_state.player_name)

  c1, c2 = st.columns(2)
  if c1.button("🔁 Intentar de Nuevo"):
    start_game()
    st.rerun()
  if c2.button("🏆 Ver Tabla General"):
    st.session_state.screen = "ranking"
    st.rerun()

# TABLA DE RANKING MULTIJUGADOR
elif st.session_state.screen == "ranking":
  st.subheader("🏆 Tabla Global de Posiciones Multijugador")

  if st.button("🔄 Actualizar Tabla"):
    st.rerun()

  df_ranking = cargar_ranking()

  if not df_ranking.empty:
    st.dataframe(df_ranking, use_container_width=True)
  else:
    st.info("Aún no hay participantes en la tabla global.")

  if st.button("Volver al Inicio"):
    st.session_state.screen = "home"
    st.rerun()
