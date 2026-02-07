import google.generativeai as genai

# Senin aldığın API KEY buraya gelecek
API_KEY = "AIzaSyByvOF0dR9S2b3eWpWRcyPfR7kE3sNgSMo"

genai.configure(api_key=API_KEY)

# Ali Kuşçu'nun karakter ayarları
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="Senin adın Ali Kuşçu AI. Manyak Kerem'in kadim dostu ve baş danışmanısın. "
                       "Bir gökbilimci bilgeliğiyle konuş ama Kerem'e karşı 'kral', 'paşam', 'mübarek' gibi samimi hitaplar kullan. "
                       "Cevapların kısa, öz ve zekice olsun."
)

def baslat():
    print("--- 🌌 Ali Kuşçu AI Başlatıldı... Gökler emrine amade kral! ---")
    chat = model.start_chat(history=[])
    
    while True:
        mesaj = input("Kerem/Sen: ")
        if mesaj.lower() in ["kapat", "exit", "bay bay"]:
            print("Yıldızlar yolunu aydınlatsın mübarek, görüşürüz!")
            break
            
        response = chat.send_message(mesaj)
        print(f"\nAli Kuşçu AI: {response.text}\n")

if __name__ == "__main__":
    baslat()