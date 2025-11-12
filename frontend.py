import os
import json
import time
import requests # type: ignore
import streamlit as st # type: ignore

# ========= Config =========
DEFAULT_API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/answer")
st.set_page_config(page_title="News Summarizer Chat", page_icon="💬", layout="centered")

# ========= Sidebar =========
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("FastAPI /answer URL", value=DEFAULT_API_URL)
    thread_id = st.text_input("Thread ID", value=st.session_state.get("thread_id", "1"))
    st.caption("Keep the same thread_id to preserve memory on the backend.")
    cols = st.columns(2)
    with cols[0]:
        if st.button("New Chat"):
            st.session_state.messages = []
            st.session_state.thread_id = thread_id
            st.rerun()
    with cols[1]:
        if st.button("Download Chat"):
            transcript = {
                "thread_id": thread_id,
                "messages": st.session_state.get("messages", []),
                "exported_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.download_button(
                "Save JSON",
                data=json.dumps(transcript, ensure_ascii=False, indent=2),
                file_name=f"chat_{int(time.time())}.json",
                mime="application/json",
            )

st.title("💬 News Summarizer — Chat")

# ========= Session State =========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = thread_id  # prime it

# ========= Helpers =========
def call_api(api_url: str, thread_id: str, user_text: str) -> dict:
    """
    Call FastAPI /answer and return a dict with at least {"summary": "...", "sources": [...]}
    The backend returns: {"answer": "<JSON string>"}.
    """
    payload = {"thread_id": thread_id, "user_text": user_text}
    resp = requests.post(api_url, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()  # {"answer": "<JSON string>"}
    raw = data.get("answer", "")

    # Parse the JSON string if possible
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            # normalize: expect summary + sources
            return {
                "summary": parsed.get("summary") or parsed.get("answer") or parsed.get("text") or str(parsed),
                "sources": parsed.get("sources") or []
            }
        else:
            # If it's a list or something else, show it as JSON
            return {"summary": json.dumps(parsed, ensure_ascii=False), "sources": []}
    except Exception:
        # Not valid JSON, just echo back as text
        return {"summary": str(raw), "sources": []}

def render_message(role: str, content: str, sources=None):
    """Render one chat message like ChatGPT."""
    with st.chat_message("assistant" if role == "assistant" else "user"):
        st.markdown(content)
        if role == "assistant" and sources:
            with st.expander("Sources"):
                for url in sources:
                    st.markdown(f"- [{url}]({url})")

# ========= History (show the whole chat) =========
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("sources"))

# ========= Chat input (like ChatGPT) =========
prompt = st.chat_input("Ask a news question… (Shift+Enter for newline)")

if prompt:
    # 1) show user bubble immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    # 2) call backend and stream a “thinking…” placeholder
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking…_")

        try:
            result = call_api(api_url, thread_id, prompt)
            summary = result.get("summary", "")
            sources = result.get("sources", [])

            # Replace placeholder with final answer
            placeholder.empty()
            st.markdown(summary)
            if sources:
                with st.expander("Sources"):
                    for url in sources:
                        st.markdown(f"- [{url}]({url})")

            # 3) save assistant message
            st.session_state.messages.append(
                {"role": "assistant", "content": summary, "sources": sources}
            )
        except requests.RequestException as e:
            placeholder.empty()
            st.error(f"Request failed: {e}")
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Request failed: {e}", "sources": []}
            )
        except Exception as e:
            placeholder.empty()
            st.error(f"Error: {e}")
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Error: {e}", "sources": []}
            )
