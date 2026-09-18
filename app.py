import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import os
from io import BytesIO

# 1. إعداد الصفحة - لازم يكون أول شي
st.set_page_config(
    page_title="Waddah Heaparavendise",
    page_icon="W.png",
    layout="wide"
)

# 2. إخفاء شعار و هوية Streamlit نهائياً
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important; display: none !important;}
    header {visibility: hidden !important; display: none !important;}
    footer {visibility: hidden !important; display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important;}
    div[data-testid="stStatusWidget"] {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    </style>
""", unsafe_allow_html=True)

# 3. الشعار العلوي
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)
elif os.path.exists("W.png"):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("W.png", width=120)

st.markdown("<h3 style='text-align: center; color: #FFD700;'>✨ Waddah Heaparavendise ✨</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>النظام المطور لتحسين الصور بدقة فائقة</p>", unsafe_allow_html=True)
st.divider()

st.header("📥 مصدر الصورة")
source = st.radio("اختر:", ["رفع من الاستوديو", "التقاط بالكاميرا"], horizontal=True, label_visibility="collapsed")

uploaded_file = None
if source == "رفع من الاستوديو":
    uploaded_file = st.file_uploader("اختر صورة", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
else:
    uploaded_file = st.camera_input("التقط صورة", label_visibility="collapsed")

st.header("🎛️ التحكم")
col_a, col_b = st.columns(2)
with col_a:
    contrast = st.slider("التباين", 0.5, 5.0, 1.2, 0.1)
with col_b:
    sharpness = st.slider("الحدة", 0.0, 5.0, 1.5, 0.1)
denoise = st.slider("التنعيم", 0.0, 15.0, 2.0, 0.5)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_enhanced = ImageEnhance.Contrast(image).enhance(contrast)
    img_enhanced = ImageEnhance.Sharpness(img_enhanced).enhance(sharpness)
    if denoise > 0:
        img_enhanced = img_enhanced.filter(ImageFilter.GaussianBlur(radius=denoise/10.0))
    
    st.header("🖥️ المعاينة")
    st.image(img_enhanced, caption="Waddah Heaparavendise - النتيجة", use_container_width=True)
    
    buf = BytesIO()
    img_enhanced.save(buf, format="PNG")
    
    st.download_button(
        label="💾 تحميل الصورة المحسنة", 
        data=buf.getvalue(), 
        file_name="waddah_enhanced.png", 
        mime="image/png", 
        use_container_width=True, 
        type="primary"
    )
else:
    st.info("👆 ارفع صورة من فوق عشان نبدأ")

st.markdown("<br><br><p style='text-align: center; color: #333; font-size: 0.8rem;'>© 2026 Waddah Heaparavendise - All Rights Reserved</p>", unsafe_allow_html=True)
