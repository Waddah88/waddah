import cv2
import numpy as np
import streamlit as st
from PIL import Image
st.set_page_config(page_title="Heaparavendise Enhancer", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
#MainMenu, header, footer, div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"], .stDeployButton, button[kind="header"], [data-testid="stHeader"] {visibility: hidden !important; display: none !important;}
.viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_ {display: none !important;}
.block-container {padding-top: 1rem !important;}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>✨ Heaparavendise Enhancer ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>النظام المطور لتصفية، معالجة، وتحسين جودة الصور بدقة فائقة</p>", unsafe_allow_html=True)
def enhance_image(input_rgb, contrast_level, noise_level, sharp_level):
    if input_rgb is None: return None
    img_bgr = cv2.cvtColor(input_rgb, cv2.COLOR_RGB2BGR)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=float(contrast_level), tileGridSize=(8,8))
    cl = clahe.apply(l)
    img_contrast = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)
    if noise_level > 0:
        img_denoised = cv2.fastNlMeansDenoisingColored(img_contrast, None, int(noise_level), int(noise_level), 7, 21)
    else:
        img_denoised = img_contrast
    if sharp_level > 0:
        blurred = cv2.GaussianBlur(img_denoised, (0, 0), 3)
        img_sharp = cv2.addWeighted(img_denoised, 1.0 + float(sharp_level), blurred, -float(sharp_level), 0)
    else:
        img_sharp = img_denoised
    return cv2.cvtColor(img_sharp, cv2.COLOR_BGR2RGB)
col1, col2 = st.columns([1, 1.5], gap="large")
with col1:
    st.markdown("### 📥 مصدر الصورة")
    source = st.radio("اختر:", ("رفع من الاستوديو", "التقاط بالكاميرا"), horizontal=True)
    uploaded_file = None
    if source == "رفع من الاستوديو":
        uploaded_file = st.file_uploader("اختر صورة:", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    else:
        uploaded_file = st.camera_input("التقط:", label_visibility="collapsed")
    st.markdown("### 🎛 التحكم")
    contrast = st.slider("التباين", 0.0, 10.0, 2.5, 0.1)
    noise = st.slider("التشويش", 0.0, 30.0, 10.0, 1.0)
    sharp = st.slider("الحدة", 0.0, 5.0, 1.2, 0.1)
with col2:
    st.markdown("### 🖥 المعاينة")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        file_bytes = np.frombuffer(bytes_data, np.uint8)
        img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        result = enhance_image(img_rgb, contrast, noise, sharp)
        st.image(result, caption="Heaparavendise - النتيجة", use_container_width=True)
        _, buffer = cv2.imencode('.jpg', cv2.cvtColor(result, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 95])
        st.download_button("💾 تحميل الصورة المحسنة", data=buffer.tobytes(), file_name="Heaparavendise_Enhanced.jpg", mime="image/jpeg", use_container_width=True, type="primary")
    else:
        st.info("💡 ارفع صورة لبدء المعالجة.")
