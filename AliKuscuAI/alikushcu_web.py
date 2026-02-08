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
            # --- 2. DENEME: HUGGING FACE (Yedek Motor) ---
            try:
                API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.3"
                headers = {"Authorization": f"Bearer {HF_TOKEN}"}
                payload = {"inputs": f"<s>[INST] Ali Kuşçu olarak kısa cevap ver: {prompt} [/INST]", "parameters": {"max_new_tokens": 200}}
                res_hf = requests.post(API_URL, headers=headers, json=payload)
                
                if res_hf.status_code == 200:
                    response_text = res_hf.json()[0]['generated_text']
                    success = True
                else:
                    response_text = "Şu an tüm motorlar sıcak, 10 saniye mola kral!"
            except:
                response_text = "Bağlantı koptu, tekrar dener misin?"

        st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
