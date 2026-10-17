from telethon import TelegramClient, events, types, Button
from datetime import datetime, timedelta
from rapidfuzz import fuzz

try:
    from backports.zoneinfo import ZoneInfo
except:
    from zoneinfo import ZoneInfo

import asyncio
import re
import sqlite3
import uuid
import json


# READ CONFIGS
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


API_ID = 1724716
API_HASH = "00b2d8f59c12c1b9a4bc63b70b461b2f"
BOT_TOKEN = config["TEST_BOT_TOKEN"] # config["BOT_TOKEN"]


OWNER_ID = 978571497
BOT_USERNAME = None
SEARCH_BTN = [Button.switch_inline("🔎 ابحث عن فيلم أو مسلسل", query="", same_peer=True, style="primary")]
RANDOM_SEARCH = [
    Button.switch_inline("🎬 اقترح لي فيلمًا", query="random_movie", same_peer=True, style="primary"),
    Button.switch_inline("📺 اقترح لي مسلسلًا", query="random_serie", same_peer=True, style="primary")
]


# =========================
# DATABASE
# =========================

database = sqlite3.connect(
    "databases/database.db",
    check_same_thread=False
)

cursor = database.cursor()


# =========================
# BOT
# =========================

bot = TelegramClient(
    "test_bot",
    API_ID,
    API_HASH
).start(
    bot_token=BOT_TOKEN
)


# =========================
# CODING
# =========================





def search_movies(db, cursor, query):
    def normalize(text):
        return re.sub(r"[^\w]", " ", text.casefold()).strip()

    normalized_query = normalize(query)
    compact_query = normalized_query.replace(" ", "")

    if not compact_query:
        return []

    movies = cursor.execute("""
        SELECT id, title, poster, release_date, story, 'فيلم' AS type
        FROM movies
        UNION ALL
        SELECT id, title, poster, release_date, story, 'مسلسل' AS type
        FROM series
    """).fetchall()

    results = []

    for movie in movies:
        title = normalize(movie[1])
        compact_title = title.replace(" ", "")

        score = max(
            fuzz.WRatio(normalized_query, title),
            fuzz.WRatio(compact_query, compact_title),
            fuzz.token_sort_ratio(normalized_query, title)
        )

        if compact_query == compact_title:
            score = 100

        if score >= 45:
            results.append((score, movie))

    results.sort(key=lambda x: x[0], reverse=True)
    return [movie for score, movie in results[:50]]


# BROADCAST
@bot.on(events.CallbackQuery(data='braodcast'))
async def Broadcast(event):

    SENT, FAIL = 0, 0
    cursor.execute(f"SELECT id FROM bot_users")
    bot_users = cursor.fetchall()
    try:
        async with bot.conversation(entity=event.chat_id, timeout=180) as conv:
            await conv.send_message("__📢 أرسل الرسالة التي تريد تعميمها على جميع المستخدمين:__")
            the_message = await conv.get_response()

        await event.respond("__⏳ جارٍ إرسال الرسالة إلى جميع المستخدمين، يرجى الانتظار...__")
        for user_id, in bot_users:
            try:
                await bot.send_message(user_id, message=the_message)
                SENT += 1
            except:FAIL += 1

        await event.respond(f'''
✅ **اكتمل الإرسال**
__
📨 الرسائل المرسلة: {SENT}
❌ الرسائل الفاشلة: {FAIL}
📊 نسبة النجاح: {SENT / len(bot_users) * 100:.2f}%

👥 إجمالي المستخدمين: {len(bot_users)}
__''', buttons=[[Button.inline("القائمة الرئيسية »", data="show_menu")]])
    
    except Exception as error:print(error)


