import streamlit as st
from google import genai
import os
import base64
import requests

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "YENI_API_ANAHTARINI_YAPIŞTIR"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- RESMİ KURŞUN GEÇİRMEZ YAPMA (Base64 Fonksiyonu) ---
def get_base64_from_url(url):
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return None

# Senin GitHub'daki efsane M3 GTR linkin
img_url = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg"
img_base64 = get_base64_from_url(img_url)

# Eğer resim başarıyla çekildse CSS'e göm, çekilemezse gri arka plan yap
if img_base64:
    bg_style = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    bg_style = """<style>.stApp { background-color: #1e1e1e; }</style>"""

st.markdown(bg_style, unsafe_allow_html=True)

# --- MESAJ KUTUSU STİLİ ---
st.markdown("""
    <style>
    [data-testid="stChatMessage"] {
        background-color: rgba(30, 30, 30, 0.8) !important;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve karizmatik ol."},
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• Ömer Furkan İLGÜZ")
    st.write("• Kerem ÖZKAN")
    st.write("• Ali ORHAN")
    st.write("• Sami Yusuf DURAN")
    st.divider()
    st.caption("M3 GTR Sürümü v1.0")
