import streamlit as st
from groq import Groq
import os
import time

# --- API AYARI ---
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = "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"

client = Groq(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
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
        response_placeholder = st.empty()
        full_response = ""
        
        # --- OTOMATİK YENİDEN DENEME (RETRY) SİSTEMİ ---
        max_retries = 3
        retry_delay = 2 # Saniye
        success = False

        for i in range(max_retries):
            try:
                with st.spinner(f"Düşünüyorum... (Deneme {i+1})" if i > 0 else "Düşünüyorum..."):
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen Ali Kuşçu AI'sın. Bilge ve kısa cevap ver."},
                            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-4:]] # Sadece son 4 mesaj (Kota dostu)
                        ],
                        model="llama3-8b-8192",
                    )
                    full_response = chat_completion.choices[0].message.content
                    success = True
                    break # Başarılıysa döngüden çık
            except Exception as e:
                if "429" in str(e) and i < max_retries - 1:
                    time.sleep(retry_delay) # Biraz bekle ve tekrar dene
                    continue
                else:
                    st.error(f"Sistem şu an çok yoğun. Lütfen birkaç saniye sonra tekrar yaz kral.")
                    break

        if success:
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 Teknofest Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
    st.divider()
    st.caption("v2.1 - Anti-Crash Edition")
