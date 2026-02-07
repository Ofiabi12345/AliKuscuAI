import streamlit as st
from google import genai
import os
import base64

# --- API AYARI (Secrets Üzerinden) ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    # Test için anahtar yoksa uyarı ver ama site çökmesin
    API_KEY = None

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

# --- ARKA PLAN LİNKLERİ (RAW FORMAT) ---
# GitHub linklerinde 'blob' yerine 'raw' kullandığından emin olmalısın.
default_pc = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg"
default_mobile = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg"

if "custom_bg" not in st.session_state:
    st.session_state.custom_bg = None

# Hangi resim görünecek?
bg_image = st.session_state.custom_bg if st.session_state.custom_bg else default_pc
mobile_bg = st.session_state.custom_bg if st.session_state.custom_bg else default_mobile

# --- CSS (Siyah ekranı bitiren versiyon) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{bg_image}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}

    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), url("{mobile_bg}");
            background-size: cover !important;
            background-position: center !important;
        }}
    }}

    /* Mesaj kutularını daha belirgin yapalım */
    [data-testid="stChatMessage"] {{
        background-color: rgba(25, 25, 25, 0.75) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ ---
with st.sidebar:
    st.markdown("### 🎨 Görünümü Özelleştir")
    uploaded_file = st.file_uploader("Kendi arka planını yükle", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        encoded_image = base64.b64encode(uploaded_file.read()).decode()
        st.session_state.custom_bg = f"data:image/png;base64,{encoded_image}"
        st.rerun()

    if st.button("Orijinale Dön"):
        st.session_state.custom_bg = None
        st.rerun()

    st.markdown("---")
    st.subheader("🚀 Teknofest Ekibi")
    st.markdown("* **Ömer Furkan İLGÜZ**\n* **Kerem ÖZKAN**\n* **Ali ORHAN**\n* **Sami Yusuf DURAN**")

# --- ANA EKRAN ---
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
        if API_KEY:
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config={"system_instruction": "Sen Ali Kuşçu AI'sın. Bilge, nazik ve kısa cevaplar ver."},
                    contents=prompt
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hata: {e}")
        else:
            st.info("Ali Kuşçu şu an çevrimdışı (Secrets ayarını kontrol et!).")
