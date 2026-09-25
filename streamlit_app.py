import random
import time
import streamlit as st

st.set_page_config(
    page_title="Álgebra Battle | Desafío Universitario",
    page_icon="⚡",
    layout="centered",
)

# Estilos CSS personalizados
st.markdown(
    """
    <style>
    .main { background: radial-gradient(circle at top, #20295a 0%, #090d1f 100%); color: #eef2ff; }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: bold; background-color: #1b2448; color: #eef2ff; border: 1px solid #303b68; }
    .stButton>button:hover { border-color: #19d3ae; background-color: #223057; }
    </style>
""",
    unsafe_allow_html=True,
)

QUESTION_BANK = [
    {
        "topic": "Operaciones con reales",
        "q": "Calcula: 18 − 3 × 4 + 2",
        "o": ["8", "14", "68", "2"],
        "a": 0,
        "e": "Primero la multiplicación: 3 × 4 = 12. Luego 18 − 12 + 2 = 8.",
    },
    {
        "topic": "Operaciones con reales",
        "q": "Calcula: (−5)² − 3²",
        "o": ["−16", "16", "34", "−34"],
        "a": 1,
        "e": "(−5)² = 25 y 3² = 9. Entonces 25 − 9 = 16.",
    },
    {
        "topic": "Fracciones y potencias",
        "q": "Calcula: 1/2 + 3/4",
        "o": ["4/6", "5/4", "7/8", "1/4"],
        "a": 1,
        "e": "El común denominador es 4: 1/2 = 2/4. Entonces 2/4 + 3/4 = 5/4.",
    },
    {
        "topic": "Fracciones y potencias",
        "q": "Simplifica: 2³ × 2²",
        "o": ["2⁵", "2⁶", "4⁵", "2¹"],
        "a": 0,
        "e": (
            "Al multiplicar potencias de la misma base se suman los"
            " exponentes: 3 + 2 = 5."
        ),
    },
    {
        "topic": "Ecuaciones de primer grado",
        "q": "Resuelve: 3x + 7 = 22",
        "o": ["x = 3", "x = 5", "x = 7", "x = 9"],
        "a": 1,
        "e": "Resta 7: 3x = 15. Divide entre 3: x = 5.",
    },
    {
        "topic": "Ecuaciones de primer grado",
        "q": "Resuelve: 5(x − 2) = 20",
        "o": ["x = 2", "x = 4", "x = 6", "x = 8"],
        "a": 2,
        "e": "Divide entre 5: x − 2 = 4. Suma 2: x = 6.",
    },
    {
        "topic": "Productos notables",
        "q": "¿Cuál es el desarrollo de (x + 3)²?",
        "o": ["x² + 9", "x² + 3x + 9", "x² + 6x + 9", "x² + 6x + 3"],
        "a": 2,
        "e": "Cuadrado de una suma: x² + 2·x·3 + 3² = x² + 6x + 9.",
    },
    {
        "topic": "Productos notables",
        "q": "Desarrolla: (a − 4)(a + 4)",
        "o": ["a² − 16", "a² + 16", "a² − 8a + 16", "a² + 8a + 16"],
        "a": 0,
        "e": "Es una diferencia de cuadrados: a² − 4² = a² − 16.",
    },
    {
        "topic": "Factorización",
        "q": "Factoriza: x² + 5x + 6",
        "o": [
            "(x+1)(x+6)",
            "(x+2)(x+3)",
            "(x−2)(x−3)",
            "(x+5)(x+1)",
        ],
        "a": 1,
        "e": "Buscamos dos números que sumen 5 y multipliquen 6: 2 y 3.",
    },
    {
        "topic": "Factorización",
        "q": "Factor común: 6x² + 9x",
        "o": ["3x(2x+3)", "6x(x+9)", "x(6x+9x)", "3(2x²+9x)"],
        "a": 0,
        "e": "El máximo factor común es 3x: 3x(2x + 3).",
    },
    {
        "topic": "Ecuaciones cuadráticas",
        "q": "Resuelve: x² − 9 = 0",
        "o": ["x = 3 solamente", "x = −3 solamente", "x = ±3", "x = 9"],
        "a": 2,
        "e": "x² = 9, por lo tanto x = 3 o x = −3.",
    },
    {
        "topic": "Ecuaciones cuadráticas",
        "q": "En x² − 5x + 6 = 0, las raíces son:",
        "o": ["1 y 6", "2 y 3", "−2 y −3", "0 y 6"],
        "a": 1,
        "e": "Factorizamos: (x − 2)(x − 3) = 0. Las raíces son 2 y 3.",
    },
    {
        "topic": "Inecuaciones",
        "q": "Resuelve: 2x + 4 > 10",
        "o": ["x > 3", "x < 3", "x > 7", "x < 7"],
        "a": 0,
        "e": "Resta 4: 2x > 6. Divide entre 2: x > 3.",
    },
    {
        "topic": "Inecuaciones",
        "q": "Al multiplicar una desigualdad por un número negativo:",
        "o": [
            "No cambia el signo",
            "Se invierte el signo",
            "Se elimina la variable",
            "Siempre se vuelve igualdad",
        ],
        "a": 1,
        "e": (
            "Al multiplicar o dividir por un número negativo, el sentido de la"
            " desigualdad se invierte."
        ),
    },
    {
        "topic": "Radicales",
        "q": "Simplifica √49",
        "o": ["6", "7", "14", "24"],
        "a": 1,
        "e": "7 × 7 = 49, por eso √49 = 7.",
    },
    {
        "topic": "Radicales",
        "q": "Simplifica √50",
        "o": ["5√2", "2√5", "10√5", "25√2"],
        "a": 0,
        "e": "√50 = √(25·2) = 5√2.",
    },
    {
        "topic": "Funciones básicas",
        "q": "Si f(x) = 2x + 1, calcula f(3)",
        "o": ["5", "6", "7", "8"],
        "a": 2,
        "e": "Sustituye x = 3: f(3) = 2(3) + 1 = 7.",
    },
    {
        "topic": "Funciones básicas",
        "q": "En y = 3x − 2, la pendiente es:",
        "o": ["−2", "2", "3", "−3"],
        "a": 2,
        "e": "En y = mx + b, m es la pendiente. Aquí m = 3.",
    },
]

