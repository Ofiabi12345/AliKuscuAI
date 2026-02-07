import streamlit as st
from google import genai
import os
import base64

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyBGCjeBr52B8Ty8MruWZdKzkFvowfGjXXo"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ARKA PLAN HAFIZASI ---
if "user_bg" not in st.session_state:
    st.session_state.user_bg = None

# --- DİNAMİK CSS ---
if st.session_state.user_bg:
    bg_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{st.session_state.user_bg}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    </style>
    """
else:
    bg_style = """<style>.stApp { background-color: #1e2124; }</style>"""

st.markdown(bg_style, unsafe_allow_html=True)

# Sohbet Balonları
st.markdown("""
    <style>
    [data-testid="stChatMessage"] { background-color: #2f3136 !important; border-radius: 15px; border: 1px solid #424549; }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ali Kuşçu'ya sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Önce 2.0-flash modelini dener
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol."},
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ **Sistem Meşgul (Hata 429):** Çok fazla soru sorduk. Google şu an bizi dinlendiriyor. Yaklaşık 30 saniye sonra tekrar dene kral, Ali Kuşçu o zaman cevap verecektir.")
            else:
                st.error(f"Hata oluştu: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown("### 🎨 Görünümü Özelleştir")
    uploaded_file = st.file_uploader("Arka plana resim yükle", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        encoded = base64.b64encode(uploaded_file.read()).decode()
        st.session_state.user_bg = f"data:image/png;base64,{encoded}"
        st.rerun()

    if st.session_state.user_bg and st.button("Temayı Sıfırla"):
        st.session_state.user_bg = None
        st.rerun()

    st.markdown("---")
    st.subheader("🚀 Ekip Üyeleri")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")

