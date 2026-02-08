import streamlit as st
import requests
import time

# --- API AYARI ---
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png")

st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Sınırsız Mod")

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
            with st.spinner("Düşünüyorum..."):
                formatted_prompt = f"<s>[INST] Sen Ali Kuşçu AI'sın. Kısa cevap ver. Soru: {prompt} [/INST]"
                payload = {"inputs": formatted_prompt, "parameters": {"max_new_tokens": 500, "return_full_text": False}}
                
                response = requests.post(API_URL, headers=headers, json=payload)
                
                # Model uyanıyorsa 503 verir, bekleyelim
                if response.status_code == 503:
                    st.warning("⌛ Ali Kuşçu kütüphanesini açıyor, 10 saniye bekle kral...")
                    time.sleep(10)
                    response = requests.post(API_URL, headers=headers, json=payload)

                output = response.json()
                
                # Yanıtın içindeki metni güvenli bir şekilde çekelim
                if isinstance(output, list) and len(output) > 0:
                    res_text = output[0].get('generated_text', "Cevap üretilemedi.")
                elif isinstance(output, dict) and 'generated_text' in output:
                    res_text = output['generated_text']
                else:
                    res_text = "Şu an cevap veremiyorum, lütfen tekrar dene."

                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})

        except Exception as e:
            st.error(f"Sistemde küçük bir sorun var: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
