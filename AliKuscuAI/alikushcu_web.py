import streamlit as st
from google import genai
import time
import os

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "AIzaSyBGCjeBr52B8Ty8MruWZdKzkFvowfGjXXo"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Yaz bakalım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""
        success = False
        
        # --- MODEL DENEME DÖNGÜSÜ ---
        # Önce 2.0'ı, olmazsa 1.5'i deniyoruz
        models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash"]
        
        with st.spinner("Ali Kuşçu yanıtlıyor..."):
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        config={"system_instruction": "Sen Ali Kuşçu AI'sın. Kısa cevap ver."},
                        contents=prompt
                    )
                    response_text = response.text
                    success = True
                    break # Başarılıysa döngüden çık
                except Exception as e:
                    if "429" in str(e):
                        continue # Diğer modele geç
                    else:
                        st.error(f"Hata: {e}")
                        break

        if success:
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            st.warning("⚠️ Google şu an çok yoğun. Lütfen 10 saniye sonra tekrar dener misin?")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 Ekip Üyeleri")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")

