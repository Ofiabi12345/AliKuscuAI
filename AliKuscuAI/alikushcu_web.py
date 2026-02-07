import streamlit as st
from google import genai
import os
import base64

# --- API AYARI (Secrets Üzerinden) ---
# Streamlit Cloud panelinden Settings -> Secrets kısmına GEMINI_API_KEY eklemeyi unutma!
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except Exception:
    st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol edin.")
    st.stop()

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
default_pc = "data:image/jpeg;base64,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"
default_mobile = "https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg"

bg_url = st.session_state.custom_bg if st.session_state.custom_bg else default_pc
mobile_bg_url = st.session_state.custom_bg if st.session_state.custom_bg else default_mobile

# --- DİNAMİK ARKA PLAN CSS ---
st.markdown(
    f"""
    <style>
    /* Masaüstü */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)), 
                    url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Mobil (Dikey Mod) */
    @media (max-width: 768px) {{
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                        url("{mobile_bg_url}");
            background-size: cover;
            background-position: center;
        }}
    }}
    
    /* Mesaj Kutuları */
    [data-testid="stChatMessage"] {{
        background-color: rgba(20, 20, 20, 0.6) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 10px;
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
        file_bytes = uploaded_file.read()
        encoded_image = base64.b64encode(file_bytes).decode()
        st.session_state.custom_bg = f"data:image/png;base64,{encoded_image}"
        st.success("Yeni tema uygulandı!")
        if st.button("Orijinale Dön"):
            st.session_state.custom_bg = None
            st.rerun()

    st.markdown("---")
    st.subheader("🚀 Teknofest Ekibi")
    st.markdown("""
    * **Ömer Furkan İLGÜZ**
    * **Kerem ÖZKAN**
    * **Ali ORHAN**
    * **Sami Yusuf DURAN**
    """)
    st.markdown("---")
    st.caption("🛠️ Geliştirici: **Ömer Furkan İLGÜZ**")

# --- ANA SOHBET EKRANI ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Yanıt
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
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
                        "Bilge, nazik ve karizmatik bir rehber gibi konuş. "
                        "Cevapların kısa ve öz olsun."
                    )
                },
                contents=prompt
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            if "429" in str(e):
                st.warning("⚠️ Sakin ol şampiyon!30 saniye bekleyip tekrar dene lütfen.")
            elif "403" in str(e):
                st.error("🚫 API Anahtarı sızdırılmış! Lütfen Secrets kısmından yeni bir anahtar tanımlayın.")
            else:
                st.error(f"Bir hata oluştu: {e}")


