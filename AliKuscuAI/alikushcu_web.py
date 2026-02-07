import streamlit as st
from google import genai
import time

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_API_ANAHTARINI_YAZ"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ARKA PLANI KALDIRDIK (SADE VE STABİL TEMA) ---
st.markdown("""
    <style>
    /* Sade ve modern bir görünüm için mesaj kutularını hafif belirginleştirdik */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Ali Kuşçu'ya sor..."):
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
            if "429" in str(e):
                # --- 30 SANİYE GERİ SAYIM BAŞLIYOR ---
                st.warning("⚠️ **Sistem Meşgul!** Google limitlerine takıldık.")
                placeholder = st.empty() # Geri sayım için boş alan
                for i in range(30, 0, -1):
                    placeholder.info(f"⏳ Lütfen bekleyin... Sistem {i} saniye içinde hazır olacak.")
                    time.sleep(1)
                placeholder.success("✅ Süre doldu! Şimdi tekrar mesaj gönderebilirsin.")
            else:
                st.error(f"Bir hata oluştu: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 Ekip Üyeleri")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
    st.divider()
    st.caption("v1.2 - Geri Sayım Özelliği Eklendi")
