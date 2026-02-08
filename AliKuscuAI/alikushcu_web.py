import streamlit as st
from google import genai
import os

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_API_ANAHTARINI_YAZ"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi
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
            # Karmaşık döngü yok, tek atış!
            response = client.models.generate_content(
                model="gemini-1.5-flash", # Daha geniş limitli model
                config={
                    "system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol. Ekip: Ömer, Kerem, Ali, Sami.",
                },
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            if "429" in str(e):
                st.error("🚨 Limit Doldu! Google mola vermemizi istiyor. Lütfen biraz bekleyip tekrar dene kral.")
            else:
                st.error(f"Hata: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
    st.divider()
    st.caption("v1.5 - Güvenli Sürüm")
