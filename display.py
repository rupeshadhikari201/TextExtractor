# display_app.py
import streamlit as st
import urllib.parse
import html

def main():
    # Get query parameters using new st.query_params API
    query_params = st.query_params
    encoded_text = query_params.get("text", "")
    
    if not encoded_text:
        st.error("No content to display")
        return

    decoded_text = urllib.parse.unquote(encoded_text)
    
    st.title("Accessibility-Optimized Viewer")
    
    # Accessibility Controls
    col1, col2, col3 = st.columns(3)
    with col1:
        font_size = st.slider("Font Size", 8, 48, 16)
        line_height = st.slider("Line Height", 1.0, 2.5, 1.5)
    with col2:
        font_color = st.color_picker("Text Color", "#000000")
        bg_color = st.color_picker("Background Color", "#FFFFFF")
    with col3:
        contrast_mode = st.checkbox("High Contrast Mode")
        dyslexia_font = st.checkbox("Dyslexia-Friendly Font")

    # Apply contrast mode
    if contrast_mode:
        font_color = "#FFFFFF"
        bg_color = "#000000"

    # Create CSS styles
    font_family = "Arial" if not dyslexia_font else "OpenDyslexic, sans-serif"
    
    custom_css = f"""
    <style>
        .content {{
            font-size: {font_size}px;
            color: {font_color};
            background-color: {bg_color};
            line-height: {line_height};
            font-family: {font_family};
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }}
        @keyframes highlight {{ 0% {{background: yellow;}} 100% {{background: transparent;}} }}
        .highlight {{ animation: highlight 2s; }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Text display with additional features
    st.markdown(f'<div class="content">{html.escape(decoded_text)}</div>', unsafe_allow_html=True)
    
    # Additional accessibility features
    with st.expander("More Accessibility Options"):
        col1, col2 = st.columns(2)
        with col1:
            letter_spacing = st.slider("Letter Spacing (px)", -1, 5, 0)
            word_spacing = st.slider("Word Spacing (px)", 0, 10, 0)
        with col2:
            text_align = st.selectbox("Text Alignment", ["left", "justify", "center"])
            text_transform = st.selectbox("Text Case", ["none", "uppercase", "lowercase"])
        
        # Update CSS
        st.markdown(f"""
        <style>
            .content {{
                letter-spacing: {letter_spacing}px;
                word-spacing: {word_spacing}px;
                text-align: {text_align};
                text-transform: {text_transform};
            }}
        </style>
        """, unsafe_allow_html=True)

    # Text-to-Speech Integration
    if st.button("Read Aloud"):
        st.markdown("""
        <script>
            var msg = new SpeechSynthesisUtterance();
            msg.text = document.querySelector('.content').textContent;
            window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()