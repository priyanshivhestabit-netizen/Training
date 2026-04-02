import streamlit as st
import requests
import tempfile
import os
from PIL import Image

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Advanced RAG", page_icon="🧠", layout="wide")
st.title("🧠 Advanced RAG")
st.caption("Text RAG · Image RAG · SQL QA — Powered by Mistral (local)")

#Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.radio("Mode", ["📄 Text RAG (/ask)",
                              "🖼️ Image RAG (/ask-image)",
                              "🗄️ SQL QA (/ask-sql)"])
    top_k = st.slider("Top-K results", 1, 10, 3)

    st.divider()
    if st.button("🗑️ Clear Memory"):
        try:
            requests.delete(f"{API_URL}/memory")
            st.success("Memory cleared!")
        except Exception:
            st.error("Could not connect to API.")

    st.divider()
    st.subheader("💬 Conversation Memory")
    try:
        mem = requests.get(f"{API_URL}/memory").json()
        for entry in mem.get("history", [])[-6:]:
            role_icon = "🧑" if entry["role"] == "user" else "🤖"
            st.caption(f"{role_icon} **{entry['role']}** [{entry['endpoint']}]")
            st.caption(entry["content"][:120] + "...")
            st.divider()
    except Exception:
        st.caption("API not running.")

# Chat history in session 
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "images" in msg:
            for img in msg["images"]:
                st.image(img,width=200)