# Inicialización de variables de estado
if "screen" not in st.session_state:
  st.session_state.screen = "home"
if "player_name" not in st.session_state:
  st.session_state.player_name = "Jugador"
if "score" not in st.session_state:
  st.session_state.score = 0
if "streak" not in st.session_state:
  st.session_state.streak = 0
if "best_streak" not in st.session_state:
  st.session_state.best_streak = 0
if "lives" not in st.session_state:
  st.session_state.lives = 3
if "q_index" not in st.session_state:
  st.session_state.q_index = 0
if "questions" not in st.session_state:
  st.session_state.questions = []
if "answered" not in st.session_state:
  st.session_state.answered = False
if "correct_count" not in st.session_state:
  st.session_state.correct_count = 0
if "ranking" not in st.session_state:
  st.session_state.ranking = []
if "start_time" not in st.session_state:
  st.session_state.start_time = time.time()
if "music_enabled" not in st.session_state:
  st.session_state.music_enabled = True

# Reproductor de música de fondo en la barra lateral
with st.sidebar:
  st.header("🎵 Audio & Ajustes")
  st.session_state.music_enabled = st.checkbox(
      "Música de fondo", value=st.session_state.music_enabled
  )
  if st.session_state.music_enabled:
    # Música libre de derechos (Arcade / Retro Loop)
    audio_url = (
        "https://cdn.pixabay.com/download/audio/2022/03/15/audio_c8c8a73467.mp3"
    )
    st.components.v1.html(
        f"""
        <audio autoplay loop id="bg-music">
            <source src="{audio_url}" type="audio/mpeg">
        </audio>
        <script>
            var audio = document.getElementById("bg-music");
            audio.volume = 0.3; // Volumen moderado
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
  st.session_state.best_streak = 0
  st.session_state.lives = 3
  st.session_state.correct_count = 0
  st.session_state.answered = False
  st.session_state.start_time = time.time()
  st.session_state.screen = "game"


def check_answer(opt_idx, timeout=False):
  if st.session_state.answered:
    return
  st.session_state.answered = True
  q = st.session_state.questions[st.session_state.q_index]

  if timeout:
    st.session_state.lives -= 1
    st.session_state.streak = 0
    st.session_state.last_result = "timeout"
  elif opt_idx == q["a"]:
    st.session_state.correct_count += 1
    st.session_state.streak += 1
    st.session_state.best_streak = max(
        st.session_state.best_streak, st.session_state.streak
    )
    # Bonificación por racha
    st.session_state.score += 100 + (st.session_state.streak * 20)
    st.session_state.last_result = "correct"
  else:
    st.session_state.lives -= 1
    st.session_state.streak = 0
    st.session_state.last_result = "wrong"


def next_question():
  st.session_state.answered = False
  st.session_state.q_index += 1
  if (
      st.session_state.q_index >= len(st.session_state.questions)
      or st.session_state.lives <= 0
  ):
    pct = int(
        (st.session_state.correct_count / len(st.session_state.questions))
        * 100
    )
    st.session_state.ranking.append({
        "name": st.session_state.player_name,
        "score": st.session_state.score,
        "pct": pct,
    })
    st.session_state.ranking = sorted(
        st.session_state.ranking, key=lambda x: x["score"], reverse=True
    )[:10]
    st.session_state.screen = "result"
  else:
    st.session_state.start_time = time.time()


st.title("⚡ ÁLGEBRA BATTLE")
st.caption("Matemática universitaria · Desafío de preguntas")

# PANTALLA INICIAL
if st.session_state.screen == "home":
  st.subheader("🎓⚔️🧮 Desafío Universitario")
  st.write(
      "Resuelve retos de álgebra antes de que se agote el tiempo (15s por"
      " pregunta)."
  )
  player_input = st.text_input(
      "Nombre del jugador:", value=st.session_state.player_name
  )
  if player_input:
    st.session_state.player_name = player_input

  col1, col2 = st.columns(2)
  with col1:
    if st.button("🚀 Iniciar desafío"):
      start_game()
      st.rerun()
  with col2:
    if st.button("🏆 Ver ranking"):
      st.session_state.screen = "ranking"
      st.rerun()

# PANTALLA DE JUEGO
elif st.session_state.screen == "game":
  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Puntos", st.session_state.score)
  c2.metric("Racha 🔥", st.session_state.streak)
  c3.metric(
      "Vidas",
      "❤️" * st.session_state.lives + "🖤" * (3 - st.session_state.lives),
  )
  c4.metric(
      "Progreso",
      f"{st.session_state.q_index + 1}/{len(st.session_state.questions)}",
  )

  # Temporizador (15 segundos)
  TIME_LIMIT = 15
  elapsed_time = time.time() - st.session_state.start_time
  remaining_time = max(0, int(TIME_LIMIT - elapsed_time))

  if not st.session_state.answered:
    progress = remaining_time / TIME_LIMIT
    st.progress(progress, text=f"⏱️ Tiempo restante: {remaining_time}s")

    if remaining_time == 0:
      check_answer(None, timeout=True)
      st.rerun()

  st.divider()
  q = st.session_state.questions[st.session_state.q_index]
  st.caption(f"Categoría: **{q['topic']}**")
  st.markdown(f"### {q['q']}")

  for idx, opt in enumerate(q["o"]):
    label = f"{chr(65 + idx)}) {opt}"
    if st.button(
        label, key=f"opt_{idx}", disabled=st.session_state.answered
    ):
      check_answer(idx)
      st.rerun()

  if st.session_state.answered:
    if st.session_state.last_result == "correct":
      st.success(f"✅ **¡Correcto!**\n\n{q['e']}")
    elif st.session_state.last_result == "timeout":
      st.warning(
          f"⏰ **¡Tiempo agotado!** Respuesta correcta: **{q['o'][q['a']]}**\n\n{q['e']}"
      )
    else:
      st.error(
          f"❌ **Incorrecto.** Respuesta correcta: **{q['o'][q['a']]}**\n\n{q['e']}"
      )

    if st.button("Siguiente pregunta ➜"):
      next_question()
      st.rerun()

# PANTALLA DE RESULTADOS
elif st.session_state.screen == "result":
  st.subheader("🏆 ¡Desafío completado!")
  pct = int(
      (st.session_state.correct_count / len(st.session_state.questions)) * 100
  )
  res_c1, res_c2, res_c3 = st.columns(3)
  res_c1.metric("Puntuación Final", st.session_state.score)
  res_c2.metric("Precisión", f"{pct}%")
  res_c3.metric("Mejor Racha", st.session_state.best_streak)

  btn_col1, btn_col2 = st.columns(2)
  with btn_col1:
    if st.button("🔁 Jugar otra vez"):
      start_game()
      st.rerun()
  with btn_col2:
    if st.button("🏆 Ver ranking"):
      st.session_state.screen = "ranking"
      st.rerun()

# PANTALLA DE RANKING
elif st.session_state.screen == "ranking":
  st.subheader("🏆 Ranking General")
  if st.session_state.ranking:
    st.table(st.session_state.ranking)
  else:
    st.info("Aún no hay puntuaciones registradas.")

  if st.button("Volver al Inicio"):
    st.session_state.screen = "home"
    st.rerun()
