import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_URL = "https://text-sumtrans-api-1074853720579.asia-south1.run.app"
st.set_page_config(page_title="AI Text Summarizer", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<div style="background: linear-gradient(90deg, #4CAF50, #008080); padding: 20px; border-radius: 15px; text-align:center;">
    <h1 style='color:white; margin-bottom:5px;'>🧠 AI Text Summarizer</h1>
    <p style='color:#f0f0f0;'>Summarize text instantly and view it in English or Hindi.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- STYLE ----------------
st.markdown("""
<style>
/* Buttons (green gradient) */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #0078D7, #005A9E);
    color: white;
    border: none;
    padding: 0.7em 2em;
    font-size: 16px;
    border-radius: 10px;
    transition: all 0.3s ease;
    font-weight:bold;
}
div.stButton > button:first-child:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #0080FF, #0060B5);
}

/* Input Text Area */
textarea {
    border: 2px solid #00FFAA !important;  /* same green as output */
    border-radius: 10px !important;
    background-color: #121212 !important;
    color: #ffffff !important;
    padding: 10px !important;
    font-size:16px !important;
    transition: all 0.3s ease;
}
textarea:focus {
    border-color: #00FFAA !important;  /* keep focus same green */
    box-shadow: 0 0 10px #00FFAA;
}

/* Scrollable Output Box (black) */
.scroll-box {
    background-color: #000;
    color: #00FFAA;
    border: 2px solid #00FFAA;  /* same green border */
    border-radius: 15px;
    padding: 20px;
    overflow-y: auto;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    line-height: 1.6;
}
.scroll-box::-webkit-scrollbar {
    width: 8px;
}
.scroll-box::-webkit-scrollbar-thumb {
    background-color: #555;
    border-radius: 4px;
}

/* Radio Buttons */
[data-baseweb="radio"] > div {
    display: flex;
    gap: 15px;
}
div.row-widget.stRadio > label {
    color: #00FFAA;
    font-weight: bold;
}
div.row-widget.stRadio > label:hover {
    color: #00FF00;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "translated" not in st.session_state:
    st.session_state.translated = ""
if "current_lang" not in st.session_state:
    st.session_state.current_lang = "English"
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2, gap="large")

# Left Input Column
with col1:
    st.markdown("### ✍️ Input Text")
    input_text = st.text_area(
        "Input Text",
        placeholder="Paste or type your text here...",
        height=420,
        label_visibility="hidden"
    )

    # Reset output to English if new input is typed
    if input_text != st.session_state.input_text:
        st.session_state.translated = ""
        st.session_state.current_lang = "English"

    st.session_state.input_text = input_text

    length_category = st.radio(
        "Summary Length",
        ["short", "medium", "long"],
        horizontal=True,
        label_visibility="hidden"
    )

    summarize_click = st.button("🚀 Summarize Text", use_container_width=True)

# Right Output Column
with col2:
    lang_choice = st.radio(
        "Output Language",
        ["English", "Hindi"],
        horizontal=True,
        label_visibility="hidden"
    )

    display_text = (
        st.session_state.translated
        if lang_choice == "Hindi" and st.session_state.translated
        else st.session_state.summary or "Your summarized text will appear here..."
    )

    st.markdown(
        f"<div class='scroll-box' style='height:420px'>{display_text}</div>",
        unsafe_allow_html=True
    )

# ---------------- LOGIC ----------------
if summarize_click:
    if not st.session_state.input_text.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        try:
            with st.spinner("🧠 Summarizing..."):
                res = requests.post(
                    f"{API_URL}/predict",
                    params={
                        "text": st.session_state.input_text,
                        "length_category": length_category
                    }
                )
            if res.status_code == 200:
                st.session_state.summary = res.json().get("summary", "")
                st.session_state.translated = ""
                st.session_state.current_lang = "English"
                st.rerun()
            else:
                st.error("❌ Summarization failed.")
        except Exception as e:
            st.error(f"🔥 Error: {e}")

# ---------------- TRANSLATION ----------------
if lang_choice == "Hindi" and st.session_state.summary and not st.session_state.translated:
    try:
        with st.spinner("🌐 Translating to Hindi..."):
            trans_res = requests.post(
                f"{API_URL}/translate",
                params={"text": st.session_state.summary}
            )
        if trans_res.status_code == 200:
            st.session_state.translated = trans_res.json().get("translated_text", "")
            st.session_state.current_lang = "Hindi"
            st.rerun()
    except Exception as e:
        st.error(f"⚠️ Translation Error: {e}")
