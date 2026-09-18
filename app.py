import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import os
from io import BytesIO

st.set_page_config(page_title="Heaparavendise Enhancer", page_icon="logo.png", layout="centered")

if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #FFD700;'>✨ Heaparavendise photo enhancer ✨</h3>", unsafe_allow_html=True)
st.divider()

st.header("📥 مصدر الصورة")
source = st.radio("اختر:", ["رفع من الاستوديو", "التقاط بالكاميرا"], horizontal=True)

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
    st.image(img_enhanced, caption="Heaparavendise - النتيجة", use_container_width=True)
    buf = BytesIO()
    img_enhanced.save(buf, format="PNG")
    st.download_button(label="💾 تحميل الصورة المحسنة", data=buf.getvalue(), file_name="heaparavendise_enhanced.png", mime="image/png", use_container_width=True, type="primary")
else:
    st.info("👆 ارفع صورة من فوق عشان نبدأ")
