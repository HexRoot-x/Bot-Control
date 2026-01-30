import telebot
import os
import subprocess
import pyautogui
import psutil
import cv2
import time
from datetime import datetime

# الإعدادات
TOKEN = 'توكن_البوت_هنا'
ADMIN_ID = 'معرف_المستخدم_الخاص_بك'
bot = telebot.TeleBot(TOKEN)

# التحقق من الهوية
def is_me(user_id):
    return str(user_id) == ADMIN_ID

# إنشاء لوحة الأزرار الرئيسية
def main_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    row1 = [
        telebot.types.KeyboardButton('📷 صورة'),
        telebot.types.KeyboardButton('🖼️ لقطة'),
        telebot.types.KeyboardButton('🔒 قفل'),
        telebot.types.KeyboardButton('💻 معلومات')
    ]
    
    row2 = [
        telebot.types.KeyboardButton('📁 ملفات'),
        telebot.types.KeyboardButton('🔍 بحث'),
        telebot.types.KeyboardButton('📶 شبكة'),
        telebot.types.KeyboardButton('🛠️ أوامر')
    ]
    
    row3 = [
        telebot.types.KeyboardButton('🔊 صوت أعلى'),
        telebot.types.KeyboardButton('🔈 صوت أقل'),
        telebot.types.KeyboardButton('❓ مساعدة'),
        telebot.types.KeyboardButton('❌ إغلاق')
    ]
    
    markup.add(*row1)
    markup.add(*row2)
    markup.add(*row3)
    return markup

# لوحة أوامر متقدمة
def commands_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    row1 = [
        telebot.types.KeyboardButton('⌨️ CMD'),
        telebot.types.KeyboardButton('📝 اكتب نص'),
        telebot.types.KeyboardButton('🖱️ انقر'),
        telebot.types.KeyboardButton('📊 مهام')
    ]
    
    row2 = [
        telebot.types.KeyboardButton('🔙 رجوع'),
        telebot.types.KeyboardButton('🔄 تحديث'),
        telebot.types.KeyboardButton('🏠 رئيسية')
    ]
    
    markup.add(*row1)
    markup.add(*row2)
    return markup

# لوحة التحكم بالصوت
def volume_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    
    row = [
        telebot.types.KeyboardButton('🔊 +'),
        telebot.types.KeyboardButton('🔈 -'),
        telebot.types.KeyboardButton('🔇 كتم'),
        telebot.types.KeyboardButton('🔙 رجوع')
    ]
    
    markup.add(*row)
    return markup

# بداية البوت
@bot.message_handler(commands=['start', 'help'])
def start(message):
    if not is_me(message.from_user.id):
        bot.reply_to(message, "❌ هذا البوت شخصي فقط")
        return
    
    welcome = "👋 *أهلاً!*\n\n"
    welcome += "استخدم الأزرار للتحكم في جهازك:\n\n"
    welcome += "📷 - صورة من الكاميرا\n"
    welcome += "🖼️ - لقطة شاشة\n"
    welcome += "💻 - معلومات النظام\n"
    welcome += "🔒 - قفل الجهاز\n"
    welcome += "📁 - عرض الملفات\n\n"
    welcome += "📱 *اختر من الأزرار أدناه:*"
    
    bot.send_message(
        message.chat.id,
        welcome,
        parse_mode='Markdown',
        reply_markup=main_keyboard()
    )

# معالجة الأزرار
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if not is_me(message.from_user.id):
        return
    
    text = message.text.strip()
    
    if text == '📷 صورة':
        take_photo(message)
    
    elif text == '🖼️ لقطة':
        screenshot(message)
    
    elif text == '🔒 قفل':
        lock_pc(message)
    
    elif text == '💻 معلومات':
        system_info(message)
    
    elif text == '📁 ملفات':
        list_files(message)
    
    elif text == '🔍 بحث':
        bot.reply_to(message, "🔍 اكتب اسم الملف للبحث:", reply_markup=commands_keyboard())
    
    elif text == '📶 شبكة':
        network_info(message)
    
    elif text == '🛠️ أوامر':
        bot.send_message(
            message.chat.id,
            "🛠️ *الأوامر المتقدمة:*\n\n"
            "⌨️ CMD - تنفيذ أمر\n"
            "📝 اكتب نص - كتابة نص\n"
            "🖱️ انقر - نقر بالماوس\n"
            "📊 مهام - المهام النشطة",
            parse_mode='Markdown',
            reply_markup=commands_keyboard()
        )
    
    elif text == '🔊 صوت أعلى':
        volume_up(message)
    
    elif text == '🔈 صوت أقل':
        volume_down(message)
    
    elif text == '❓ مساعدة':
        start(message)
    
    elif text == '❌ إغلاق':
        bot.reply_to(message, "✅ تم إغلاق الأزرار", reply_markup=telebot.types.ReplyKeyboardRemove())
    
    elif text == '⌨️ CMD':
        bot.reply_to(message, "💻 اكتب الأمر الذي تريد تنفيذه:")
    
    elif text == '📝 اكتب نص':
        bot.reply_to(message, "⌨️ اكتب النص الذي تريد كتابته:")
    
    elif text == '🖱️ انقر':
        pyautogui.click()
        bot.reply_to(message, "✅ تم النقر", reply_markup=commands_keyboard())
    
    elif text == '📊 مهام':
        show_tasks(message)
    
    elif text == '🔙 رجوع' or text == '🏠 رئيسية':
        bot.send_message(
            message.chat.id,
            "🏠 *القائمة الرئيسية*",
            parse_mode='Markdown',
            reply_markup=main_keyboard()
        )
    
    elif text == '🔄 تحديث':
        bot.reply_to(message, "🔄 تم التحديث", reply_markup=main_keyboard())
    
    elif text == '🔊 +':
        volume_up(message)
    
    elif text == '🔈 -':
        volume_down(message)
    
    elif text == '🔇 كتم':
        pyautogui.press('volumemute')
        bot.reply_to(message, "🔇 تم كتم الصوت", reply_markup=volume_keyboard())
    
    # أوامر CMD
    elif text.startswith('cmd ') or text.startswith('CMD '):
        run_cmd(message)
    
    # كتابة نص
    elif len(text) > 10 and 'اكتب' not in text:
        pyautogui.write(text)
        bot.reply_to(message, f"✅ تم كتابة النص", reply_markup=main_keyboard())
    
    # البحث عن ملفات
    elif len(text) > 2 and text not in ['🔍 بحث']:
        search_file(message)

