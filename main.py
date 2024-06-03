import streamlit as st
import tempfile
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


def process_audio(audio_file_path):
    """Process the audio using the user's prompt with Google's Generative API."""
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    audio_file = genai.upload_file(path=audio_file_path)
    response = model.generate_content(
        [
            """สรุปการประชุม อย่างละเอียด เพื่อง่ายต่อการดำเนินการต่อ และง่ายสำหรับคนที่กลับมาอ่าน ในภาษาไทย""",
            audio_file
        ]
    )
    return response.text
def clean_msg(msg):
    return msg.replace("**", "").replace("##", "#").replace("*","•").replace("\n\n","\n")

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None
st.image('image.png', width=700)
st.title('AI สรุปการประชุมจากไฟล์เสียง ฟรี!')
st.text("Application สำหรับสรุปการประชุมจากไฟล์เสียง")
st.text("ไฟล์เสียงที่รองรับ: wav, mp3, ogg, flac, m4a")
st.markdown("สามารถติดตามหรือขอให้สร้าง Application ใหม่ๆ ได้ที่ [Facebook Page #AI](https://www.facebook.com/profile.php?id=61560597801592)")
st.sidebar.markdown("""# About US""")
st.sidebar.markdown("""## สร้างโดยทีมงาน #AI \n\n #AI for people \n\nเพจที่รวบรวมข่าวสารที่เกี่ยวข้อง และแชร์เทคนิคๆ ต่างของ AI""")
st.sidebar.markdown("## สามารถติดตามเราได้ที่ \n\n **[Facbook Page #AI](https://www.facebook.com/profile.php?id=61560597801592)** ")
st.sidebar.image('logo.png', width=100)  
st.sidebar.markdown("สามารถใช้งานได้ฟรี และไม่มีค่าใช้จ่ายเพิ่มเติม \nโดย Google AI Studio \n\n")

audio_file = st.file_uploader("อัพโหลดไฟล์เสียง", type=["wav", "mp3", "ogg", "flac", "m4a"])
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)
    st.audio(audio_path)
    try:
        if st.button('Process Audio'):
            with st.spinner('Processing...'):
                processed_text = process_audio(audio_path)
                st.text_area("Processed Output", clean_msg(processed_text), height=500)
    except:
        st.error("ระบบไม่สามารถประมวลผลไฟล์เสียงได้ในขณะนี้ กรุณาลองใหม่อีกครั้ง เนื่องจากมีคนใช้งานจำนวนมาก กรุณาลองใหม่อีกครั้งในภายหลัง")