def add_stat(name, increase_by=1):
    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO bot_stats (name, date, count)
        VALUES (?, ?, ?)
        ON CONFLICT(name, date)
        DO UPDATE SET count = count + excluded.count
    """, (name, today, increase_by))

    database.commit()


# STATISTICS
@bot.on(events.CallbackQuery(data='statistics'))
async def Statistics(event):

    # Total users
    total_users = cursor.execute(
        "SELECT COUNT(*) FROM bot_users"
    ).fetchone()[0]

    # Users who joined this month
    this_month = cursor.execute("""
        SELECT COUNT(*) FROM bot_users
        WHERE strftime('%Y-%m', substr(created_at, 7, 4) || '-' ||
            substr(created_at, 4, 2) || '-' || substr(created_at, 1, 2))
        = strftime('%Y-%m', 'now')
    """).fetchone()[0]

    # Users who joined last month
    last_month = cursor.execute("""
        SELECT COUNT(*) FROM bot_users
        WHERE strftime('%Y-%m', substr(created_at, 7, 4) || '-' ||
            substr(created_at, 4, 2) || '-' || substr(created_at, 1, 2))
        = strftime('%Y-%m', 'now', '-1 month')
    """).fetchone()[0]

    # Users joined each day of this month
    daily_users = cursor.execute("""
        SELECT substr(created_at, 1, 10) AS join_date,
            COUNT(*) AS total
        FROM bot_users
        WHERE substr(created_at, 7, 4) = strftime('%Y', 'now')
        AND substr(created_at, 4, 2) = strftime('%m', 'now')
        GROUP BY substr(created_at, 1, 10)
        ORDER BY substr(created_at, 1, 10)
    """).fetchall()

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT name, count
        FROM bot_stats
        WHERE date = ?
    """, (today,))

    stats = dict(cursor.fetchall())

    total_searches = stats.get("total_searches", 0)
    movie_suggestions = stats.get("movie_suggestions", 0)
    series_suggestions = stats.get("series_suggestions", 0)

    movie_requests = stats.get("movie_requests", 0)
    series_requests = stats.get("series_requests", 0)
    
    movie_servers_views = stats.get("movie_servers_views", 0)
    series_seasons_views = stats.get("series_seasons_views", 0)
    series_episodes_views = stats.get("series_episodes_views", 0)
    series_episode_servers_views = stats.get("series_episode_servers_views", 0)

    message = f"""
📊 **إحصائيات التفاعل**
__
↢ إجمالي عمليات البحث: `{total_searches}`
↢ اقتراحات الأفلام: `{movie_suggestions}`
↢ اقتراحات المسلسلات: `{series_suggestions}`

↢ طلبات مشاهدة الأفلام: `{movie_requests}`
↢ طلبات مشاهدة المسلسلات: `{series_requests}`

↢ عرض سيرفرات الأفلام: `{movie_servers_views}`
↢ عرض مواسم المسلسلات: `{series_seasons_views}`
↢ عرض حلقات المسلسلات: `{series_episodes_views}`
↢ عرض سيرفرات حلقات المسلسلات: `{series_episode_servers_views}`
__
---------------------------------------

📊 **إحصائيات المستخدمين**
__
↢ إجمالي المستخدمين: `{total_users}`
↢ مستخدمو الشهر الماضي: `{last_month}`
↢ مستخدمو هذا الشهر: `{this_month}`
__
📈 **المستخدمون الجدد اليومي هذا الشهر:**

{chr(10).join(f"↣ {day}: `{count}`" for day, count in daily_users)}
"""

    await event.respond(
        message,
        buttons=[[Button.inline("القائمة الرئيسية »", data="show_menu")]])


async def daily_stats_report():
    TZ = ZoneInfo("Africa/Casablanca")

    STAT_LABELS = {
        "total_searches": "↢ إجمالي عمليات البحث",
        "movie_suggestions": "↢ اقتراحات الأفلام",
        "series_suggestions": "↢ اقتراحات المسلسلات",
        "movie_requests": "↢ طلبات مشاهدة الأفلام",
        "series_requests": "↢ طلبات مشاهدة المسلسلات",
        "movie_servers_views": "↢ عرض سيرفرات الأفلام",
        "series_seasons_views": "↢ عرض مواسم المسلسلات",
        "series_episodes_views": "↢ عرض حلقات المسلسلات",
        "series_episode_servers_views": "↢ عرض سيرفرات حلقات المسلسلات",
    }

    while True:
        now = datetime.now(TZ)
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # Wait until midnight in Morocco
        await asyncio.sleep((tomorrow - now).total_seconds())

        report_date = datetime.now(TZ).date() - timedelta(days=1)
        report_date = report_date.isoformat()

        cursor.execute("""
            SELECT name, count
            FROM bot_stats
            WHERE date = ?
        """, (report_date,))

        stats = dict(cursor.fetchall())

        message = (
            f"📊 **إحصائيات البوت اليومية**\n"
            f"📅 التاريخ: `{report_date}`\n\n"
        )

        for name, label in STAT_LABELS.items():
            message += f"{label}: `{stats.get(name, 0)}`\n"

        try:
            await bot.send_message(OWNER_ID, message)
        except Exception as e:
            print(f"Failed to send daily stats: {e}")



