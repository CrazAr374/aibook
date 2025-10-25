import streamlit as st
import requests
import json
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="BookForge AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Page and container */
    body, .stApp, .block-container {
        background-color: #0b1220 !important;
        color: #e6eef8 !important;
    }

    /* Header */
    .header { text-align: center; margin-bottom: 36px; padding-bottom: 16px; border-bottom: 1px solid rgba(255,255,255,0.04); }
    .header h1 { font-size: 38px; margin: 0; color: #ffffff; font-weight: 700; }
    .header p { font-size: 14px; color: #bcd3f5; margin: 8px 0 0 0; }

    /* Section card */
    .section-box { background: #0f1724; border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 22px; margin: 18px 0; }
    .section-box h2 { color: #e6eef8; }

    /* Message boxes */
    .info-box { background: rgba(59,130,246,0.08); border-left: 4px solid #3b82f6; padding: 12px 14px; border-radius: 6px; color: #cfe3ff; }
    .success-box { background: rgba(34,197,94,0.06); border-left: 4px solid #16a34a; padding: 12px 14px; border-radius: 6px; color: #bbf1d0; }
    .error-box { background: rgba(239,68,68,0.06); border-left: 4px solid #ef4444; padding: 12px 14px; border-radius: 6px; color: #ffc9c9; }

    /* Buttons */
    .stButton > button {
        height: 44px;
        font-weight: 600;
        border-radius: 8px;
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover { background-color: #1d4ed8 !important; }

    /* Inputs (light adjustments) */
    textarea, input, .stTextArea, .stTextInput {
        background-color: #071025 !important;
        color: #e6eef8 !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid rgba(255,255,255,0.04); }
    .stTabs [data-baseweb="tab"] { padding: 12px 18px; color: #9fb9ff; }
    .stTabs [aria-selected="true"] { color: #ffffff; border-bottom: 3px solid #2563eb; }

    /* Small footer */
    .footer { color: #9aa9bf; font-size: 12px; }
    
    /* Responsive adjustments */
    .block-container { max-width: 1100px; margin: 0 auto; padding-left: 16px; padding-right: 16px; }
    @media (max-width: 900px) {
        .stColumns { gap: 12px; }
        .stCols { gap: 12px; }
        .section-box { padding: 16px; }
        .header h1 { font-size: 28px; }
        .header p { font-size: 13px; }
        .stButton > button { width: 100% !important; }
        .stTextInput, .stTextArea { width: 100% !important; }
        .stTabs [data-baseweb="tab"] { padding: 10px 12px; font-size: 14px; }
    }

    @media (max-width: 420px) {
        .header h1 { font-size: 22px; }
        .section-box { padding: 12px; }
        .section-box h2 { font-size: 16px; }
        .stButton > button { height: 44px; font-size: 14px; }
    }
</style>
""", unsafe_allow_html=True)

if "outline_data" not in st.session_state: st.session_state.outline_data = None
if "book_data" not in st.session_state: st.session_state.book_data = None
if "current_topic" not in st.session_state: st.session_state.current_topic = ""

st.markdown("<div class='header'><h1>BookForge AI</h1><p>Professional Book Generation Powered by AI</p></div>", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input("Your Book Topic", placeholder="e.g., The Future of AI", value=st.session_state.current_topic, label_visibility="collapsed")
    st.session_state.current_topic = topic
with col2:
    if st.button("Reset", use_container_width=True, key="reset_btn"):
        st.session_state.outline_data = None
        st.session_state.book_data = None
        st.session_state.current_topic = ""
        st.rerun()

WRITING_STYLES = {
    "informative": "Factual, data-driven",
    "narrative": "Story-driven",
    "educational": "Progressive learning",
    "self-help": "Practical guidance",
    "fiction": "Creative storytelling",
    "technical": "Implementation details",
    "business": "Strategic insights",
    "inspirational": "Personal growth",
    "research": "Academic rigor",
    "lifestyle": "Wellness focused"
}

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Step 1: Create Outline", "Step 2: Edit Outline", "Step 3: Generate Book", "Step 4: Edit Book", "Step 5: Export"])

with tab1:
    st.markdown("<div class='section-box'><h2>Create Your Book Outline</h2></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Select Writing Style**")
        outline_style = st.selectbox("Outline Style", list(WRITING_STYLES.keys()), format_func=lambda x: f"{x.title()} - {WRITING_STYLES[x]}", label_visibility="collapsed")
    with col2:
        if st.button("Generate Outline (8 Chapters)", use_container_width=True, key="generate_outline_btn"):
            if not topic or topic.strip() == "": 
                st.markdown("<div class='error-box'>Please enter a book topic first.</div>", unsafe_allow_html=True)
            else:
                with st.spinner("Generating outline..."):
                    try:
                        resp = requests.post(f"{BACKEND_URL}/generate_outline", json={"topic": topic, "outline_style": outline_style}, timeout=120)
                        if resp.status_code == 200:
                            st.session_state.outline_data = resp.json().get("outline")
                            st.markdown("<div class='success-box'>Outline generated successfully!</div>", unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown(f"<div class='error-box'>Error: {resp.json().get('detail', 'Unknown error')}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)
    
    if st.session_state.outline_data:
        st.markdown("<div class='section-box'><h2>Your Outline</h2></div>", unsafe_allow_html=True)
        outline = st.session_state.outline_data
        st.write(f"**Title:** {outline.get('title', 'Untitled')}")
        st.write(f"**Chapters:** {len(outline.get('chapters', []))}")
        for chapter in outline.get("chapters", []):
            with st.expander(f"Chapter {chapter.get('chapter_number')}: {chapter.get('title')}"):
                for i, section in enumerate(chapter.get("sections", []), 1):
                    st.write(f"{i}. {section}")

with tab2:
    if st.session_state.outline_data:
        st.markdown("<div class='section-box'><h2>Edit Your Outline</h2></div>", unsafe_allow_html=True)
        outline = st.session_state.outline_data
        new_title = st.text_input("Book Title", value=outline.get("title", ""), label_visibility="collapsed")
        if new_title and new_title != outline.get("title", ""):
            outline["title"] = new_title
        st.write("---")
        st.write("**Edit Chapters**")
        for idx, chapter in enumerate(outline.get("chapters", [])):
            with st.expander(f"Chapter {chapter.get('chapter_number')}: {chapter.get('title')}"):
                new_ch_title = st.text_input(f"Chapter {idx + 1} Title", value=chapter.get("title", ""), key=f"ch_{idx}", label_visibility="collapsed")
                if new_ch_title and new_ch_title != chapter.get("title", ""):
                    chapter["title"] = new_ch_title
                st.write("Sections:")
                for sec_idx, section in enumerate(chapter.get("sections", [])):
                    new_sec = st.text_input(f"Section {sec_idx + 1}", value=section, key=f"sec_{idx}_{sec_idx}", label_visibility="collapsed")
                    if new_sec != section:
                        chapter["sections"][sec_idx] = new_sec
        if st.button("Save Changes", use_container_width=True, key="save_outline_btn"):
            st.session_state.outline_data = outline
            st.markdown("<div class='success-box'>Outline saved successfully!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>Generate an outline first in Step 1.</div>", unsafe_allow_html=True)

with tab3:
    if st.session_state.outline_data:
        st.markdown("<div class='section-box'><h2>Generate Full Book Content</h2></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Select Writing Style**")
            book_style = st.selectbox("Book Style", list(WRITING_STYLES.keys()), format_func=lambda x: f"{x.title()} - {WRITING_STYLES[x]}", label_visibility="collapsed")
        with col2:
            if st.button("Generate Book (8 Chapters, 1200-1500 words each)", use_container_width=True, key="generate_book_btn"):
                with st.spinner("Generating book... This will take 3-5 minutes"):
                    try:
                        resp = requests.post(f"{BACKEND_URL}/generate_book", json={"outline": st.session_state.outline_data, "book_style": book_style}, timeout=600)
                        if resp.status_code == 200:
                            st.session_state.book_data = resp.json().get("book")
                            st.markdown("<div class='success-box'>Book generated successfully!</div>", unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown(f"<div class='error-box'>Error: {resp.json().get('detail', 'Unknown error')}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)
        
        if st.session_state.book_data:
            st.markdown("<div class='section-box'><h2>Book Preview</h2></div>", unsafe_allow_html=True)
            book = st.session_state.book_data
            st.write(f"**Title:** {book.get('title', 'Untitled')}")
            st.write(f"**Author:** {book.get('author', 'Unknown')}")
            st.write(f"**Chapters:** {len(book.get('chapters', []))}")
            for chapter in book.get("chapters", []):
                with st.expander(f"Chapter {chapter.get('chapter_number')}: {chapter.get('title')}"):
                    content = chapter.get("content", "")
                    preview = content[:400] + "..." if len(content) > 400 else content
                    st.write(preview)
    else:
        st.markdown("<div class='info-box'>Generate an outline first in Step 1.</div>", unsafe_allow_html=True)

with tab4:
    if st.session_state.book_data:
        st.markdown("<div class='section-box'><h2>Edit Book Content</h2></div>", unsafe_allow_html=True)
        book = st.session_state.book_data
        chapters = book.get("chapters", [])
        chapter_opts = {f"Chapter {ch['chapter_number']}: {ch['title']}": ch['chapter_number'] for ch in chapters}
        selected = st.selectbox("Select Chapter to Edit", list(chapter_opts.keys()), label_visibility="collapsed")
        if selected:
            ch_num = chapter_opts[selected]
            current = next((ch for ch in chapters if ch['chapter_number'] == ch_num), None)
            if current:
                st.write(f"### Editing: {current.get('title')}")
                edited = st.text_area("Chapter Content", value=current.get("content", ""), height=350, label_visibility="collapsed")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Changes", use_container_width=True, key="save_chapter_btn"):
                        try:
                            resp = requests.post(f"{BACKEND_URL}/edit_chapter", json={"book": book, "chapter_number": ch_num, "new_content": edited}, timeout=30)
                            if resp.status_code == 200:
                                st.session_state.book_data = resp.json().get("book")
                                st.markdown("<div class='success-box'>Changes saved!</div>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)
                with col2:
                    if st.button("Discard", use_container_width=True, key="discard_changes_btn"):
                        st.markdown("<div class='info-box'>Discarded</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>Generate book content in Step 3 first.</div>", unsafe_allow_html=True)

with tab5:
    if st.session_state.book_data:
        st.markdown("<div class='section-box'><h2>Export Your Book</h2></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fmt = st.selectbox("Select Export Format", ["docx", "pdf"], label_visibility="collapsed")
        with col2:
            if st.button("Export Book", use_container_width=True, key="export_book_btn"):
                with st.spinner(f"Exporting as {fmt.upper()}..."):
                    try:
                        resp = requests.post(f"{BACKEND_URL}/export_book", json={"book": st.session_state.book_data, "format": fmt}, timeout=60)
                        if resp.status_code == 200:
                            filename = f"bookforge_{st.session_state.book_data.get('title', 'book').replace(' ', '_')}.{fmt}"
                            mime_type = "application/pdf" if fmt == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            st.markdown("<div class='success-box'>Book exported!</div>", unsafe_allow_html=True)
                            st.download_button(f"Download {fmt.upper()}", resp.content, filename, mime_type, use_container_width=True)
                        else:
                            st.markdown(f"<div class='error-box'>Error: {resp.json().get('detail', 'Unknown error')}</div>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<div class='error-box'>Error: {str(e)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='info-box'>Generate book content in Step 3 first.</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p class='footer' style='text-align:center; margin-top: 20px;'>BookForge AI | Powered by Gemini</p>", unsafe_allow_html=True)
