import streamlit as st
from PIL import Image, ImageOps
import io

# Page Setup
st.set_page_config(page_title="Digital Cafe Tool", layout="centered")
st.title("🖨️ Professional ID & Passport Tool")
st.info("Aadhar, PAN aur Passport photo ko perfect size mein set karein.")

# Sidebar Settings
st.sidebar.header("Configuration")
pass_count = st.sidebar.slider("Passport Photos Kitni Chahiye?", 1, 15, 5)
dpi = 300

def get_px(mm):
    return int((mm * dpi) / 25.4)

# File Uploaders
col1, col2 = st.columns(2)
with col1:
    front_file = st.file_uploader("Upload ID Front (JPG/PNG)", type=['jpg', 'png', 'jpeg'])
with col2:
    back_file = st.file_uploader("Upload ID Back (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

pass_file = st.file_uploader("Upload Passport Size Photo", type=['jpg', 'png', 'jpeg'])

if st.button("PREPARE PRINTABLE PDF"):
    if (front_file and back_file) or pass_file:
        with st.spinner("Processing..."):
            # A4 Sheet (210x297mm)
            sheet = Image.new('RGB', (get_px(210), get_px(297)), 'white')
            curr_y = 200

            # 1. ID Processing (Standard 85.6 x 54 mm)
            if front_file and back_file:
                f_img = Image.open(front_file).resize((get_px(85.6), get_px(54)), Image.LANCZOS)
                b_img = Image.open(back_file).resize((get_px(85.6), get_px(54)), Image.LANCZOS)
                
                f_img = ImageOps.expand(f_img, border=2, fill='black')
                b_img = ImageOps.expand(b_img, border=2, fill='black')

                sheet.paste(f_img, (200, curr_y))
                sheet.paste(b_img, (200 + f_img.width + 50, curr_y))
                curr_y += f_img.height + 300

            # 2. Passport Processing (Standard 35 x 45 mm)
            if pass_file:
                p_img = Image.open(pass_file).resize((get_px(35), get_px(45)), Image.LANCZOS)
                p_img = ImageOps.expand(p_img, border=2, fill='black')
                
                for i in range(pass_count):
                    x_pos = 200 + (i % 5 * (p_img.width + 40))
                    y_pos = curr_y + (i // 5 * (p_img.height + 40))
                    sheet.paste(p_img, (x_pos, y_pos))

            # PDF Buffer
            pdf_buf = io.BytesIO()
            sheet.save(pdf_buf, format="PDF", resolution=300)
            
            st.success("PDF Taiyar Hai!")
            st.download_button(
                label="📥 Download Ready PDF",
                data=pdf_buf.getvalue(),
                file_name="Digital_Cafe_Print.pdf",
                mime="application/pdf"
            )
    else:
        st.error("Kripya files upload karein!")
