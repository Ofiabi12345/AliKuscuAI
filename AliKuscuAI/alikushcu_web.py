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

# --- OTURUM HAFIZASI (Özel Arka Plan İçin) ---
if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = None

# --- ARKA PLAN SEÇİCİ MANTIĞI ---
# Eğer kullanıcı resim yüklemediyse senin GitHub'daki orijinal resimlerin kullanılır
default_pc = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg"
default_mobile = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg"

bg_url = st.session_state.custom_bg if st.session_state.custom_bg else default_pc
mobile_bg_url = st.session_state.custom_bg if st.session_state.custom_bg else default_mobile

# --- DİNAMİK ARKA PLAN CSS ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), 
                    url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        image-rendering: -webkit-optimize-contrast;
    }}

    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url("{mobile_bg_url}");
            background-size: cover;
            background-position: center;
        }}
    }}
    
    [data-testid="stChatMessage"] {{
        background-color: rgba(15, 15, 15, 0.6) !important;
        backdrop-filter: blur(8px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- YAN MENÜ (MODİFİYE PANELİ) ---
with st.sidebar:
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png", use_container_width=True)
    
    st.markdown("### 🎨 Görünümü Özelleştir")
    uploaded_file = st.file_uploader("Kendi arka planını yükle", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        import base64
        # Yüklenen resmi CSS'e uygun formata çeviriyoruz
        file_bytes = uploaded_file.read()
        encoded_image = base64.b64encode(file_bytes).decode()
        st.session_state.custom_bg = f"data:image/png;base64,{encoded_image}"
        st.success("Yeni tema uygulandı!")
        if st.button("Orijinale Dön"):
            st.session_state.custom_bg = None
            st.rerun()

    st.markdown("---")
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• **Ömer Furkan**\n• **Kerem**\n• **Ali**\n• **Sami Yusuf**")

# --- ANA SOHBET EKRANI ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge ve nazik ol."},
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata: {e}")

