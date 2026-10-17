from telethon import Button
from assets.Bot.SearchMovies import convert_movie_time
import random


async def Movies_Types(event):
    buttons = [
        [Button.inline("اثارة", "ChoiceType_اثارة"), Button.inline("غموض", "ChoiceType_غموض")],
        [Button.inline("رعب", "ChoiceType_رعب")],
        [Button.inline("دراما", "ChoiceType_دراما"), Button.inline("رومانسي", "ChoiceType_رومانسي")],
        [Button.inline("خيال علمي", "ChoiceType_خيال_علمي"), Button.inline("تاريخي", "ChoiceType_تاريخي")],
        [Button.inline("غربي", "ChoiceType_غربي"), Button.inline("كوميدي", "ChoiceType_كوميدي")],
        [Button.inline("سيرة ذاتية", "ChoiceType_سيرة_ذاتية"), Button.inline("موسيقي", "ChoiceType_موسيقي")],
        [Button.inline("فانتازيا", "ChoiceType_فانتازيا"), Button.inline("حربي", "ChoiceType_حربي")],
        [Button.inline("قصير", "ChoiceType_قصير"), Button.inline("وثائقي", "ChoiceType_وثائقي")],
        [Button.inline("كرتون", "ChoiceType_كرتون"), Button.inline("واقعي", "ChoiceType_واقعي")],
        [Button.inline("مسابقات", "ChoiceType_مسابقات")],
        [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]
    ]
    
    await event.reply("__اختر التصنيف المفضل لك لتحصل على فيلم عشوائي ينتمي لذالك التصنيف__", buttons=buttons)
    
async def Get_Movie_Type(event, cursor, movie_type):
    movies_list = cursor.execute(f"SELECT * FROM movies WHERE GetMSG_ID NOT NULL AND tags LIKE '%{movie_type}%'").fetchall()
    selected_movie = random.choice(movies_list)
    
    tags = ', '.join(eval(selected_movie[7])) if len(eval(selected_movie[7])) != 0 else 'غير معروف'
    length = (await convert_movie_time(int(selected_movie[9].replace("دقيقة", "").strip())) if selected_movie[9] is not None else 'غير معروف')
    rate = (f"{selected_movie[6]}/10" if selected_movie[6] is not None else 'غير معروف')
    released = (selected_movie[8] if selected_movie[8] is not None else 'غير معروف')
    story = (selected_movie[16] if selected_movie[16] is not None else 'غير معروف')
    
    message_to_user = f'''
⇐ **معرف الفيلم :** __{selected_movie[0]}__
    
⇦ **اسم الفيلم :** __{selected_movie[14].strip()}__
⇦ **التصنيف :** __{tags}__    
⇦ **التقييم :** __{rate}__
⇦ **تاريخ الإصدار :** __{released}__

⇦ **مدة الفيلم :** __{length}__
⇦ **جودة فيديو الفيلم :** __720p__
    
⇦ **قصة الفيلم :** __{story}__

⇐  __لمشاهدة أو تحميل هذا الفيلم, اضغط على زر "🎬 اضغظ للمشاهدة أو التحميل 🎬"__
'''

    buttons = [[Button.inline("🎲 إقترح فيلم آخر لنفس التصنيف", f"ChoiceType_{movie_type.replace(' ', '_')}")], [Button.inline("🎬 اضغظ للمشاهدة أو التحميل 🎬", f"get_movie_{selected_movie[0]}")], [Button.inline("الرجوع للتصنيفات ⇐", "ChoiceByType")]]
    
    try:
        file_path = selected_movie[5]
        await event.reply(f"{message_to_user}", buttons=buttons, file=file_path)
    except:
        await Get_Movie_Type(event, cursor, movie_type)
    
    