import streamlit as st
from google import genai
import time

# --- API AYARI ---
# Yeni bir Gemini Key alırsan buraya yapıştır kral
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = "YENI_GEMINI_KEY_BURAYA"

client = genai.Client(api_key=API_KEY)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Ali Kuşçu AI 1.0", page_icon="ai_logo.png")

st.title("Ali Kuşçu AI 1.0")
st.write("Teknofest 2026 | Ali Kuşçu AİHL")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj Geçmişi
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Sor bakalım..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- ZIRHLI DENEME SİSTEMİ ---
        success = False
        for deneme in range(3): # 3 kere deneyecek
            try:
                with st.spinner("Ali Kuşçu düşüncelerini topluyor..." if deneme == 0 else f"Sistem yoğun, tekrar deneniyor ({deneme}/3)..."):
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", # En stabil model budur
                        config={
                            "system_instruction": "Sen Ali Kuşçu AI'sın. Teknofest ekibindesin. Kısa ve öz cevap ver.",
                        },
                        # Sadece son 3 mesajı gönderiyoruz ki kota bitmesin
                        contents=[m["content"] for m in st.session_state.messages[-3:]]
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    success = True
                    break
            except Exception as e:
                if "429" in str(e):
                    time.sleep(5) # 5 saniye mola verip tekrar deneyecek
                else:
                    st.error(f"Hata: {e}")
                    break
        
        if not success:
            st.warning("⚠️ Google şu an çok yoğun. Kerem çok hızlı yazıyor herhalde! 10 saniye sonra tekrar dene.")

# --- YAN MENÜ ---
with st.sidebar:
    st.subheader("🚀 Ekip")
    st.write("Ömer Furkan İLGÜZ\nKerem ÖZKAN\nAli ORHAN\nSami Yusuf DURAN")