# image-rag - 3 submodels
if "Image RAG (/ask-image)" in mode:
    st.divider()
    st.subheader("🖼️ Image RAG — Choose Sub-Mode")
    img_mode = st.radio(
        "Image Query Mode",
        ["📝 Text → Image", "🖼️ Image → Image", "🔍 Image → Text"],
        horizontal=True
    )
 
    # ── SUB-MODE 1: Text → Image ─────────────────────────────────────────────
    if "Text → Image" in img_mode:
        st.caption("Type a text query → system finds matching images")
        query = st.text_input("Enter text query:", placeholder="e.g. bar chart, invoice, policy document")
 
        if st.button("🔍 Search Images", key="txt2img"):
            if not query.strip():
                st.warning("Please enter a query.")
            else:
                with st.spinner("Searching images..."):
                    try:
                        res = requests.post(f"{API_URL}/ask-image",
                                            json={"query": query, "k": top_k}).json()
 
                        st.success(f"Found {len(res.get('images', []))} images")
 
                        # Show answer
                        st.markdown(f"**Answer:** {res.get('answer', 'No answer.')}")
 
                        # Show matched images
                        if res.get("images"):
                            st.subheader("📷 Matched Images")
                            cols = st.columns(min(len(res["images"]), 3))
                            for i, img_info in enumerate(res["images"]):
                                with cols[i % 3]:
                                    img_path = f"src/data/images/{img_info['source']}"
                                    if os.path.exists(img_path):
                                        st.image(img_path, caption=img_info["caption"], use_column_width=True)
                                    else:
                                        st.caption(f"📄 {img_info['source']}")
                                        st.caption(f"Caption: {img_info['caption']}")
 
                        # Evaluation
                        with st.expander("📊 Evaluation"):
                            ev = res.get("evaluation", {})
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Confidence",    f"{ev.get('confidence_pct', 0)}%")
                            c2.metric("Faithfulness",  ev.get('faithfulness_score', 0))
                            c3.metric("Hallucination", ev.get('hallucination_label', 'N/A'))
 
                        # Save to chat history
                        st.session_state.messages.append({"role": "user",      "content": f"[Text→Image] {query}"})
                        st.session_state.messages.append({"role": "assistant", "content": res.get("answer", "")})
 
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API.")
 
    # ── SUB-MODE 2: Image → Image ────────────────────────────────────────────
    elif "Image → Image" in img_mode:
        st.caption("Upload an image → system finds visually similar images")
        uploaded = st.file_uploader("Upload a query image", type=["png", "jpg", "jpeg"], key="img2img_upload")
 
        if uploaded and st.button("🔍 Find Similar Images", key="img2img"):
            with st.spinner("Finding similar images..."):
                try:
                    # Save uploaded file to temp location
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(uploaded.read())
                        tmp_path = tmp.name
 
                    # Show uploaded image
                    st.subheader("📤 Your Query Image")
                    st.image(tmp_path, width=300, caption="Uploaded image")
 
                    # Call API
                    res = requests.post(
                        f"{API_URL}/image-to-image",
                        json={"image_path": tmp_path, "k": top_k}
                    ).json()
 
                    similar = res.get("similar_images", [])
 
                    if not similar:
                        st.info("No similar images found. Add more images to src/data/images/")
                    else:
                        st.subheader(f"🖼️ Top {len(similar)} Similar Images")
                        cols = st.columns(min(len(similar), 3))
                        for i, img_info in enumerate(similar):
                            with cols[i % 3]:
                                img_path = f"src/data/images/{img_info['source']}"
                                if os.path.exists(img_path):
                                    st.image(img_path, caption=img_info["caption"], use_column_width=True)
                                else:
                                    st.caption(f"📄 {img_info['source']}")
                                    st.caption(img_info["caption"])
 
                    os.unlink(tmp_path)
 
                    st.session_state.messages.append({"role": "user",      "content": "[Image→Image] Uploaded image for similarity search"})
                    st.session_state.messages.append({"role": "assistant", "content": f"Found {len(similar)} similar images."})
 
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API.")
 
    # ── SUB-MODE 3: Image → Text ──────────────────────────────────────────────
    elif "Image → Text" in img_mode:
        st.caption("Upload an image → system extracts OCR text + caption + summary")
        uploaded = st.file_uploader("Upload an image to analyze", type=["png", "jpg", "jpeg"], key="img2txt_upload")
 
        if uploaded and st.button("🔍 Analyze Image", key="img2txt"):
            with st.spinner("Analyzing image..."):
                try:
                    # Save uploaded file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        tmp.write(uploaded.read())
                        tmp_path = tmp.name
 
                    # Show uploaded image
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.subheader("📤 Uploaded Image")
                        st.image(tmp_path, use_column_width=True)
 
                    # Call API
                    res = requests.post(
                        f"{API_URL}/image-to-text",
                        json={"image_path": tmp_path}
                    ).json()
 
                    with col2:
                        st.subheader("📝 Analysis Result")
 
                        st.markdown(f"**🤖 Caption:** {res.get('caption', 'N/A')}")
                        st.markdown(f"**📄 OCR Text:** {res.get('ocr_text', 'No text found') or 'No text found'}")
 
                        if res.get("summary"):
                            st.markdown(f"**📊 Summary:** {res.get('summary')}")
 
                        # Related images
                        related = res.get("related_images", [])
                        if related:
                            st.subheader("🔗 Related Images in Index")
                            rcols = st.columns(min(len(related), 3))
                            for i, r in enumerate(related):
                                with rcols[i % 3]:
                                    rpath = f"src/data/images/{r['source']}"
                                    if os.path.exists(rpath):
                                        st.image(rpath, caption=r["caption"], use_column_width=True)
                                    else:
                                        st.caption(f"📄 {r['source']}: {r['caption']}")
 
                    os.unlink(tmp_path)
 
                    st.session_state.messages.append({"role": "user",      "content": "[Image→Text] Uploaded image for analysis"})
                    st.session_state.messages.append({"role": "assistant", "content": res.get("summary", res.get("caption", ""))})
 
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to API.")
 
 
# ════════════════════════════════════════════════════════════════════════════
# TEXT RAG + SQL QA — chat input
# ════════════════════════════════════════════════════════════════════════════
else:
    question = st.chat_input("Ask a question...")
 
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
 
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    if "Text RAG" in mode:
                        res = requests.post(f"{API_URL}/ask",
                                            json={"question": question, "k": top_k}).json()
                        answer = res.get("answer", "No answer.")
                        st.markdown(answer)
 
                        with st.expander("📊 Evaluation"):
                            ev = res.get("evaluation", {})
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Confidence",    f"{ev.get('confidence_pct', 0)}%")
                            c2.metric("Faithfulness",  ev.get('faithfulness_score', 0))
                            c3.metric("Hallucination", ev.get('hallucination_label', 'N/A'))
 
                        with st.expander("📂 Sources"):
                            for s in res.get("sources", []):
                                st.caption(f"• {s}")
 
                    elif "SQL QA" in mode:
                        res = requests.post(f"{API_URL}/ask-sql",
                                            json={"question": question}).json()
 
                        if res.get("error"):
                            st.error(f"SQL Error: {res['error']}")
                            answer = res.get("summary", "Error.")
                        else:
                            st.markdown(res.get("summary", ""))
                            with st.expander("🔍 Generated SQL"):
                                st.code(res.get("sql", ""), language="sql")
                            with st.expander("📋 Raw Results"):
                                st.text(res.get("table", ""))
                            answer = res.get("summary", "")
 
                except requests.exceptions.ConnectionError:
                    answer = "❌ Cannot connect to API."
                    st.error(answer)
 
        st.session_state.messages.append({"role": "assistant", "content": answer})
    
