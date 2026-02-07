import streamlit as st
from google import genai
import os
import base64

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_API_ANAHTARINI_YAZ"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Ali Kuşçu AI 1.0", 
    page_icon="ai_logo.png", 
    layout="centered"
)

# --- ARKA PLAN HAFIZASI ---
if "user_bg" not in st.session_state:
    st.session_state.user_bg = None

# --- DİNAMİK CSS ---
if st.session_state.user_bg:
    # Kullanıcı resim yüklediyse onu kullan
    bg_style = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{st.session_state.user_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    # Resim yoksa o karizmatik Gri temayı kullan
    bg_style = """
    <style>
    .stApp {
        background-color: #1e2124;
    }
    </style>
    """

st.markdown(bg_style, unsafe_allow_html=True)

# Mesaj Kutuları Stili
st.markdown("""
    <style>
    [data-testid="stChatMessage"] {
        background-color: rgba(47, 49, 54, 0.8) !important;
        border-radius: 15px;
        border: 1px solid #424549;
    }
    </style>
    """, unsafe_allow_html=True)

# --- YAN MENÜ (MODİFİYE PANELİ) ---
with st.sidebar:
    st.markdown("### 🎨 Görünümü Özelleştir")
    uploaded_file = st.file_uploader("Arka plana kendi resmini koy!", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Yüklenen resmi Base64'e çevirip hafızaya alıyoruz
        encoded = base64.b64encode(uploaded_file.read()).decode()
        st.session_state.user_bg = f"data:image/png;base64,{encoded}"
        st.success("Yeni tema uygulandı!")
        if st.button("Temayı Sıfırla"):
            st.session_state.user_bg = None
            st.rerun()

    st.markdown("---")
    st.subheader("🚀 4NDR0M3DY4 Ekibi")
    st.write("• **Ömer Furkan İLGÜZ**")
    st.write("• **Kerem ÖZKAN**")
    st.write("• **Ali ORHAN**")
    st.write("• **Sami Yusuf DURAN**")

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ali Kuşçu'ya sor..."):
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
