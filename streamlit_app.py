import random
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CyberMath: Álgebra Overdrive",
    page_icon="⚔️",
    layout="centered",
)

# Estilos CSS Cyberpunk / Neo-Arcade
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 50% 20%, #150d2a 0%, #07040d 100%);
        font-family: 'Rajdhani', sans-serif;
        color: #00f0ff;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #1f1135 0%, #0f081d 100%);
        color: #00f0ff;
        border: 2px solid #00f0ff;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        transition: all 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        border-color: #ff007f;
        color: #ffffff;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.8);
        transform: scale(1.02);
    }
    
    .stat-card {
        background: rgba(20, 10, 35, 0.8);
        border: 1px solid #7928ca;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 0 15px rgba(121, 40, 202, 0.4);
    }
    
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #ff007f !important;
        text-shadow: 0 0 10px #ff007f;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Módulo de Sonidos Synthetizados Web Audio API
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
        "topic": "Operaciones Reales",
        "q": "Calcula: 18 − 3 × 4 + 2",
        "o": ["8", "14", "68", "2"],
        "a": 0,
        "e": "Prioridad: 3 × 4 = 12 ➔ 18 − 12 + 2 = 8.",
    },
    {
        "topic": "Operaciones Reales",
        "q": "Calcula: (−5)² − 3²",
        "o": ["−16", "16", "34", "−34"],
        "a": 1,
        "e": "(−5)² = 25 y 3² = 9 ➔ 25 − 9 = 16.",
    },
    {
        "topic": "Fracciones & Potencias",
        "q": "Calcula: 1/2 + 3/4",
        "o": ["4/6", "5/4", "7/8", "1/4"],
        "a": 1,
        "e": "Denominador común 4: 2/4 + 3/4 = 5/4.",
    },
    {
        "topic": "Fracciones & Potencias",
        "q": "Simplifica: 2³ × 2²",
        "o": ["2⁵", "2⁶", "4⁵", "2¹"],
        "a": 0,
        "e": "Bases iguales suman exponentes: 3 + 2 = 5.",
    },
    {
        "topic": "Ecuaciones I",
        "q": "Resuelve: 3x + 7 = 22",
        "o": ["x = 3", "x = 5", "x = 7", "x = 9"],
        "a": 1,
        "e": "3x = 15 ➔ x = 5.",
    },
    {
        "topic": "Ecuaciones I",
        "q": "Resuelve: 5(x − 2) = 20",
        "o": ["x = 2", "x = 4", "x = 6", "x = 8"],
        "a": 2,
        "e": "x − 2 = 4 ➔ x = 6.",
    },
    {
        "topic": "Productos Notables",
        "q": "Desarrollo de: (x + 3)²",
        "o": ["x² + 9", "x² + 3x + 9", "x² + 6x + 9", "x² + 6x + 3"],
        "a": 2,
        "e": "Binomio al cuadrado: x² + 2(3)x + 3².",
    },
    {
        "topic": "Productos Notables",
        "q": "Desarrolla: (a − 4)(a + 4)",
        "o": ["a² − 16", "a² + 16", "a² − 8a + 16", "a² + 8a + 16"],
        "a": 0,
        "e": "Diferencia de cuadrados: a² − 16.",
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
        "e": "Números que sumados den 5 y multiplicados 6: (x+2)(x+3).",
    },
    {
        "topic": "Ecuaciones Cuadráticas",
        "q": "En x² − 5x + 6 = 0, las raíces son:",
        "o": ["1 y 6", "2 y 3", "−2 y −3", "0 y 6"],
        "a": 1,
        "e": "Factorización: (x−2)(x−3) = 0 ➔ x = 2, x = 3.",
    },
]

# Estado del sistema
if "screen" not in st.session_state:
  st.session_state.screen = "home"
if "player_name" not in st.session_state:
  st.session_state.player_name = "CyberRunner"
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
if "ranking" not in st.session_state:
  st.session_state.ranking = []

# Power-ups
if "shield" not in st.session_state:
  st.session_state.shield = False
if "time_freeze" not in st.session_state:
  st.session_state.time_freeze = False
if "disabled_options" not in st.session_state:
  st.session_state.disabled_options = []

