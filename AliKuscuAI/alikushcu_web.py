import streamlit as st
from google import genai
import os
import base64

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except:
    # Eğer secrets yoksa hata vermesin, sadece bot çalışmaz
    API_KEY = "YOK"

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = None

# --- ARKA PLAN LİNKLERİ ---
# Buradaki linkleri tarayıcıda açtığında resmi gördüğünden emin ol kral
default_pc = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg"
default_mobile = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg"

# Hangi resmi kullanacağımızı seçiyoruz
main_bg = st.session_state.custom_bg if st.session_state.custom_bg else default_pc
mobile_bg = st.session_state.custom_bg if st.session_state.custom_bg else default_mobile

# --- CSS (GARANTİ YÖNTEM) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{main_bg}");
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{mobile_bg}");
            background-size: cover !important;
            background-position: center !important;
        }}
    }}

    /* Sohbet Balonları Görünürlüğü */
    [data-testid="stChatMessage"] {{
        background-color: rgba(30, 30, 30, 0.7) !important;
        backdrop-filter: blur(5px);
        border-radius: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ ---
with st.sidebar:
    st.title("🎨 Modifiye")
    uploaded_file = st.file_uploader("Arka planı değiştir", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        encoded = base64.b64encode(uploaded_file.read()).decode()
        st.session_state.custom_bg = f"data:image/png;base64,{encoded}"
        st.rerun()
    
    if st.button("Orijinale Dön"):
        st.session_state.custom_bg = None
        st.rerun()

    st.divider()
    st.subheader("🚀 Teknofest Ekibi")
    st.write("• Ömer Furkan İLGÜZ\n• Kerem ÖZKAN\n• Ali ORHAN\n• Sami Yusuf DURAN")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | 4NDR0M3DY4")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Yaz bakalım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Bot cevabı (Basitleştirilmiş deneme)
    with st.chat_message("assistant"):
        if API_KEY != "YOK":
            try:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Limit doldu veya bir hata oluştu.")
        else:
            st.info("Ali Kuşçu şu an çevrimdışı (API Key yok).")
