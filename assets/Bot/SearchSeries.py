import json, requests
from telethon import Button
from telethon.tl.types import ReplyInlineMarkup
from telethon.tl.types import KeyboardButtonCallback
from telethon.tl.types import KeyboardButtonUrl
from telethon.tl.types import ReplyKeyboardMarkup
from telethon.tl.types import KeyboardButtonRow
from telethon.tl.types import KeyboardButtonSimpleWebView
from telethon.tl.types import KeyboardButton

# test urls function
async def test_url(url, session):
    get_page = session.get(url)
    if get_page.status_code == 404:
        print (url, "not working")
        return False
    else:
        if "file not found" in str(get_page.content).lower():
            print (url, "not working")
            return False
        else:
            print (url, "working")
            return True

# make shortcut url
async def make_url(url, session):
    #api_url = "https://shrinkearn.com/api?api=3e860a7d30f13a5d727aeba1606e253038c9f11d&url="
    api_url = "https://sh.st/st/603efe038b0d88573c8acd605133a9f5/"+url
    # get_url = session.get(api_url+url)
    # response = json.loads(get_url.text)
    # return response.get("shortenedUrl")
    return api_url
    
# Watch Procces urls
async def Proccess_Watch_series(event, data, serie_id):
    series_urls, rows = json.loads((data[0][6]).replace("'", '"')), []
    
    user_wait, session = await event.reply('__جاري الفحص انتظر قليلا من فضلك...__'), requests.Session()
    for seasons in series_urls:
        for season in series_urls.get(seasons):
            season_rows = []
            for episode in series_urls.get(seasons).get(season):
                for idx, url in enumerate(series_urls.get(seasons).get(season).get(episode).get("watch_urls"), start=1):
                    short_url = await make_url(url.strip(), session)
                    season_rows.append(KeyboardButtonRow(buttons=[KeyboardButtonUrl(text=f"⇐ {season} - {episode} ( سيرفر - {idx} )", url=f'{short_url}')]))
            season_rows.append(KeyboardButtonRow(buttons=[KeyboardButtonCallback(text="❌ أغلق هذه القائمة ❌", data="Delete")]))
            rows.append(season_rows)

    await user_wait.delete()
    for idx, row in enumerate(rows, start=0):
        WatchDashboard = ReplyInlineMarkup(rows=rows[idx])
        try:
            UserWatch = await event.client.send_message(event.chat_id, "__اضغط على أي سيرفر للمشاهدة أو التحميل__", buttons=WatchDashboard)
        except Exception as error:
            if str(error).startswith('The data embedded in the reply markup buttons was too much'):
                error_msg = await event.client.send_message(event.chat_id, "__يبدو أن هذا الموسم كبير جدا لا يمكن ارساله, اذا كنت مهتما بشدة راسل المطور لتوفيره في الخاص @zkada__")
                await event.client.send_message(entity="@zkada", message=f"__user : **{event.chat_id}** find long serie {serie_id}__")
            else:
                error_msg = await event.client.send_message(event.chat_id, "__يبدو أنك اكتشفت خطأ برمجي.. سيتم اصلاحه قريبا, حاليا لا تستطيع الحصول على كل المواسم لهذا المسلسل__")
                await event.client.send_message(entity="@zkada", message=f"__user : **{event.chat_id}** find something wrong {serie_id} -- {error}__")

# set current_index to 1 - series
async def SetCurrentIndexSeries(event, cursor, database, new_index):
    set = cursor.execute(f"UPDATE users SET current_index2 = {new_index} WHERE user_id = {event.chat_id}")
    database.commit()
    
# add match data - series
async def Add_Match_Data_Series(event, match_data, cursor, database, series_cursor):
    
    series_id_list = {
        "results": {},
        "total_result": len(match_data)
    }
    
    for idx, match_movie in enumerate(match_data, start=1):
        series_id_list["results"][f"result_{idx}"] = match_movie[0]
    
    series_id_list = str(series_id_list).replace("'", '"')
    update_data, commit = cursor.execute(f"UPDATE users SET search_data_series = '{series_id_list}' WHERE user_id = {event.chat_id}"), database.commit()
    
    await SendMatchDataToUser(event, cursor, database, "send", series_cursor)

