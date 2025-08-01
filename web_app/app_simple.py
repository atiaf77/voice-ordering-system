from flask import Flask, request, jsonify, render_template, send_from_directory
import speech_recognition as sr
from gtts import gTTS
import os
import openai
import webbrowser
from datetime import datetime
import json
import io
import tempfile

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Create directories for storing audio files
os.makedirs("audio_files", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Menu items
MENU = {
    "قهوة": {
        "إسبريسو": 15,
        "لاتيه": 20,
        "كابتشينو": 18,
        "أمريكانو": 12,
        "قهوة تركية": 10
    },
    "أكل": {
        "برجر": 35,
        "بيتزا": 40,
        "سندويش": 25,
        "سلطة": 20,
        "معكرونة": 30
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static', filename)

@app.route('/menu')
def get_menu():
    return jsonify(MENU)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        # Save the uploaded audio file
        audio_file = request.files['audio']
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Try to save the file directly as WAV first
        audio_path = f"audio_files/uploaded_audio_{timestamp}.wav"
        audio_file.save(audio_path)
        
        print(f"Audio file saved to: {audio_path}")
        print(f"File size: {os.path.getsize(audio_path)} bytes")

        # Convert audio to text
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise and record
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='ar-SA')
                print(f"Recognized text: {text}")
        except sr.UnknownValueError:
            # If direct WAV reading fails, try with different approach
            try:
                # Try reading as WebM and convert using speech_recognition's built-in capabilities
                with open(audio_path, 'rb') as f:
                    audio_data = f.read()
                
                # Save with different extension
                webm_path = f"audio_files/uploaded_audio_{timestamp}.webm"
                with open(webm_path, 'wb') as f:
                    f.write(audio_data)
                
                # Try using sr.Microphone or different approach
                return jsonify({"error": "لم يتم فهم الصوت، يرجى المحاولة مرة أخرى والتحدث بوضوح أكثر"})
                
            except Exception as e:
                print(f"Conversion error: {e}")
                return jsonify({"error": "مشكلة في تنسيق الملف الصوتي، يرجى المحاولة مرة أخرى"})
        except sr.RequestError as e:
            return jsonify({"error": f"حدث خطأ في خدمة التعرف على الصوت: {str(e)}"})
        except Exception as e:
            print(f"Audio processing error: {e}")
            return jsonify({"error": "مشكلة في قراءة الملف الصوتي، يرجى المحاولة مرة أخرى"})

        # Analyze the text and generate response
        response_text = analyze_order(text)

        # Convert response text to audio
        tts = gTTS(response_text, lang='ar', slow=False)
        response_audio_filename = f"response_audio_{timestamp}.mp3"
        response_audio_path = f"static/{response_audio_filename}"
        tts.save(response_audio_path)

        # Log the interaction
        log_interaction(text, response_text, timestamp)

        return jsonify({
            "text": response_text, 
            "audio": f"/static/{response_audio_filename}",
            "recognized_text": text
        })

    except Exception as e:
        print(f"Error processing audio: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"حدث خطأ في معالجة الصوت: {str(e)}"})

def analyze_order(text):
    """Analyze the user's order and generate appropriate response"""
    text_lower = text.lower()
    
    # Check for greetings
    greetings = ["مرحبا", "أهلا", "السلام عليكم", "صباح الخير", "مساء الخير", "هاي", "هلو"]
    if any(greeting in text_lower for greeting in greetings):
        return "أهلاً وسهلاً بك! كيف يمكنني مساعدتك؟ هل ترغب في طلب قهوة أم أكل؟"
    
    # Check for coffee orders
    coffee_keywords = ["قهوة", "coffee", "إسبريسو", "لاتيه", "كابتشينو", "أمريكانو"]
    if any(keyword in text_lower for keyword in coffee_keywords):
        coffee_menu = "أنواع القهوة المتاحة:\n"
        for item, price in MENU["قهوة"].items():
            coffee_menu += f"• {item}: {price} ريال\n"
        return coffee_menu + "ما نوع القهوة التي ترغب بها؟"
    
    # Check for food orders
    food_keywords = ["أكل", "food", "طعام", "برجر", "بيتزا", "سندويش", "وجبة"]
    if any(keyword in text_lower for keyword in food_keywords):
        food_menu = "الأطعمة المتاحة:\n"
        for item, price in MENU["أكل"].items():
            food_menu += f"• {item}: {price} ريال\n"
        return food_menu + "ما نوع الأكل الذي ترغب به؟"
    
    # Check for specific items
    for category, items in MENU.items():
        for item, price in items.items():
            if item in text_lower:
                return f"ممتاز! {item} سعره {price} ريال. هل تريد إضافة شيء آخر؟"
    
    # Check for order confirmation
    confirm_keywords = ["نعم", "موافق", "أريد", "أطلب", "اطلب", "تمام", "ok"]
    if any(keyword in text_lower for keyword in confirm_keywords):
        return "تم تأكيد طلبك! سيتم تحضيره خلال دقائق. شكراً لك!"
    
    # Check for cancellation
    cancel_keywords = ["لا", "إلغاء", "لا أريد", "cancel"]
    if any(keyword in text_lower for keyword in cancel_keywords):
        return "لا مشكلة! إذا احتجت أي شيء آخر، أنا هنا لمساعدتك."
    
    # Default response
    return "يرجى تحديد طلبك بوضوح أكثر. يمكنك قول 'قهوة' أو 'أكل' أو اختيار من القائمة المعروضة."

def log_interaction(user_input, response, timestamp):
    """Log user interactions for analysis"""
    log_entry = {
        "timestamp": timestamp,
        "user_input": user_input,
        "response": response
    }
    
    log_file = "interaction_log.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error logging interaction: {e}")

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)
