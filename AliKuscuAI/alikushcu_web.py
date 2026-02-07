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

# --- DUYARLI (RESPONSIVE) ARKA PLAN ---
st.markdown(
    """
    <style>
    /* 1. MASAÜSTÜ: Bilgisayar ve Tablet (Yatay) */
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* 2. MOBİL: Telefonlar (Dikey - _mobil ekiyle biten dosya) */
    @media (max-width: 768px) {
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url("https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi_mobil.jpg");
            background-size: cover;
            background-position: center;
        }
    }
    
    /* Okunabilirlik için hafif bir karanlık perde */
    [data-testid="stChatMessage"] {
        background-color: rgba(30, 30, 30, 0.5) !important;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
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
if prompt := st.chat_input("Size nasıl yardımcı olabilirim? (Sistem 30 saniye içinde hazır olur)"):
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
                        "Hocalara karşı nazik ve bilge, ekip üyelerine karşı samimi ve seviyeli ol. "
                        "Cevapların kısa, vurucu ve zekice olsun."
                    )
                },
                contents=prompt
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            if "429" in str(e):
                st.error("Şu an yoğunluk nedeniyle yanıt veremiyorum, lütfen kısa bir süre sonra tekrar deneyiniz.")
            else:
                st.error(f"Sistemde bir güncelleme yapılıyor: {e}")

# Yan Menü
with st.sidebar:
    if os.path.exists("ai_logo.png"):
        st.image("ai_logo.png", use_container_width=True)
    st.markdown("---")
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• **Ömer Furkan İLGÜZ**")
    st.write("• **Kerem ÖZKAN**")
    st.write("• **Ali ORHAN**")
    st.write("• **Sami Yusuf DURAN**")
    st.markdown("---")
    st.caption("🛠️ **Ömer Furkan İLGÜZ** tarafından geliştirildi.")
    if st.button("Yanımdan Ayrıl"):
        st.info("Ali Kuşçu galaksisine geri döndü. Tekrar görüşmek üzere!")
        st.stop()
