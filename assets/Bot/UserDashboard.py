from telethon import Button
import asyncio


# USER DASHBOARD
async def UserDashboard(event):
    owner_id = 978571497

    # USER KEYBOARD
    UserDashboard = [
        [Button.inline(" 🎲 إقتراح بالتصنيف 🎲 ", "ChoiceByType"), Button.inline(" 🎲 إقتراح عشوائي 🎲 ", "ChoiceByRandom")],
        [Button.inline("🔍 ابحث عن فيلم 🔎", "Search_Movie")],
        [Button.inline("🔍 ابحث عن مسلسل 🔎", "Search_Serie")],
        [Button.inline("📊 إحصائيات قاعدة البيانات 📊", "statistics")],
        [Button.inline("🇲🇦  Made in Morooco  🇲🇦", "Made")]
    ]

    if event.chat_id == owner_id:
        UserDashboard.append([Button.inline("📡 Braodcast", "braodcast")])
        UserDashboard.append([Button.inline("🎥 Upload Video", "upload_video")])


    MESSAGE = f'''❕ __هذا البوت يساعدك بإقتراح عليك أفضل الأفلام و المسلسلات الأجنبية مع إمكانية مشاهدتها أو تحميلها من خلال هذا البوت.__


🎲  __**إضغط - إقتراح عشوائي :**__
__ستحصل على إقتراح عشوائي لمسلسل أو فيلم__

🎲  __**إضغط - إقتراح بالتصنيف :**__
__ستحصل على قائمة بالتصنيفات، إضغط على التصنيف المفضل لك لتحصل على إقتراح ينتمي للتصنيف__'''

    Dashboard = await event.client.send_message(event.chat_id, MESSAGE, buttons=UserDashboard)
    
async def UserDashboard_ChoiceByRandom(event):
    ChoiceByRandomKeyborad = [
        [Button.inline(" 🎲 إقتراح عشوائي لفيلم 🎲 ", "ChoiceByRandomMovie")],
        [Button.inline(" 🎲 إقتراح عشوائي لمسلسل 🎲 ", "ChoiceByRandomSerie")],
        [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]
    ]
    
    MESSAGE = f'''
🎲  __**إضغط -  إقتراح عشوائي لفيلم :**__
__ستحصل على إقتراح عشوائي لفيلم__

🎲  __**إضغط -  إقتراح عشوائي لمسلسل :**__
__ستحصل على إقتراح عشوائي لمسلسل__'''
    
    Dashboard = await event.client.send_message(event.chat_id, MESSAGE, buttons=ChoiceByRandomKeyborad)
    
    
async def UserDashboard_ChoiceType(event):
    ChoiceByRandomKeyborad = [
        [Button.inline(" 🎲 إقتراح بالتصنيف لفيلم 🎲 ", "ChoiceByTypeMovie")],
        [Button.inline(" 🎲 إقتراح بالتصنيف لمسلسل 🎲 ", "ChoiceByTypeSerie")],
        [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]
    ]
    
    MESSAGE = f'''
🎲  __**إضغط -  إقتراح بالتصنيف لفيلم :**__
__ستحصل على قائمة تصنيفات الافلام__

🎲  __**إضغط -  إقتراح بالتصنيف لمسلسل :**__
__ستحصل على قائمة تصنيفات المسلسلات__'''
    
    Dashboard = await event.client.send_message(event.chat_id, MESSAGE, buttons=ChoiceByRandomKeyborad)
    
    
    
    
    
    
    
    
    
    
    
    
    
    