async def NoticeOwner(message):
    try:
        await bot.send_message(entity=OWNER_ID, message=message)
    except Exception as error:print(f"[ERROR OWNER MSG] >> {error}")


@bot.on(events.NewMessage(pattern=r"^/start(?:\s+(.*))?$"))
async def start_bot(event, show_menu=False):

    # ADD USER TO DATABASE
    user_id, username = event.sender.id, event.sender.username
    created_at = datetime.now().strftime(format="%d/%m/%Y, %H:%M:%S")
    if event.is_private:
        cursor.execute(f"SELECT id FROM bot_users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO bot_users (id, username, created_at) VALUES (?,?,?)", (user_id, username, created_at,))
            database.commit()

            await NoticeOwner(f"**[NEW USER] >> **__[{user_id}](tg://user?id={user_id}) (@{username})__")

    if not show_menu:
        is_query = event.pattern_match.group(1)
        if is_query:
            return

    total_movies = cursor.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    total_series = cursor.execute("SELECT COUNT(*) FROM series").fetchone()[0]

    buttons = [
        SEARCH_BTN,
        RANDOM_SEARCH,
        [Button.url(text="✉ تابع أحدث التحديثات أولًا بأول", url="https://t.me/ArabicFilmNews", style="success")]
    ]

    if event.chat_id == OWNER_ID:
        buttons.append([Button.inline("📢 Braodcast", "braodcast")])
        buttons.append([Button.inline("📊 Statistics", "statistics")])

    maintance = "<blockquote expandable>⚠️ قسم المسلسلات قيد التحديث.</blockquote>"
    await event.reply(
        f"""
🍿 <i><b>مكتبة الأفلام والمسلسلات في مكان واحد، شاهدها أو حمّلها مباشرةً دون إعلانات مزعجة.</b></i>


<blockquote expandable>
• الأفلام ← {total_movies}
• المسلسلات ← {total_series}

← أفلام أجنبية
← أفلام كورية
← أفلام أنمي
← أفلام آسيوية
← مسلسلات أجنبية
← مسلسلات كورية
← مسلسلات أنمي
← مسلسلات آسيوية
</blockquote>
{maintance}
""",
        buttons=buttons,
        parse_mode="html"
    )


@bot.on(events.CallbackQuery(data=b"show_menu"))
async def show_menu(event):
    await start_bot(event, show_menu=True)


@bot.on(events.InlineQuery())
async def inline_handler(event):
    global BOT_USERNAME

    if not BOT_USERNAME:
        bot_data = await bot.get_me()
        BOT_USERNAME = getattr(bot_data, "username", None)

    user_id = event.sender.id
    builder = event.builder
    query = event.text.strip()

    # await NoticeOwner(f"**[USER QUERY] >> **__[{user_id}](tg://user?id={user_id}) (query: {query})__")

    used_engine = False
    if not query:
        add_stat("total_searches", increase_by=1)
        cursor.execute(
            """
            SELECT * FROM (
                SELECT id, title, poster, release_date, story, 'فيلم' AS type FROM (
                    SELECT id, title, poster, release_date, story FROM movies ORDER BY RANDOM() LIMIT 25
                )
                UNION ALL
                SELECT id, title, poster, release_date, story, 'مسلسل' AS type FROM (
                    SELECT id, title, poster, release_date, story FROM series ORDER BY RANDOM() LIMIT 25
                )
            )
            ORDER BY RANDOM()""",
        )
    elif query == "random_movie":
        add_stat("movie_suggestions", increase_by=1)
        cursor.execute(
            """
            SELECT id, title, poster, release_date, story, 'فيلم' AS type
            FROM movies
            ORDER BY RANDOM()
            LIMIT 50
            """,
        )
    elif query == "random_serie":
        add_stat("series_suggestions", increase_by=1)
        cursor.execute(
            """
            SELECT id, title, poster, release_date, story, 'مسلسل' AS type
            FROM series
            ORDER BY RANDOM()
            LIMIT 50
            """,
        )
    else:
        used_engine = True
        add_stat("total_searches", increase_by=1)
        engine_results = search_movies(database, cursor, query)

    if used_engine:
        movies = engine_results
    else:
        movies = cursor.fetchall()

    results = []
    for movie_id, title, poster, release_date, story, item_type in movies:
        thumb = None
        if poster:
            thumb = types.InputWebDocument(
                url=poster,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            )

        if query == "random_movie" or query == "random_serie":
            description = story
        else:
            description = f"النوع: {item_type} | سنة الانتاج: {release_date}"

        details = f"""<s><em>/get_{movie_id}</em></s>
🎬 <b>{title}</b>

📖 <b>القصة ⬋</b>
<blockquote expandable>{story}</blockquote>
"""

        if item_type == "فيلم":
            show_text = "🎬 عرض تفاصيل الفيلم"
        else:
            show_text = "🍿 عرض تفاصيل المسلسل"

        buttons = [
            [Button.url(show_text, f"https://t.me/{BOT_USERNAME}?start=get_{movie_id}")],
            SEARCH_BTN,
            RANDOM_SEARCH
        ]
        result = builder.article(
            title=title,
            description=description,
            buttons=buttons,
            text=details,
            thumb=thumb,
            content=thumb,
            id=str(uuid.uuid4()),
            parse_mode="html"
        )

        results.append(result)

    await event.answer(
        results,
        cache_time=0
    )


