from telethon import Button
from assets.Bot.SearchMovies import convert_movie_time
import random


async def RandomChoiceMovies(event, cursor):
    movies_list = cursor.execute(f"SELECT * FROM movies").fetchall()
    get_match_data = random.choice(movies_list)
    
    file_path = get_match_data[3]
    length = (await convert_movie_time(int(get_match_data[7].replace("دقيقة", "").strip())) if get_match_data[9] is not None else 'غير معروف')
        
    message_to_user = f'''
⇐ **معرف الفيلم :** __{get_match_data[0]}__

⇦ **اسم الفيلم :** __{get_match_data[1].replace('فيلم','').replace('مترجم','').replace('مشاهدة','').strip()}__
⇦ **التصنيف :** __{', '.join(eval(get_match_data[4]))}__
⇦ **التقييم :** __{get_match_data[5]}/10__
⇦ **تاريخ الإصدار :** __{get_match_data[6]}__
⇦ **مدة الفيلم :** __{length}__

⇦ **قصة الفيلم :** __{get_match_data[8]}__

⇐  __لمشاهدة أو تحميل هذا الفيلم, اضغط على زر "🎬 اضغظ للمشاهدة أو التحميل 🎬"__
'''

    buttons = [[Button.inline("🎲 إقترح فيلم آخر", "ChoiceByRandomMovie")], [Button.inline("🎬 اضغظ للمشاهدة أو التحميل 🎬", f"get_movie_{get_match_data[0]}")], [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]]
    
    try:
        await event.reply(f"{message_to_user}", buttons=buttons, file=file_path)
    except:
        await event.reply(f"{message_to_user}", buttons=buttons)


async def RandomChoiceSeries(event, cursor):
    movies_list = cursor.execute(f"SELECT * FROM series").fetchall()
    get_match_data = random.choice(movies_list)
    
    file_path = get_match_data[3]
        
    message_to_user = f'''
⇐ **معرف المسلسل :** __{get_match_data[0]}__

⇦ **اسم المسلسل :** __{get_match_data[1].replace('مسلسل','').replace('مترجم','').replace('مشاهدة','').replace('كامل','').strip()}__
⇦ **التصنيف :** __غير متوفر__
⇦ **التقييم :** __غير متوفر__
⇦ **تاريخ الإصدار :** __{get_match_data[4]}__

⇦ **قصة المسلسل :** __غير متوفرة__

⇐  __لمشاهدة أو تحميل هذا المسلسل, اضغط على زر "🎬 اضغظ للمشاهدة أو التحميل 🎬"__
'''
    
    buttons = [[Button.inline("🎲 إقترح مسلسل آخر", "ChoiceByRandomSerie")], [Button.inline("🎬 اضغظ للمشاهدة أو التحميل 🎬", f"get_serie_{get_match_data[0]}")], [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]]
    
    try:
        await event.reply(f"{message_to_user}", buttons=buttons, file=file_path)
    except:
        await event.reply(f"{message_to_user}", buttons=buttons)
