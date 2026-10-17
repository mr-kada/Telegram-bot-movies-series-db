from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon import Button
from telethon.tl.types import ReplyKeyboardHide



# channels
must_join = ["zxllkada", "mz_space"]



async def JoinFunction(event):
    global must_join
    
    try:
        await event.answer("⏳ تحقق من المطلوب")
    except:
        pass
    MustJoinChannlesButton = []
    for channel_id in must_join:
        MustJoinChannlesButton.append([Button.url(channel_id, f'https://t.me/{channel_id}')])
        
    MustJoinChannlesButton.append([Button.inline('تحقق ✔️', 'check_now')])
    MustDashboard = await event.client.send_message(event.chat_id, '__اشترك في القنوات التالية لتتمكن من اكمال استخدام البوت__', buttons=MustJoinChannlesButton)

async def JoinFunction2(event):
    global must_join
    
    try:
        await event.answer("⏳ تحقق من المطلوب")
    except:
        pass
    MustJoinChannlesButton = []
    for channel_id in must_join:
        MustJoinChannlesButton.append([Button.url(channel_id, f'https://t.me/{channel_id}')])
        
    MustJoinChannlesButton.append([Button.inline('تحقق ✔️', 'check_now2')])
    MustDashboard = await event.client.send_message(event.chat_id, '__اشترك في القنوات التالية لتتمكن من اكمال استخدام البوت__', buttons=MustJoinChannlesButton)


async def check_joined(event, UserDashboard, result):
    global must_join
    
    joined = True
    for channel_id in must_join:
        try:
            user_exist = await event.client(GetParticipantRequest(channel=channel_id, participant=event.chat_id))
        except UserNotParticipantError:
            joined = False
            break
        except Exception as error:
            #print (f"ERROR (check_joined) [USER: {event.chat_id}] >> {error}")
            joined = True
            break

    MustDashboard = await event.client.send_message(event.chat_id, '__جاري المعالجة__', buttons=ReplyKeyboardHide())
    await MustDashboard.delete()

    if joined == False:
        if result != "NoDashboard":
            await JoinFunction(event)
        else:
            await JoinFunction2(event)
    else:
        if result != "NoDashboard":
            redirect = await UserDashboard(event)
        return True
    


    
    
    