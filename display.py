import streamlit as st
import html
import re
from database import conn  # Import the database connection

def process_text(text):
    """Clean and structure the extracted text."""
    # Preserve paragraph breaks
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Convert bullet points to HTML lists
    text = re.sub(r'^(\s*•\s+)(.*)$', r'<li>\2</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*</li>\n)+', r'<ul>\g<0></ul>\n', text)
    
    # Detect headings (lines ending with colons or in all caps)
    text = re.sub(r'^([A-Z][A-Z\s]+:?)\s*$', r'<h3 class="heading">\1</h3>', text, flags=re.MULTILINE)
    
    # Convert URLs to clickable links
    text = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', text)
    
    # Preserve original paragraph structure
    paragraphs = text.split('\n\n')
    processed = []
    
    for p in paragraphs:
        p = p.strip()
        if p:
            if p.startswith('<ul>') or p.startswith('<h3'):
                processed.append(p)
            else:
                processed.append(f'<p>{p}</p>')
    
    return '\n'.join(processed)

def main():
    st.title("Accessibility-Optimized Viewer")
    
    # Use number input for integer IDs with validation
    try:
        text_id = st.number_input(
            "Enter Document ID", 
            min_value=1, 
            step=1,
            format="%d",
            help="Enter the numeric ID provided after document upload"
        )
    except ValueError:
        st.error("Please enter a valid numeric ID")
        return
    
    if text_id:
        # Convert to integer and validate
        try:
            text_id = int(text_id)
            if text_id < 1:
                raise ValueError
        except (ValueError, TypeError):
            st.error("Invalid ID format. Please enter a positive whole number.")
            return

        # Retrieve the text from database
        c = conn.cursor()
        c.execute("SELECT content FROM texts WHERE id = ?", (text_id,))
        result = c.fetchone()
        
        if result:
            text = result[0]
            
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
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    hyphens: auto;
                }}
                
                .content p {{
                    margin: 0.8em 0;
                }}
                
                .content ul {{
                    margin: 0.8em 20px;
                    padding-left: 20px;
                    list-style-type: disc;
                }}
                
                .content h3 {{
                    font-size: 1.2em;
                    margin: 1.2em 0 0.5em;
                    padding-bottom: 3px;
                    border-bottom: 2px solid {font_color};
                }}
                
                .content a {{
                    color: {font_color};
                    text-decoration: underline;
                    word-break: break-all;
                }}
                
                @keyframes highlight {{ 0% {{background: yellow;}} 100% {{background: transparent;}} }}
                .highlight {{ animation: highlight 2s; }}
            </style>
            """
            st.markdown(custom_css, unsafe_allow_html=True)

            # Process and display text
            processed_text = process_text(html.escape(text))
            st.markdown(f'<div class="content">{processed_text}</div>', unsafe_allow_html=True)
            
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
            else:
                st.error("Text not found. Please check the ID.")
            
        else:
            st.error("Document not found. Please check the ID and try again.")

if __name__ == "__main__":
    main()
