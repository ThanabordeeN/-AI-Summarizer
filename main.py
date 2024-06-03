import streamlit as st
import tempfile
import google.generativeai as genai
def API_KEY(api):
    GOOGLE_API_KEY = api
    genai.configure(api_key=GOOGLE_API_KEY)


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

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary file and return the path."""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error handling uploaded file: {e}")
        return None
st.image('image.png')
st.title('AI สรุปการประชุมจากไฟล์เสียง ฟรี!')
st.text("Application สำหรับสรุปการประชุมจากไฟล์เสียง")
st.sidebar.markdown("""# About US""")
st.sidebar.markdown("""## สร้างโดยทีมงาน #AI \n\n #AI for people \n\nเพจที่รวบรวมข่าวสารที่เกี่ยวข้อง และแชร์เทคนิคๆ ต่างของ AI""")
st.sidebar.markdown("## สามารถติดตามเราได้ที่ \n\n **[Facbook Page #AI](https://www.facebook.com/profile.php?id=61560597801592)** ")
st.sidebar.image('logo.png', width=100)  
st.sidebar.title('การตั้งค่า')
api_key = st.sidebar.text_input("Enter your API key")
st.sidebar.text("ไม่มี API Key หรอ?")
st.sidebar.markdown("[สามารถรับ API_KEY ได้ที่นี่]( https://aistudio.google.com/app/apikey)")
st.sidebar.markdown("สามารถใช้งานได้ฟรี และไม่มีค่าใช้จ่ายเพิ่มเติม \nโดยใช้ API_KEY ของ Google AI Studio ในการใช้งาน \n\n")
if not api_key:
    st.warning("กรุณากรอก API Key ก่อนใช้งาน")
API_KEY(api_key)
audio_file = st.file_uploader("Upload Audio File", type=["wav", "mp3", "ogg", "flac", "m4a"])
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)
    st.audio(audio_path)

    if st.button('Process Audio'):
        with st.spinner('Processing...'):
            processed_text = process_audio(audio_path)
            st.text_area("Processed Output", processed_text, height=500)