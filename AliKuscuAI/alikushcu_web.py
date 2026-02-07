import streamlit as st
from google import genai
import os

# --- API AYARI ---
# Secrets çalışmıyorsa direkt anahtarını buraya yapıştır
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_API_KEY_YAPIŞTIR" 

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

# --- ARKA PLAN (EN BASİT CSS) ---
# Not: Eğer bu linkler hala siyahsa, GitHub'da dosya isimlerini (büyük/küçük harf) kontrol et kral.
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                          url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    @media (max-width: 768px) {
        .stApp {
            background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                              url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg");
        }
    }

    /* Mesaj kutuları */
    [data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
                config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol."},
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    # Logo dosyası varsa göster
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png")
    
    st.markdown("---")
    st.subheader("🚀 Teknofest Ekibi")
    # İsimleri en düz şekilde yazıyoruz hata payı kalmasın
    st.write("• Ömer Furkan İLGÜZ")
    st.write("• Kerem ÖZKAN")
    st.write("• Ali ORHAN")
    st.write("• Sami Yusuf DURAN")
    st.markdown("---")
    st.caption("Geliştirici: Ömer Furkan")
