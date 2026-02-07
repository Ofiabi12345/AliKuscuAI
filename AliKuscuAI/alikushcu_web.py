import streamlit as st
from google import genai
import time

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyBGCjeBr52B8Ty8MruWZdKzkFvowfGjXXo"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ÖZEL YÜKLEME ANİMASYONU (CSS) ---
st.markdown("""
    <style>
    @keyframes pulse {
        0% { opacity: 0.5; transform: scale(0.95); }
        50% { opacity: 1; transform: scale(1); }
        100% { opacity: 0.5; transform: scale(0.95); }
    }
    .custom-loader {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 20px;
        animation: pulse 1.5s infinite ease-in-out;
    }
    .loader-text {
        color: #ff4b4b;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yapay zeka yanıt üretirken bir yükleme ikonu gösterir
            with st.spinner("Düşünüyorum..."):
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol."},
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            if "429" in str(e):
                # HATA ANINDA GERİ SAYIM BAŞLATAN BÖLÜM
                st.error("⚠️ Limit doldu! Google bizi biraz bekletiyor.")
                timer_place = st.empty() # Geri sayımın görüneceği yer
                for i in range(30, 0, -1):
                    timer_place.info(f"⏳ Lütfen bekleyin... {i} saniye kaldı.")
                    time.sleep(1)
                timer_place.success("✅ Hazırız! Tekrar mesaj gönderebilirsin.")
            else:
                st.error(f"Beklenmedik bir hata: {e}")

# --- YAN MENÜ (EKİP LİSTESİ) ---
with st.sidebar:
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.markdown("""
    * **Ömer Furkan İLGÜZ**
    * **Kerem ÖZKAN**
    * **Ali ORHAN**
    * **Sami Yusuf DURAN**
    """)
    st.divider()
    st.caption("Teknofest 2026 Geliştirme Sürümü")