# ========== الوظائف الأساسية ==========

def take_photo(message):
    try:
        bot.reply_to(message, "📸 جاري التقاط الصورة...")
        
        for cam_index in range(3):
            camera = cv2.VideoCapture(cam_index)
            if camera.isOpened():
                ret, frame = camera.read()
                camera.release()
                
                if ret:
                    filename = f"photo_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)
                    
                    with open(filename, 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption="📸 صورة من الكاميرا")
                    
                    os.remove(filename)
                    return
        
        bot.reply_to(message, "❌ لا توجد كاميرا")
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def screenshot(message):
    try:
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename)
        
        with open(filename, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="🖼️ لقطة الشاشة")
        
        os.remove(filename)
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def lock_pc(message):
    try:
        os.system('rundll32.exe user32.dll,LockWorkStation')
        bot.reply_to(message, "🔒 تم قفل الجهاز")
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def system_info(message):
    try:
        info = []
        info.append(f"👤 *المستخدم:* {os.getlogin()}")
        info.append(f"💻 *المعالج:* {psutil.cpu_percent()}%")
        info.append(f"🧠 *الذاكرة:* {psutil.virtual_memory().percent}%")
        info.append(f"💾 *التخزين:* متاح")
        info.append(f"🕐 *الوقت:* {datetime.now().strftime('%H:%M')}")
        
        bot.reply_to(message, "\n".join(info), parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def list_files(message):
    try:
        path = os.path.expanduser('~')
        items = os.listdir(path)[:15]
        
        if not items:
            bot.reply_to(message, "📂 المجلد فارغ")
            return
        
        files_list = ["📁 *مجلد المستخدم:*\n"]
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                files_list.append(f"📁 {item}/")
            else:
                size = os.path.getsize(item_path)
                if size < 1024:
                    size_str = f"{size} ب"
                elif size < 1024**2:
                    size_str = f"{size/1024:.0f} ك"
                else:
                    size_str = f"{size/(1024**2):.1f} م"
                files_list.append(f"📄 {item} ({size_str})")
        
        response = "\n".join(files_list)
        bot.reply_to(message, response, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def search_file(message):
    try:
        search = message.text.strip()
        bot.reply_to(message, f"🔍 جاري البحث عن '{search}'...")
        
        results = []
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        
        for root, dirs, files in os.walk(desktop):
            for file in files:
                if search.lower() in file.lower():
                    results.append(os.path.basename(file))
                    if len(results) >= 8:
                        break
        
        if results:
            response = f"✅ *النتائج:*\n\n" + "\n".join([f"• {r}" for r in results[:8]])
        else:
            response = f"❌ لم أجد '{search}'"
        
        bot.reply_to(message, response, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def network_info(message):
    try:
        net = psutil.net_io_counters()
        
        info = []
        info.append("📶 *استخدام الشبكة:*")
        info.append(f"📥 الوارد: {net.bytes_recv / (1024**2):.1f} م.ب")
        info.append(f"📤 الصادر: {net.bytes_sent / (1024**2):.1f} م.ب")
        
        bot.reply_to(message, "\n".join(info), parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def volume_up(message):
    for _ in range(3):
        pyautogui.press('volumeup')
    bot.reply_to(message, "🔊 تم رفع الصوت")

def volume_down(message):
    for _ in range(3):
        pyautogui.press('volumedown')
    bot.reply_to(message, "🔉 تم خفض الصوت")

def show_tasks(message):
    try:
        processes = []
        for proc in psutil.process_iter(['name', 'memory_percent']):
            try:
                processes.append((proc.info['name'], proc.info['memory_percent']))
            except:
                pass
        
        processes.sort(key=lambda x: x[1], reverse=True)
        
        tasks_info = "📊 *المهام النشطة:*\n\n"
        for i, (name, mem) in enumerate(processes[:8], 1):
            tasks_info += f"{i}. {name[:15]:15} - {mem:.1f}%\n"
        
        bot.reply_to(message, tasks_info, parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

def run_cmd(message):
    try:
        cmd = message.text[4:].strip()  # إزالة "cmd "
        
        if not cmd:
            bot.reply_to(message, "💻 اكتب الأمر بعد cmd")
            return
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout or result.stderr or "✅ تم التنفيذ"
        
        if len(output) > 2000:
            output = output[:2000] + "\n... (طويل جداً)"
        
        bot.reply_to(message, f"```\n{output}\n```", parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

# تشغيل البوت
print("🚀 بدأ تشغيل البوت...")
print("📱 أرسل /start في تيليجرام")
bot.polling(none_stop=True)