# Música e integración SFX
components.html(
    f"""
    {SFX_SCRIPT}
    <audio id="bg-music" loop autoplay>
        <source src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3" type="audio/mpeg">
    </audio>
    <script>
        var audio = document.getElementById("bg-music");
        audio.volume = 0.2;
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

  if timeout or opt_idx != q["a"]:
    if st.session_state.shield:
      st.session_state.shield = False
      st.session_state.last_result = "shield_absorbed"
      components.html(
          f"{SFX_SCRIPT}<script>sfxPowerup();</script>", height=0
      )
    else:
      components.html(f"{SFX_SCRIPT}<script>sfxWrong();</script>", height=0)
      st.session_state.player_hp -= 35
      st.session_state.streak = 0
      st.session_state.last_result = "timeout" if timeout else "wrong"
  else:
    components.html(f"{SFX_SCRIPT}<script>sfxCorrect();</script>", height=0)
    st.session_state.streak += 1
    damage = 10 + (st.session_state.streak * 5)
    st.session_state.boss_hp = max(0, st.session_state.boss_hp - damage)
    st.session_state.score += 150 + (st.session_state.streak * 30)
    st.session_state.last_result = "correct"


def next_question():
  st.session_state.answered = False
  st.session_state.time_freeze = False
  st.session_state.disabled_options = []
  st.session_state.q_index += 1

  if (
      st.session_state.q_index >= len(st.session_state.questions)
      or st.session_state.player_hp <= 0
      or st.session_state.boss_hp <= 0
  ):
    st.session_state.ranking.append({
        "name": st.session_state.player_name,
        "score": st.session_state.score,
        "victory": st.session_state.boss_hp <= 0,
    })
    st.session_state.ranking = sorted(
        st.session_state.ranking, key=lambda x: x["score"], reverse=True
    )[:10]
    st.session_state.screen = "result"
  else:
    st.session_state.start_time = time.time()


st.title("⚔️ CYBERMATH: OVERDRIVE")
st.caption("Sistema de Inteligencia Matemática · Modo Combate")

# INICIO
if st.session_state.screen == "home":
  st.subheader("🤖 DESAFÍO CONTRA EL NÚCLEO")
  st.write("Derrota al Boss del sistema resolviendo ecuaciones complejas.")
  st.session_state.player_name = st.text_input(
      "Identificador de Usuario:", value=st.session_state.player_name
  )

  c1, c2 = st.columns(2)
  with c1:
    if st.button("🚀 INICIAR COMBATE"):
      start_game()
      st.rerun()
  with c2:
    if st.button("🏆 TABLA DE HONORES"):
      st.session_state.screen = "ranking"
      st.rerun()

# JUEGO
elif st.session_state.screen == "game":
  # Barra de estado de Combate
  col_hp1, col_hp2 = st.columns(2)
  with col_hp1:
    st.write(f"💙 **Jugador HP:** {st.session_state.player_hp}%")
    st.progress(max(0, st.session_state.player_hp) / 100)
  with col_hp2:
    st.write(f"👾 **Boss HP:** {st.session_state.boss_hp}%")
    st.progress(max(0, st.session_state.boss_hp) / 100)

  m1, m2, m3 = st.columns(3)
  m1.metric("Puntuación", st.session_state.score)
  m2.metric("Multiplicador", f"x{st.session_state.streak + 1}")
  m3.metric("Protección", "🛡️ ACTIVA" if st.session_state.shield else "NINGUNA")

  # Habilidades / Power-Ups
  st.write("---")
  p1, p2, p3 = st.columns(3)
  if p1.button(
      "🛡️ Escudo",
      disabled=st.session_state.shield or st.session_state.answered,
  ):
    apply_powerup("shield")
    st.rerun()
  if p2.button(
      "⚡ Congelar",
      disabled=st.session_state.time_freeze or st.session_state.answered,
  ):
    apply_powerup("freeze")
    st.rerun()
  if p3.button(
      "💣 50/50",
      disabled=len(st.session_state.disabled_options) > 0
      or st.session_state.answered,
  ):
    apply_powerup("bomb")
    st.rerun()

  # Temporizador
  TIME_LIMIT = 15
  if not st.session_state.answered and not st.session_state.time_freeze:
    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, int(TIME_LIMIT - elapsed))
    st.progress(remaining / TIME_LIMIT, text=f"⏱️ Tiempo: {remaining}s")
    if remaining == 0:
      check_answer(None, timeout=True)
      st.rerun()
  elif st.session_state.time_freeze and not st.session_state.answered:
    st.info("⚡ ¡TIEMPO CONGELADO EN ESTA PREGUNTA!")

  st.divider()
  q = st.session_state.questions[st.session_state.q_index]
  st.caption(f"Módulo: **{q['topic']}**")
  st.markdown(f"### {q['q']}")

  # Botones de Opciones
  for idx, opt in enumerate(q["o"]):
    if idx in st.session_state.disabled_options:
      st.button(f"🚫 {opt}", key=f"opt_{idx}", disabled=True)
    else:
      if st.button(
          f"{chr(65+idx)}) {opt}",
          key=f"opt_{idx}",
          disabled=st.session_state.answered,
      ):
        check_answer(idx)
        st.rerun()

  if st.session_state.answered:
    if st.session_state.last_result == "correct":
      st.success(f"💥 **¡Impacto Directo!**\n\n{q['e']}")
    elif st.session_state.last_result == "shield_absorbed":
      st.info(f"🛡️ **¡Escudo Absorbió el Golpe!**\n\n{q['e']}")
    else:
      st.error(
          f"⚡ **¡Ataque Recibido!** Respuesta correcta: **{q['o'][q['a']]}**\n\n{q['e']}"
      )

    if st.button("Siguiente Ronda ➔"):
      next_question()
      st.rerun()

# RESULTADO
elif st.session_state.screen == "result":
  if st.session_state.boss_hp <= 0:
    st.balloons()
    st.title("🎉 ¡SISTEMA PURGADO! (VICTORIA)")
  else:
    st.title("💀 ¡INFILTRACIÓN FALLIDA! (GAME OVER)")

  r1, r2 = st.columns(2)
  r1.metric("Puntuación Final", st.session_state.score)
  r2.metric("Salud del Boss Restante", f"{st.session_state.boss_hp}%")

  c1, c2 = st.columns(2)
  if c1.button("🔁 Reiniciar Sistema"):
    start_game()
    st.rerun()
  if c2.button("🏆 Ver Salón de la Fama"):
    st.session_state.screen = "ranking"
    st.rerun()

# RANKING
elif st.session_state.screen == "ranking":
  st.subheader("🏆 SALÓN DE LA FAMA")
  if st.session_state.ranking:
    st.table(st.session_state.ranking)
  else:
    st.info("Sin registros en la base de datos.")

  if st.button("Volver a la Base"):
    st.session_state.screen = "home"
    st.rerun()
