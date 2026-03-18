import streamlit as st
from transcript import get_transcript
from quotes import detect_meaningful_quotes, save_quotes_to_file
from utils import extract_video_id, format_transcript_display

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Transcriber & Quote Extractor",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 YouTube Transcriber & Quote Extractor")
st.markdown("Paste a YouTube URL to fetch its transcript, search keywords, and extract quotes.")

# ── Session state setup ───────────────────────────────────────────────────────
if "transcript" not in st.session_state:
    st.session_state.transcript = []          # list of {start, text} dicts
if "saved_quotes" not in st.session_state:
    st.session_state.saved_quotes = []        # list of quote strings
if "video_id" not in st.session_state:
    st.session_state.video_id = ""

# ── Sidebar: saved quotes ─────────────────────────────────────────────────────
with st.sidebar:
    st.header("📌 Saved Quotes")
    if st.session_state.saved_quotes:
        for i, quote in enumerate(st.session_state.saved_quotes):
            st.markdown(f"> {quote}")
            if st.button(f"❌ Remove", key=f"remove_{i}"):
                st.session_state.saved_quotes.pop(i)
                st.rerun()

        # Export buttons
        st.divider()
        quotes_text = "\n\n".join(
            [f"• {q}" for q in st.session_state.saved_quotes]
        )
        st.download_button(
            label="💾 Save as .txt",
            data=quotes_text,
            file_name="saved_quotes.txt",
            mime="text/plain",
        )
        st.text_area("📋 Copy from here", value=quotes_text, height=150)
    else:
        st.info("No quotes saved yet.")

# ── Main area ─────────────────────────────────────────────────────────────────
url = st.text_input("🔗 YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
col1, col2 = st.columns([1, 4])

with col1:
    fetch_btn = st.button("🚀 Get Transcript", type="primary")

# ── Fetch transcript ──────────────────────────────────────────────────────────
if fetch_btn:
    if not url.strip():
        st.warning("Please enter a YouTube URL.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("❌ Invalid YouTube URL. Please check and try again.")
        else:
            with st.spinner("Fetching transcript… this may take a moment."):
                transcript, method, error = get_transcript(url)

            if error:
                st.error(f"❌ {error}")
            else:
                st.session_state.transcript = transcript
                st.session_state.video_id = video_id
                st.success(f"✅ Transcript fetched via **{method}**.")

# ── Display transcript ────────────────────────────────────────────────────────
if st.session_state.transcript:
    st.divider()
    st.subheader("📄 Transcript")

    # Search bar
    keyword = st.text_input("🔍 Search keyword in transcript", "")

    # Render transcript lines
    transcript_lines = format_transcript_display(st.session_state.transcript)

    for entry in transcript_lines:
        timestamp = entry["timestamp"]
        text      = entry["text"]

        # Highlight keyword matches
        highlight = keyword.strip().lower() in text.lower() if keyword.strip() else False
        bg = "#fff3cd" if highlight else "transparent"

        col_ts, col_txt, col_btn = st.columns([1, 7, 2])
        with col_ts:
            st.markdown(
                f"<span style='color:gray; font-size:0.85em;'>{timestamp}</span>",
                unsafe_allow_html=True,
            )
        with col_txt:
            st.markdown(
                f"<div style='background:{bg}; padding:2px 6px; border-radius:4px;'>{text}</div>",
                unsafe_allow_html=True,
            )
        with col_btn:
            if st.button("💬 Save", key=f"save_{timestamp}_{text[:10]}"):
                quote = f"[{timestamp}] {text}"
                if quote not in st.session_state.saved_quotes:
                    st.session_state.saved_quotes.append(quote)
                    st.toast("Quote saved!")

    # ── Auto quote detection ──────────────────────────────────────────────────
    st.divider()
    st.subheader("✨ Auto-Detected Meaningful Quotes")
    if st.button("🤖 Detect Meaningful Quotes"):
        meaningful = detect_meaningful_quotes(st.session_state.transcript)
        if meaningful:
            for entry in meaningful:
                ts   = entry["timestamp"]
                text = entry["text"]
                c1, c2 = st.columns([8, 2])
                with c1:
                    st.markdown(f"> **[{ts}]** {text}")
                with c2:
                    if st.button("💾 Save", key=f"auto_{ts}"):
                        quote = f"[{ts}] {text}"
                        if quote not in st.session_state.saved_quotes:
                            st.session_state.saved_quotes.append(quote)
                            st.toast("Quote saved!")
        else:
            st.info("No particularly meaningful quotes detected.")
