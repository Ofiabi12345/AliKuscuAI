import streamlit as st
import requests
import time
import os

# Google kütüphanesi kontrolü
try:
    from google import genai
except ImportError:
    st.error("Kütüphane hatası! Lütfen requirements.txt dosyasına 'google-genai' ekle.")

# --- API ANAHTARLARI ---
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="🚀", layout="centered")

# --- ANA EKRAN ---
st.title("🚀 Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | 4NDR0M3DY4 Takımı")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişini Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- SOHBET MOTORU ---
if prompt := st.chat_input("Ali Kuşçu'ya sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        
        # 1. DENEME: GEMINI
        try:
            with st.spinner("Ali Kuşçu düşünüyor..."):
                client = genai.Client(api_key=GEMINI_KEY)
                res = client.models.generate_content(
                    model="gemini-1.5-flash",
                    config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol."},
                    contents=prompt
                )
                full_response = res.text
        except Exception:
            # 2. DENEME: HUGGING FACE (Yedek)
            try:
                with st.spinner("Yedek kütüphaneler taranıyor..."):
                    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.3"
                    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                    payload = {
                        "inputs": f"<s>[INST] Ali Kuşçu olarak kısa cevap ver: {prompt} [/INST]",
                        "parameters": {"max_new_tokens": 250}
                    }
                    res_hf = requests.post(API_URL, headers=headers, json=payload)
                    if res_hf.status_code == 200:
                        full_response = res_hf.json()[0]['generated_text']
                    else:
                        full_response = "Şu an tüm motorlar yoğun, 10 saniye mola kral! 🏁"
            except:
                full_response = "Sistem kilitlendi. API anahtarlarını kontrol etmelisin."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- YAN MENÜ ---
with st.sidebar:
    st.image("https://www.teknofest.org/assets/img/logo.png", width=200)
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.markdown("""
    * **Ömer Furkan İLGÜZ**
    * **Kerem ÖZKAN**
    * **Ali ORHAN**
    * **Sami Yusuf DURAN**
    """)
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
