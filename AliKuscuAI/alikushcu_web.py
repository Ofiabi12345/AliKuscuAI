import streamlit as st
import requests
import time

# --- API AYARI ---
# Paylaştığın anahtarı buraya ekledim kral
HF_TOKEN = "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"

# Mistral-7B modeli ücretsiz dünyadaki en dengeli ve güçlü modellerden biridir
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-v0.3"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Hugging Face Sınırsız Motor 🚀")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi
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
            with st.spinner("Ali Kuşçu bilgisini konuşturuyor..."):
                # Sistem talimatını Mistral formatına uygun hale getirdik
                formatted_prompt = f"<s>[INST] Sen Ali Kuşçu AI'sın. Bilge, nazik ve Teknofest ruhuna uygun bir rehbersin. Ekip: Ömer Furkan, Kerem, Ali, Sami. Soru: {prompt} [/INST]"
                
                payload = {
                    "inputs": formatted_prompt,
                    "parameters": {
                        "max_new_tokens": 500,
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "return_full_text": False
                    }
                }
                
                # İsteği gönder
                response = requests.post(API_URL, headers=headers, json=payload)
                
                # Model uyanmamışsa (503 hatası) otomatik bekleme
                if response.status_code == 503:
                    st.info("⌛ Ali Kuşçu kütüphanesini açıyor (Model yükleniyor)... Lütfen 15 saniye bekle kral.")
                    time.sleep(15)
                    response = requests.post(API_URL, headers=headers, json=payload)

                output = response.json()
                
                # Yanıtı ekrana bas
                if isinstance(output, list) and 'generated_text' in output[0]:
                    res_text = output[0]['generated_text']
                    st.markdown(res_text)
                    st.session_state.messages.append({"role": "assistant", "content": res_text})
                else:
                    st.error("Bir şeyler ters gitti ama limit hatası değil. Tekrar dener misin?")
                    
        except Exception as e:
            st.error(f"Hata: {e}")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
    st.divider()
    st.caption("v2.6 - Sınırsız Mod Aktif")