def find_item(item_type, item_id):

    if item_type == "movie":
        table_name = "movies"
        share_text = "➥ مشاركة الفيلم"
        watch_download = [Button.inline("🍿 سيرفرات المشاهدة و التحميل 🍿", data=f"movieServers_{item_id}", style="success")]
    elif item_type == "serie":
        table_name = "series"
        share_text = "➥ مشاركة المسلسل"
        watch_download = [Button.inline("🍿 عرض مواسم المسلسل 🍿", data=f"serieServers_{item_id}", style="success")]

    cursor.execute(
        f"SELECT title, poster, tags, rate, release_date, duration, story FROM {table_name} WHERE id = ?",
        (item_id,)
    )

    item_data = cursor.fetchone()
    if not item_data:
        return [None, None, None]

    title, poster, category, rating, release_date, duration, story = item_data

    # Send the actual movie
    details = f"""🎬 <b>{title}</b>

📖 <b>القصة ⬋</b>
<blockquote expandable>{story}</blockquote>
"""

    if rating:
        rating = float(rating)
        full_stars = int(rating)
        half_star = rating % 1 >= 0.5
        empty_stars = 10 - full_stars - int(half_star)
        # rate_as_stars = "☆" * empty_stars + ("✬" if half_star else "") + "★" * full_stars + f" ( ⭐ {rating} )"
        rate_as_stars = f"[ ★ {rating}/10 ]"
    else:
        rate_as_stars = None

    if release_date:release_date = f"[ 🗓 {release_date} ]"
    else:release_date = None

    if duration:duration = f"[ ⏱️ {duration} ]"
    else:duration = None

    if category:
        categories = json.loads(category.replace("'", '"'))

        emojis = {
            "اكشن": "🔥",
            "اثارة": "⚡",
            "رعب": "👻",
            "دراما": "🎭",
            "رومانسي": "❤️",
            "كوميدي": "😂",
            "فانتازيا": "🧙",
            "مغامرة": "🏹",
            "خيال علمي": "🚀",
            "جريمة": "🔪",
            "غموض": "🕵️",
            "عائلي": "👨‍👩‍👧‍👦",
            "كرتون": "🎨",
            "تاريخي": "🏛️",
            "حربي": "⚔️",
            "سيرة ذاتية": "👤",
            "وثائقي": "📽️",
            "رياضي": "🏆",
            "موسيقي": "🎵",
            "Music": "🎵",
            "ويسترن": "🤠",
            "قصير": "⏱️",
            "Short": "⏱️",
        }

        category =  " ╎ ".join(f"{emojis.get(cat, '🎬')} {cat}" for cat in categories)
    else:
        category = "🎭 N/A"

    btns_row1 = []
    if rate_as_stars:btns_row1.append(Button.inline(text=rate_as_stars, data="show_rate"))
    if release_date:btns_row1.append(Button.inline(text=release_date, data="show_release"))
    btns_row2 = []
    if duration:btns_row2.append(Button.inline(text=duration, data="show_duration"))

    buttons = [
        btns_row1,
        btns_row2,
        [
            Button.inline(text=category, data="show_category")
        ],
        watch_download,
        SEARCH_BTN,
        RANDOM_SEARCH,
        [
            Button.inline("القائمة الرئيسية »", data="show_menu"),
            Button.switch_inline(share_text, query=title, same_peer=False, style="success")
        ]
    ]

    return [poster, details, buttons]


