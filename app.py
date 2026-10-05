import streamlit as st
import google.generativeai as genai
from PIL import Image

# পেজের টাইটেল
st.set_page_config(page_title="AI Trading Signal", layout="centered")
st.title("📊 AI Trading Signal Prototype (Free)")
st.write("৪টি টাইমফ্রেমের চার্ট আপলোড করুন। এআই বিশ্লেষণ করে সিগন্যাল দেবে।")
st.warning("⚠️ সতর্কতা: এটি শুধুমাত্র শিক্ষামূলক। ট্রেডিংয়ে ঝুঁকি রয়েছে।")

# এপিআই কী লোড করা (Streamlit Secrets থেকে)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key সেট করা হয়নি। Settings -> Secrets এ GEMINI_API_KEY যোগ করুন।")
    st.stop()

# ৪টি ছবি আপলোডের বক্স
img1 = st.file_uploader("Timeframe 1 (যেমন: 15m)", type=["jpg", "jpeg", "png"])
img2 = st.file_uploader("Timeframe 2 (যেমন: 1H)", type=["jpg", "jpeg", "png"])
img3 = st.file_uploader("Timeframe 3 (যেমন: 4H)", type=["jpg", "jpeg", "png"])
img4 = st.file_uploader("Timeframe 4 (যেমন: 1D)", type=["jpg", "jpeg", "png"])

# অ্যানালাইসিস বাটন
if st.button("🚀 Analyze & Generate Signal", use_container_width=True):
    if img1 and img2 and img3 and img4:
        with st.spinner("এআই চার্টগুলো বিশ্লেষণ করছে... অপেক্ষা করুন..."):
            
            # ছবিগুলোকে PIL ইমেজে রূপান্তর করা (Gemini এর জন্য)
            image1 = Image.open(img1)
            image2 = Image.open(img2)
            image3 = Image.open(img3)
            image4 = Image.open(img4)

            prompt = """
            You are an expert Forex, Crypto, and Binary Options trader. 
            I am providing you with 4 chart screenshots of the same asset across different timeframes.
            Analyze all 4 charts together. Identify the overall trend, support, and resistance levels.
            
            Based on the confluence of these 4 timeframes, provide the following in a clean format:
            1. Asset Name (if visible)
            2. Overall Trend
            3. Confluence Analysis
            4. Final Signal: BUY, SELL, or NO TRADE. (If charts are conflicting or unclear, strictly say NO TRADE).
            5. Confidence Score: High, Medium, or Low.
            6. Suggested Entry Price, Stop Loss (SL), and Take Profit (TP).
            
            Remember, risk management is crucial. If it's too risky, say NO TRADE.
            """

            try:
                # Gemini 1.5 Flash মডেল ব্যবহার (ফ্রি এবং ফাস্ট)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # এপিআই-তে প্রম্পট এবং ৪টি ছবি একসাথে পাঠানো
                response = model.generate_content([prompt, image1, image2, image3, image4])
                
                st.success("✅ বিশ্লেষণ সম্পন্ন!")
                st.markdown("### 📋 AI Signal Prototype")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")
    else:
        st.error("অনুগ্রহ করে ৪টি ছবিই আপলোড করুন।")
