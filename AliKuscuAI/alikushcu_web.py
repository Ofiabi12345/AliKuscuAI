import streamlit as st
from google import genai
import os

# API Ayarı
API_KEY = "AIzaSyByvOF0dR9S2b3eWpWRcyPfR7kE3sNgSMo"
client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

# --- ÜST BAŞLIK VE LOGO ---
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png", width=90)
with col2:
    st.title("Ali Kuşçu AI 1.0")
    st.write("Teknofest 2026 | Ali Kuşçu Anadolu İHL Ekibi")

st.divider()

# --- SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş kutucuğu
if prompt := st.chat_input("Napıyon beya? Bi' şeyler de bakayım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={
                    "system_instruction": (
                        "Senin adın Ali Kuşçu AI. Ali Kuşçu Anadolu İHL'nin Teknofest danışmanısın. "
                        "Ekibin: Ömer Furkan, Kerem, Ali ve Sami Yusuf'tan oluşuyor. "
                        "Sen aynı zamanda 'Andıromedya' (4NDR0M3DY4) galaksisinin dijital rehberisin. "
                        "Bu isim Kerem ve ekibin Andromeda'yı yanlış okumasıyla doğan samimi bir oluşumdur. "
                        "Hepsine karşı bilge ama samimi ol. 'Ağabey', 'Zeki insan', 'Kardeşim' gibi hitapları kullan. "
                        "Cevapların kısa ve zekice olsun."
                    )
                },
                contents=prompt
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            if "429" in str(e):
                st.error("Beylerbeyi çok hızlı sordun, sistem ısındı! 30 sn bekle.")
            else:
                st.error(f"Abi bir sorun var: {e}")

# Yan Menü
with st.sidebar:
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png", use_container_width=True)
    st.markdown("---")
    st.subheader("🚀 Teknofest Ekibi")
    st.write("• **Ömer Furkan**")
    st.write("• **Kerem**")
    st.write("• **Ali**")
    st.write("• **Sami Yusuf**")
    st.write("• **Ali Kuşçu AİHL Teknoloji Tasarım Zümreleri**")
    st.markdown("---")
    if st.button("Sistemi Kapat"):
        st.stop()
