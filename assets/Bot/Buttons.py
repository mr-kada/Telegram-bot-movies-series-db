from telethon.tl.types import ReplyInlineMarkup
from telethon.tl.types import KeyboardButtonRow
from telethon.tl.types import KeyboardButtonCallback

# MAIN KEYDOARD
async def MarkupKeyboard():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='👨‍💻👩‍💻  ملفي الشخصي  👩‍💻👨‍💻', data=b'Profile')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='⭐️  أفضل 50 مسلسل  ⭐️', data=b'TopSeries'),
                KeyboardButtonCallback(text='⭐️  أفضل 50 فيلم  ⭐️', data=b'TopMovies')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🎲  إقتراح عشوائي  🎲', data=b'Clicked_2')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🎲  إقتراح حسب التصنيف  🎲', data=b'Clicked_9')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='📈✏️  أعلى المساهمين - ساهم بالإضافة  ✏️📈', data=b'Clicked_9')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🇲🇦 Made in Morooco', data=b'Clicked_10')
            ]
        )
        
    ])
    
    return Keyboard
    
# PROFILE KEYDOARD
async def MarkupKeyboard_Profile():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🎖  تغيير المسلسل المفضل  🎖', data=b'ChangeSerie')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🎖  تغيير الفيلم المفضل  🎖', data=b'ChangeMovie'),
                KeyboardButtonCallback(text='🧬  تغيير الجنس  🧬', data=b'ChangeGender')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🖱  رجوع للقائمة الرئيسية  🖱', data=b'Back')
            ]
        )
    ])
    
    return Keyboard
    
# CONFIRM SERIE KEYBOARD
async def MarkupKeyboard_Profile_SerieConfirm():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='إلغاء  ❌', data=b'Cancel'),
                KeyboardButtonCallback(text='✅  تأكيد', data=b'SerieConfirm')
            ]
        )
    ])
    
    return Keyboard
    
# CONFIRM MOVIE KEYBOARD
async def MarkupKeyboard_Profile_MovieConfirm():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='إلغاء  ❌', data=b'Cancel'),
                KeyboardButtonCallback(text='✅  تأكيد', data=b'MovieConfirm')
            ]
        )
    ])
    
    return Keyboard  

# SELECT GENDER
async def MarkupKeyboard_Profile_ChangeGender():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='👨‍💼  ذكر', data=b'Male'),
                KeyboardButtonCallback(text='👩‍💼  أنثى', data=b'Female')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='👽  كائن فضائي', data=b'alien')
            ]
        )
    ])
    
    return Keyboard 

# RETURN ON SUCCESS
async def MarkupKeyboard_Profile_BackOnSuccess():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🖱   رجوع لقائمة المعلومات  🖱', data=b'BackOnSuccess')
            ]
        )
    ])
    
    return Keyboard
    
    
# TOP MOVIES NEXT
async def MarkupKeyboard_TopMovies_Next():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='➡️  التالي', data=b'NextTopMovies')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🖱  رجوع للقائمة الرئيسية  🖱', data=b'TopBack')
            ]
        )
    ])
    
    return Keyboard
    
# TOP MOVIES NEXT WITH PREVIOUS
async def MarkupKeyboard_TopMovies_Next_With_Previous():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='⬅️  السابق', data=b'PreviousTopMovies'),
                KeyboardButtonCallback(text='➡️  التالي', data=b'NextTopMovies')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🖱  رجوع للقائمة الرئيسية  🖱', data=b'TopBack')
            ]
        )
    ])
    
    return Keyboard
    
# TOP MOVIES END
async def MarkupKeyboard_TopMovies_End():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='⬅️  السابق', data=b'EndTopMovies')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='🖱  رجوع للقائمة الرئيسية  🖱', data=b'TopBack')
            ]
        )
    ])
    
    return Keyboard
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
async def MarkupKeyboard_2():
    Keyboard = ReplyInlineMarkup(rows=[
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='📨  رسائل الإدارة 📨', data=b'Clicked_3'),
                KeyboardButtonCallback(text='📈  أعلى المساهمين  📈', data=b'Clicked_4')
            ]
        ),
        KeyboardButtonRow(
            buttons=[
                KeyboardButtonCallback(text='📝  مساهماتي  📝', data=b'Clicked_7'),
                KeyboardButtonCallback(text='✏️  ساهم بالإضافة  ✏️', data=b'Clicked_8')
            ]
        )
    ])
    
    return Keyboard
    
    
    
    
    