@bot.on(events.NewMessage(pattern=r"(?:/get_(\d+)|/start\s+get_(\d+))"))
async def movie_handler(event):
    movie_id = int(event.pattern_match.group(1) or event.pattern_match.group(2))
    user_id = event.sender.id

    if not event.pattern_match.group(2):
        try:await event.delete()
        except:pass

    if len(str(movie_id)) == 12:
        add_stat("series_requests", increase_by=1)
        poster, details, buttons = find_item(item_type="serie", item_id=movie_id)
        # await NoticeOwner(f"**[USER REQUEST SERIE] >> **__[{user_id}](tg://user?id={user_id}) (id: /get_{movie_id})__")
    else:
        add_stat("movie_requests", increase_by=1)
        poster, details, buttons = find_item(item_type="movie", item_id=movie_id)
        # await NoticeOwner(f"**[USER REQUEST MOVIE] >> **__[{user_id}](tg://user?id={user_id}) (id: /get_{movie_id})__")
    
    if not poster and not details and not buttons:
        await NoticeOwner(f"**[USER REQUEST NOT FOUND] >> **__[{user_id}](tg://user?id={user_id}) (id: /get_{movie_id})__")
        return
    
    try:
        await event.respond(file=poster, message=details, buttons=buttons, parse_mode="html")
    except Exception as error:
        print(f"[ERROR IN POSTER ({poster})] >> {error}")
        await event.respond(message=details, buttons=buttons, parse_mode="html")


@bot.on(events.CallbackQuery(pattern=rb"^(movieServers|serieServers|episodeServers)_(\d+)$"))
async def movie_callback(event):
    action = event.pattern_match.group(1).decode()
    movie_id = int(event.pattern_match.group(2))

    user_id = event.sender.id
    
    if action == "serieServers":
        # await NoticeOwner(f"**[USER REQUESTED SEASONS] >> **__[{user_id}](tg://user?id={user_id}) (action: {action} -- /get_{movie_id})__")
        add_stat("series_seasons_views", increase_by=1)
        await show_serie_seasons(event, series_id=movie_id)
        # await event.answer("⚠️ قسم المسلسلات قيد التحديث، حاول لاحقًا.", alert=True)
        return


    # await NoticeOwner(f"**[USER REQUESTED SERVER] >> **__[{user_id}](tg://user?id={user_id}) (action: {action} -- /get_{movie_id})__")
    if action == "movieServers":
        add_stat("movie_servers_views", increase_by=1)
    elif action == "episodeServers":
        add_stat("series_episode_servers_views", increase_by=1)

    buttons = []

    if action == "movieServers":
        cursor.execute("SELECT id, server_name, quality, url FROM movie_servers WHERE movie_id = ? AND server_type = ?", (movie_id, "download"))
        download_servers = cursor.fetchall()
    elif action == "episodeServers":
        cursor.execute("SELECT id, server_name, quality, url FROM episode_servers WHERE episode_id = ? AND server_type = ?", (movie_id, "download"))
        download_servers = cursor.fetchall()

        season_id, episode_number = cursor.execute("SELECT season_id, episode_number FROM episodes WHERE id = ?", (movie_id,)).fetchone()
        serie_id, season_number = cursor.execute("SELECT series_id, season_number FROM seasons WHERE id = ?", (season_id,)).fetchone()

        buttons.append([Button.inline(text=f"[ الموسم: {season_number} ] ↜ [ الحلقة: {episode_number} ]", data="season_episode_do_nothing", style="success")])

    buttons.append([Button.inline(text="💾 سيرفرات التحميل", data="download_do_nothing", style="success")])
    current_row = []
    for id, server_name, quality, url in download_servers:
        button = Button.url(text=f"{server_name} ({quality})", url=url, style="primary")

        if server_name == "VideoTube":
            if current_row:
                buttons.append(current_row)
                current_row = []
            buttons.append([button])
        else:
            current_row.append(button)
            if len(current_row) == 2:
                buttons.append(current_row)
                current_row = []

    if current_row:buttons.append(current_row)


    buttons.append([Button.inline(text="🍿 سيرفرات المشاهدة", data="watch_do_nothing", style="success")])
    if action == "movieServers":
        cursor.execute("SELECT id, server_name, quality, url FROM movie_servers WHERE movie_id = ? AND server_type = ?", (movie_id, "watch"))
        watch_servers = cursor.fetchall()
    elif action == "episodeServers":
        cursor.execute("SELECT id, server_name, quality, url FROM episode_servers WHERE episode_id = ? AND server_type = ?", (movie_id, "watch"))
        watch_servers = cursor.fetchall()

    current_row = []
    for id, server_name, quality, url in watch_servers:
        button = Button.url(text=f"{server_name}", url=url, style="primary")

        current_row.append(button)
        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []

    if current_row:buttons.append(current_row)


    buttons.append(
        [Button.inline(text="× أغلق هذه الرسالة ×", data="close_msg", style="danger")]
    )

    await event.respond(
        f"__روابط المشاهدة والتحميل جاهزة، مشاهدة ممتعة!__ 🍿",
        buttons=buttons
    )


