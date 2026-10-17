from datetime import datetime

# CURRENT TIME
async def GetCurrentTime():
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d -- %H:%S')
    return current_time
