from telethon import Button
import asyncio, time


# ANIMATION
async def Animation(event):
    # BACK KEYBOARD
    BackKeyboard = [[Button.inline("الرجوع للقائمة الرئيسية ⇐", "BackToHome")]]
    
    Paragraph = """
__اذا كنت تريد دعمنا للاستمرار, يمكنك المحاولة لتخطي هذه الروابط:__

__- ceesty.com/eg2wIQ
- http://ceesty.com/eg2y1W
- http://ceesty.com/eg2y1J
- http://ceesty.com/eg2y2y__


__This bot made by @zkada ( 2023 - 2024 )__
__**IN MOROCCO**__ 🇲🇦
"""


    FirstAnimation = await event.client.send_message(event.chat_id, Paragraph, link_preview=False, buttons=BackKeyboard)
        
    # try:
    #     for _ in range(10):
    #         LoopAnimation = await event.client.edit_message(event.chat_id, FirstAnimation.id, ShadowParagraph, link_preview=False, buttons=BackKeyboard)
    #         time.sleep(0.3)
    #         LoopAnimation = await event.client.edit_message(event.chat_id, FirstAnimation.id, Paragraph, link_preview=False, buttons=BackKeyboard)
    #         time.sleep(0.3)

    #     LoopAnimation = await event.client.edit_message(event.chat_id, FirstAnimation.id, ShadowParagraph, link_preview=False, buttons=BackKeyboard)
    # except:
    #     pass