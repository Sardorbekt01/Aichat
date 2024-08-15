MESSAGES = {
    "start": """Assalomu alaykum! 🤖

Men ChatGPT Telegram botman. Sizga turli xil mavzularda yordam bera olaman. Quyidagi imkoniyatlardan foydalanishingiz mumkin:

📝 GPT-4 mini: Har kuni 30 ta bepul so'rov
📝 GPT-4: Har kuni 5 ta bepul so'rov
🖼 Rasm yaratish: Har kuni 2 ta bepul rasm
🎤 Matn oʻrniga ovozli xabarlar yuborishingiz mumkin

Muhim eslatmalar:
Agar bepul limitdan oshsangiz, sizdan obuna bo'lishingiz so'raladi. 

Botdan foydalanish uchun quyidagi komandalarni bosing yoki yozing:
/start - Botni qayta ishga tushirish
/profile - Shaxsiy profil
/rejim - Suhbat rejimini tanlang
/premium - Premium obuna
/help - Foydalanish qo’llanmasi

Yordam kerak bo'lsa yoki savollaringiz bo'lsa, admin bilan bog'laning.""",
    
    "profile": "Profilingiz: 👤\n\n🔍 Bugungi foydalanish limiti:\n\n"
               "GPT-3.5: 30/{gpt4_mini_limit}\n"
               "GPT-4: 5/{gpt4_limit}\n"
               "Rasm yaratish: 2/{image_limit}\n"
               "Ovozli xabarlar: 5/{tts_limit}\n\n"
               "🎟 Obuna turi: {obuna_turi}\n\n"
               "Agar obunangiz Premium bo'lsa, sizda cheksiz foydalanish imkoni mavjud va barcha so'rovlar tezroq amalga oshiriladi. "
               "Premium obuna sizga botning barcha imkoniyatlarini to'liq va reklamasiz foydalanish imkonini beradi: /premium\n\n"
               "Botdan foydalanishda davom eting va kuningizni yanada samarali o'tkazing! 😊",
    
    "rejim": """💬 Suhbat rejimini tanlang:

    ✨ChatGPT-3.5: Tez va samarali javoblar uchun.
    ✨ChatGPT-4: Mukammal va aniq javoblar uchun.
    🏞Rasm yaratish: Tasvirlar yaratish uchun.
    🎤Ovozli xabar: Ovozli xabarlar orqali muloqot qilish uchun.""",

    "rejim1": "Quyidagi rejimlardan birini tanlang:\n\n"
              "1. ChatGPT-4mini\n"
              "2. ChatGPT-4\n"
              "3. Rasm yaratish\n"
              "4. Ovozli xabar",
    "chatgpt_4mini": "ChatGPT-4 mini: Hi, I'm ChatGPT-4 mini. How can I help you?",
    "chatgpt_4": "ChatGPT-4: Hi, I'm ChatGPT-4. How can I assist you?",
    "image": "Rasm yaratish: Siz tasvir yaratish rejimini tanladingiz.",
    "tts": "Ovozli xabar: Siz ovozli xabarlar rejimini tanladingiz.",

"selected_mode": "Tanlangan rejimda davom etishingiz mumkin.",  # Ensure this entry exists


    "premium": """⭐️ Premium obuna

Premium obuna orqali siz quyidagi imkoniyatlarga ega bo'lasiz:

✨ Cheksiz foydalanish: GPT-3.5, GPT-4 va rasm yaratish xizmatlaridan cheksiz foydalanish imkoniyati.
⚡️ Tezkor javoblar: So'rovlaringiz tezroq qayta ishlanadi va natijalar tezroq yetkaziladi.
🔒 Reklamasiz: Reklamalarsiz qulay muloqot.
🗣 Ovozli xabarlar: Ovozli xabarlar orqali ham foydalanish imkoniyati mavjud.""",
    
    "help": """🆘 Foydalanish qo’llanmasi

Quyidagi komandalar orqali botdan foydalanishingiz mumkin:

/start - Botni qayta ishga tushirish
/profile - Shaxsiy profil
/rejim - Suhbat rejimini tanlang
/premium - Premium obuna
/help - Foydalanish qo’llanmasi

🔍 Bugungi foydalanish limiti haqida bilish uchun /profile komandasidan foydalaning.
🎟 Premium obuna haqida ma'lumot olish uchun /premium komandasini bosing.
🔄 Botni qayta ishga tushirish uchun /start komandasini bosing.
💬 Suhbat rejimini tanlash uchun /rejim komandasidan foydalaning.

Qo'shimcha yangiliklar va yangilanishlar haqida bilib olish uchun @AIChatGPTInfo kanaliga obuna bo'ling.
Har qanday savol yoki murojat uchun @DigiTechGPT_support bilan bog'laning.

Botdan foydalanishda davom eting va kuningizni yanada samarali o'tkazing! 😊""",


"admin_start": (
    "Admin panelga xush kelibsiz!\n"
    "Bu yerda siz botni boshqarishingiz, API kalitini o'zgartirishingiz, "
    "statistikani ko'rishingiz va boshqa ko'plab funksiyalarni bajarishingiz mumkin."
),
"api_key_changed": (
    "API kaliti muvaffaqiyatli o'zgartirildi!"
),
"invalid_api_key": (
    "Yangi API kaliti noto'g'ri yoki bo'sh bo'lishi mumkin. Iltimos, tekshirib ko'ring va qayta urinib ko'ring."
),
"view_stats": (
    "Statistika:\n"
    "Foydalanuvchilar soni: {user_count}\n"
    "Bugungi so'rovlar soni: {request_count}\n"
    "Umumiy so'rovlar soni: {total_requests}\n"
),
"set_limits": (
    "Limitlar muvaffaqiyatli o'zgartirildi:\n"
    "GPT-3.5: {gpt4_mini_limit}\n"
    "GPT-4: {gpt4_limit}\n"
    "Image: {image_limit}"
),
"broadcast_success": (
    "Xabar barcha foydalanuvchilarga muvaffaqiyatli yuborildi."
),
"broadcast_error": (
    "Xabar yuborishda xato yuz berdi. Iltimos, tekshirib ko'ring va qayta urinib ko'ring."
),
"admin_profile": (
    "Admin profil ma'lumotlari:\n"
    "ID: {admin_id}\n"
    "Ism: {admin_name}\n"
    "Foydalanuvchi nomi: {admin_username}"
),
"restart_bot": (
    "Bot qayta ishga tushirilyapti...\n"
    "Botni qayta ishga tushirish uchun, administratorlardan xabar kuting."
)


}