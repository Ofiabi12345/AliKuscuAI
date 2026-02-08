import streamlit as st
from groq import Groq
import os

# --- API AYARI (Groq) ---
# Paylaştığın anahtarı buraya güvenli bir şekilde bağlıyoruz
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # Eğer secrets'a eklemediysen şimdilik direkt buraya da yazabilirsin
    API_KEY = "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"

client = Groq(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Groq Llama-3 Motoruyla Işık Hızında ⚡")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı Girişi
if prompt := st.chat_input("Ali Kuşçu'ya sor (Işık Hızında)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Groq'un en iyi modellerinden biri olan Llama-3-70b veya 8b kullanabiliriz
            # 8b-instant inanılmaz hızlıdır
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen Ali Kuşçu AI'sın. Bilge, nazik ve öz konuşan bir rehber ol. Ekip: Ömer Furkan, Kerem, Ali, Sami."
                    },
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
                ],
                model="llama3-8b-8192",
            )
            
            response_text = chat_completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Groq Motoru Hatası: {e}")
            if "rate_limit_exceeded" in str(e).lower():
                st.warning("⚠️ Groq bile yoruldu kral, bir 10 saniye bekle motor soğusun.")

# --- YAN MENÜ ---
with st.sidebar:
    # Logo varsa göster
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png")
    
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")
    st.divider()
    st.caption("v2.0 - Groq Ultra Fast Edition")