async def show_serie_seasons(event, series_id):

    cursor.execute("SELECT id, season_number, title FROM seasons WHERE series_id = ? ORDER BY season_number ASC", (series_id,))
    seasons = cursor.fetchall()

    if seasons:
        serie_title, = cursor.execute("SELECT title FROM series WHERE id = ?", (series_id,)).fetchone()

        buttons, pre_buttons = [], []
        buttons.append([Button.inline(text=f"🍿 {serie_title} 🍿", data="serie_do_nothing", style="success")])

        for season_id, season_number, season_title in seasons:
            pre_buttons.append(Button.inline(text=f"الموسم {season_number}", data=f"seasonEpisodes_{season_id}"))

            if len(pre_buttons) == 2:
                buttons.append(pre_buttons.copy())
                pre_buttons.clear()
                
        if pre_buttons:buttons.append(pre_buttons.copy())
        buttons.append([Button.inline(text="× أغلق هذه الرسالة ×", data="close_msg", style="danger")])

        await event.respond("🎬 __اختر الموسم الذي تريده لعرض حلقاته:__", buttons=buttons)
    else:
        await event.answer("لا تتوفر مواسم لهذا المسلسل حاليًا، يرجى المحاولة مرة أخرى لاحقًا.", alert=True)


@bot.on(events.CallbackQuery(pattern=r"seasonEpisodes_(\d+)"))
async def season_episodes_callback(event):
    season_id = int(event.pattern_match.group(1).decode())

    user_id = event.sender.id
    # await NoticeOwner(f"**[USER REQUESTED EPISODES] >> **__[{user_id}](tg://user?id={user_id}) (season id: {season_id})__")
    add_stat("series_episodes_views", increase_by=1)

    cursor.execute("SELECT id, episode_number, title, duration FROM episodes WHERE season_id = ? ORDER BY episode_number ASC", (season_id,))
    episodes = cursor.fetchall()

    if episodes:
        season_number, = cursor.execute("SELECT season_number FROM seasons WHERE id = ?", (season_id,)).fetchone()

        buttons, pre_buttons = [], []
        buttons.append([Button.inline(text=f"🍿 الموسم {season_number} 🍿", data="season_do_nothing", style="success")])
        
        for episode_id, episode_number, title, duration in episodes:
            pre_buttons.append(Button.inline(text=f"الحلقة {episode_number}", data=f"episodeServers_{episode_id}"))
            
            if len(pre_buttons) == 3:
                buttons.append(pre_buttons.copy())
                pre_buttons.clear()
                
        if pre_buttons:buttons.append(pre_buttons.copy())
        buttons.append([Button.inline(text="× أغلق هذه الرسالة ×", data="close_msg", style="danger")])

        await event.respond("🎬 __اختر الحلقة التي تريدها لعرض سيرفرات المشاهدة:__", buttons=buttons)

    else:
        await event.answer("لا تتوفر حلقات لهذا الموسم حاليًا، يرجى المحاولة مرة أخرى لاحقًا.", alert=True)


@bot.on(events.CallbackQuery(pattern="close_msg"))
async def close_msg(event):
    await event.delete()


print("Bot started")

bot.loop.create_task(daily_stats_report())
bot.run_until_disconnected()