import streamlit as st
from google import genai
import requests
import time

# --- API ANAHTARLARI (Güvenli şekilde çekiyoruz) ---
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "BURAYA_GEMINI_KEY")
HF_TOKEN = st.secrets.get("HF_TOKEN", "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")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="🚀")
st.title("Ali Kuşçu AI 1.0")
st.caption("Teknofest 2026 | Hibrit Motor Teknolojisi 🛡️")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ali Kuşçu her zaman burada..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = ""
        success = False

        # --- 1. DENEME: GEMINI (Ana Motor) ---
        try:
            client = genai.Client(api_key=GEMINI_KEY)
            res = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
            response_text = res.text
            success = True
        except Exception:
           try:
                with st.spinner("Yedek kütüphaneler taranıyor..."):
                    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.3"
                    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                    payload = {
                        "inputs": f"<s>[INST] Sen Ali Kuşçu AI'sın. Kısa cevap ver: {prompt} [/INST]",
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

# --- YAN MENÜ (EKİP İSİMLERİ BURADA) ---
with st.sidebar:
    st.image("https://www.teknofest.org/assets/img/logo.png", width=200) # Teknofest Logosu
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.markdown("""
    * **Ömer Furkan İLGÜZ**
    * **Kerem ÖZKAN**
    * **Ali ORHAN**
    * **Sami Yusuf DURAN**
    """)
    st.divider()
    st.info("Ali Kuşçu AI, Teknofest 2026 için özel olarak geliştirilmiştir.")
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
