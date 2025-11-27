from telegram import Update
from telegram.ext import ContextTypes
# मान लेते हैं कि 'utils' मॉड्यूल में 'get_user' और 'users' (MongoDB collection) हैं
# आपको यह सुनिश्चित करना होगा कि 'utils.py' में 'get_user' और 'users' सही से परिभाषित हों।
from utils import get_user, users 
from datetime import datetime
from random import randint
import typing # टाइप हिंटिंग के लिए, खासकर जब `get_user` किसी डिक्ट (उपयोगकर्ता डेटा) को लौटाता है

# आपको इस फंक्शन को 'main.py' में इंपोर्ट करना होगा
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    यूजर को मारने और हत्यारे को इनाम देने के लिए एक इकोनॉमी कमांड।
    """
    
    # सुनिश्चित करें कि एक मैसेज मौजूद है
    if not update.message:
        return

    user_id = update.effective_user.id
    # 'get_user' से आने वाले डेटा के लिए टाइप हिंट (मान लें कि यह एक डिक्ट है)
    killer_user: typing.Dict = get_user(user_id)
    
    # 1. रिप्लाई की जांच करें
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ कृपया किसी को मारने के लिए रिप्लाई करें!")

    target_user_object = update.message.reply_to_message.from_user
    target_id = target_user_object.id
    target_name = target_user_object.first_name
    
    # 2. खुद को मारने से रोकें
    if user_id == target_id:
        return await update.message.reply_text("❌ आप खुद को नहीं मार सकते!")
    
    # 3. टारगेट यूज़र को लाएँ
    target_user: typing.Dict = get_user(target_id)
    
    # 4. हत्यारे की स्थिति की जांच करें (क्या वह खुद मरा हुआ है?)
    if killer_user.get("is_dead", False):
        return await update.message.reply_text("❌ मृत यूज़र किसी को नहीं मार सकते!")

    # 5. टारगेट की स्थिति की जांच करें (क्या वह पहले से ही मृत है?)
    if target_user.get("is_dead", False):
        return await update.message.reply_text(f"💀 **{target_name}** पहले से ही मृत है!")

    # 6. प्रोटेक्शन की जांच करें
    # यदि target_user में 'protection' की है और उसकी datetime.utcnow() से ज़्यादा है।
    protection_end_time = target_user.get("protection")
    if protection_end_time and isinstance(protection_end_time, datetime) and protection_end_time > datetime.utcnow():
        return await update.message.reply_text("Nice try on me, better luck next time!😂") 

    # 7. मारें और इनाम दें
    
    # इनाम 100 से 200 के बीच सेट करें
    earned_amount = randint(100, 200)

    # a) टारगेट को 'dead' के रूप में चिह्नित करें
    users.update_one(
        {"user_id": target_id}, 
        {"$set": {"is_dead": True}}
    )
    
    # b) हत्यारे के बैलेंस और किल्स को अपडेट करें
    users.update_one(
        {"user_id": user_id}, 
        {"$inc": {"balance": earned_amount, "kills": 1}}
    )
    
    # फाइनल मैसेज
    await update.message.reply_text(
        f"💀 **{target_name}** killed **{target_name}**! 💰 Earned: **${earned_amount}**"
    )