# send match data to user
async def SendMatchDataToUser(event, cursor, database, type, series_cursor):
    
    user_data = cursor.execute(f"SELECT * FROM users WHERE user_id = {event.chat_id}").fetchall()[0]
    results = json.loads(user_data[6])
    match_index = results.get("results").get(f"result_{user_data[5]}")
    total_results = results.get("total_result")
    
    get_match_data = series_cursor.execute(f"SELECT * FROM series WHERE id = {match_index}").fetchall()[0]

    if match_index == None:
        message_to_user, set, delete = "__يبدو أنك استخدمة رسالة قديمة, عد الى القائمة الرئيسية لاصلاح المشكلة..__", await SetCurrentIndexSeries(event, cursor, database, 1), await event.delete()
        buttons, file_path = [[Button.inline("Search Again", "Search_Serie")]], None
    else:
        file_path = get_match_data[3]
        if get_match_data[1] != None:
            serie_title = get_match_data[1].replace('مسلسل','').replace('مترجم','').replace('مشاهدة','').replace('كامل','').strip()
        else:
            serie_title = str(get_match_data[1])
        
        message_to_user = f'''
⇐ **معرف المسلسل :** __{get_match_data[0]}__

⇦ **اسم المسلسل :** __{serie_title}__
⇦ **التصنيف :** __غير متوفر__
⇦ **التقييم :** __غير متوفر__
⇦ **تاريخ الإصدار :** __{get_match_data[4]}__

⇦ **قصة المسلسل :** __غير متوفرة__

⇐  __لمشاهدة أو تحميل هذا المسلسل, اضغط على زر "🎬 اضغظ للمشاهدة أو التحميل 🎬"__
'''
        buttons=[[Button.inline(f"النتائج ({total_results}) : النتيجة {total_results}/{user_data[5]}", f"ResultsButtonSeries_{total_results}_{user_data[5]}")], [Button.inline("التالي", "Series_Next"), Button.inline("السابق", "Series_Back")], [Button.inline("🎬 اضغظ للمشاهدة أو التحميل 🎬", f"get_serie_{match_index}")], [Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]]

    try:
        if type == "send":
            await event.respond(f"{message_to_user}", buttons=buttons, file=file_path)
        elif type == "edit":
            await event.edit(f"{message_to_user}", buttons=buttons, file=file_path)
    except Exception as error:
        if type == "send":
            await event.respond(f"{message_to_user}", buttons=buttons)
        elif type == "edit":
            await event.edit(f"{message_to_user}", buttons=buttons)

# return index
async def which_index(path, current_index, end_index):
    if path == "next":
        if current_index == end_index:
            return ["NO", current_index]
        else:
            return ["", current_index + 1]
    elif path == "back":
        if current_index == 1:
            return ["NO", current_index]
        else:
            return ["", current_index - 1]
    

# add one to next
async def series_next_clicked(event, cursor, database, series_database):
    user_data = cursor.execute(f"SELECT * FROM users WHERE user_id = {event.chat_id}").fetchall()[0]
    current_index, end_index = user_data[5], (json.loads(user_data[6])).get("total_result")
    
    new_index = await which_index("next", current_index, end_index)
    if new_index[0] == "NO":
        await event.answer("No More Pages")
    else:
        await SetCurrentIndexSeries(event, cursor, database, new_index[1]), await SendMatchDataToUser(event, cursor, database, "edit", series_database)
        
        
# add one to back
async def series_back_clicked(event, cursor, database, series_database):
    user_data = cursor.execute(f"SELECT * FROM users WHERE user_id = {event.chat_id}").fetchall()[0]
    current_index, end_index = user_data[5], (json.loads(user_data[6])).get("total_result")
    
    new_index = await which_index("back", current_index, end_index)
    if new_index[0] == "NO":
        await event.answer("No More Pages")
    else:
        await SetCurrentIndexSeries(event, cursor, database, new_index[1]), await SendMatchDataToUser(event, cursor, database, "edit", series_database)


async def convert_movie_time(movie_time_minutes):
    hours = movie_time_minutes // 60
    minutes = movie_time_minutes % 60

    if hours == 1:
        hour_string = "ساعة واحدة"
    elif hours == 2:
        hour_string = "ساعتان"
    elif 2 < hours <= 10:
        hour_string = f"{hours} ساعات"
    else:
        hour_string = f"{hours} ساعة"

    if minutes == 1:
        minute_string = "دقيقة واحدة"
    elif minutes == 2:
        minute_string = "دقيقتان"
    elif 2 < minutes <= 10:
        minute_string = f"{minutes} دقائق"
    else:
        minute_string = f"{minutes} دقيقة"

    movie_time = f"{hour_string} و {minute_string}"
    return movie_time















