import streamlit as st
from google import genai
import os
import base64

# --- API AYARI ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "BURAYA_ANAHTARINI_YAZ" # Secrets yoksa buraya yaz

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png", layout="centered")

# --- RESMİ BASE64'E ÇEVİREN FONKSİYON (Siyah Ekranı Bitiren Hile) ---
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Eğer resim kodla aynı klasördeyse (GitHub'a beraber yüklediysen) bu çalışır
try:
    # Kendi dosya ismine göre burayı güncelle (Örn: ekip_fotografi.jpg)
    bin_str = get_base64("ekip_fotografi.jpg") 
    bg_image_style = f"url('data:image/jpg;base64,{bin_str}')"
except:
    # Eğer dosya bulunamazsa (hata vermesin diye) senin orijinal linki kullanır
    bg_image_style = "url('https://raw.githubusercontent.com/Ofiabi12345/AliKuscuAI/main/AliKuscuAI/ekip_fotografi.jpg')"

# --- CSS ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), {bg_image_style};
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    [data-testid="stChatMessage"] {{
        background-color: rgba(30, 30, 30, 0.7) !important;
        border-radius: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- ANA EKRAN ---
st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | 4NDR0M3DY4")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Yaz bakalım..."):
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

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 Ekip Üyeleri")
    st.markdown("""
    * **Ömer Furkan İLGÜZ**
    * **Kerem ÖZKAN**
    * **Ali ORHAN**
    * **Sami Yusuf DURAN**
    """)
    st.caption("F5 atınca resmin gitmemesi için resim kodla aynı klasörde olmalıdır.")
