import streamlit as st
from google import genai
import os

# --- API AYARI ---
# Eğer Secrets kullanmıyorsan buraya tırnak içinde anahtarını yazabilirsin
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_YENI_ANAHTARINI_YAZ" # Eğer secrets yoksa buraya yapıştır

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

# --- ARKA PLAN (SENİN ÇALIŞAN SİSTEMİN) ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    @media (max-width: 768px) {
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                        url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg");
            background-size: cover;
            background-position: center;
        }
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(20, 20, 20, 0.7) !important;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- ÜST BAŞLIK ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu Anadolu İHL")
st.divider()

# --- SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Size nasıl yardımcı olabilirim?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={"system_instruction": "Sen Ali Kuşçu AI'sın. Ekip: Ömer Furkan, Kerem, Ali, Sami Yusuf. Kısa ve bilge cevaplar ver."},
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Google meşgul, 30 saniye sonra tekrar dene!")
            else:
                st.error(f"Bir hata oluştu: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png", use_container_width=True)
    st.markdown("---")
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• **Ömer Furkan İLGÜZ**")
    st.write("• **Kerem ÖZKAN**")
    st.write("• **Ali ORHAN**")
    st.write("• **Sami Yusuf DURAN**")
    st.markdown("---")
    st.caption("🛠️ Geliştirici: **Ömer Furkan İLGÜZ**")
