import os
import streamlit as st
from google import genai

try:
    client = genai.Client(api_key=st.secrets("GEMINI_API_KEY"))
except Exception:
    client = None

st.set_page_config(page_title="AI - Лінго", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1626; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #0b101d; }
    .stTextArea textarea { background-color: #1b263b !important; color: white !important; border: 1px solid #2c3e50; border-radius: 8px; }
    .stButton>button { width: 100%; background-color: #2563eb !important; color: white !important; font-weight: bold; border-radius: 5px; border: none; height: 45px; }
    .example-box { background-color: #162238; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] { background-color: #1b263b !important; border-radius: 8px; border: 1px solid #2c3e50; }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] * { background-color: transparent !important; color: white !important; }
    
    div.element-container:has(button[key="copy_btn"]) button {
        background-color: #1c2d4a !important;
        color: #a0aec0 !important;
        border: 1px dashed #3b82f6 !important;
        transition: 0.3s;
    }
    div.element-container:has(button[key="copy_btn"]) button:hover {
        color: white !important;
        border-style: solid !important;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🌐 AI - Лінго")
    st.caption("Швидкий • Зручний • Розумний")
    st.write("")
    page = st.radio("Навігація", ["Перекладач", "Історія"], label_visibility="collapsed")

if "history" not in st.session_state:
    st.session_state.history = []

if page == "Історія":
    st.title("Історія")
    if not st.session_state.history:
        st.info("Історія поки порожня. Зробіть свій перший переклад!")
    for item in st.session_state.history:
        st.info(item)

else:
    languages = ["Українська", "Англійська", "Німецька", "Французька", "Іспанська", "Польська"]
    
    col_l1, col_arrow, col_l2 = st.columns(3)
    with col_l1:
        src_lang = st.selectbox("З мови:", languages, index=0)
    with col_arrow:
        st.markdown("<h3 style='text-align: center; margin-top: 25px; color: #a0aec0;'>⇆</h3>", unsafe_allow_html=True)
    with col_l2:
        target_lang = st.selectbox("На мову:", languages, index=1)

    if "txt_in" not in st.session_state: st.session_state.txt_in = ""
    if "txt_out" not in st.session_state: st.session_state.txt_out = ""

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.session_state.txt_in = st.text_area("Ввід", value=st.session_state.txt_in, height=250, label_visibility="collapsed", placeholder="Введіть текст тут...")
    with col_t2:
        st.text_area("Вивід", value=st.session_state.txt_out, height=250, label_visibility="collapsed", disabled=True)
        
        if st.session_state.txt_out:
            st.write("📋 Для копіювання натисніть кнопку нижче:")
            st.code(st.session_state.txt_out, language="")

    st.write("")
    if st.button("🌐 Перекласти"):
        if not st.session_state.txt_in.strip():
            st.warning("Будь ласка, введіть текст для перекладу.")
        elif not client:
            st.error("Критична помилка: Не вдалося знайти ключ магістрального API Gemini. Перевірте змінні оточення.")
        else:
            with st.spinner("AI-Лінго аналізує контекст та створює художній переклад..."):
                try:
                    lang_map = {
                        "Українська": "Ukrainian",
                        "Англійська": "English",
                        "Німецька": "German",
                        "Французька": "French",
                        "Іспанська": "Spanish",
                        "Польська": "Polish"
                    }
                    
                    prompt = f"Translate from {lang_map[src_lang]} to {lang_map[target_lang]}. Return ONLY the translation text without any explanations: {st.session_state.txt_in}"
                    
                    response = client.models.generate_content(
                        model='gemini-3.5-flash-lite',
                        contents=prompt,
                    )
                    st.session_state.txt_out = response.text.strip()
                    
                    record = f"{src_lang} -> {target_lang}: {st.session_state.txt_in} = {st.session_state.txt_out}"
                    st.session_state.history.append(record)
                    
                    st.toast("Готово! Ваш переклад згенерувано. Ви можете скопіювати його у вікні праворуч.")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Упс! Сервери штучного інтелекту зараз перевантажені або недоступні. Спробуйте надіслати текст ще раз через кілька секунд. Код помилки: {e}")

    st.write("")
    st.write("---")
    st.markdown(
        """
        <div class="example-box">
            <strong>📍 Приклад</strong><br>
            <span style='color: #a0aec0;'>UA: Привіт! Як справи?</span><br>
            <span style='color: #a0aec0;'>EN: Hello! How are you?</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
