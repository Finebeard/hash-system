import streamlit as st
from whirlpool import whirlpool_hash

st.set_page_config(page_title="Whirlpool Hash Generator", layout="centered")
st.title("🔐 Whirlpool Hash Generator & Comparator")
st.markdown("Compute or compare Whirlpool hashes for text or files.")

tab1, tab2 = st.tabs(["📄 Generate Hash", "⚖️ Compare Files / Text"])

def safe_hash_bytes(b: bytes):
    try:
        digest = whirlpool_hash(b)
        return digest.hex().upper()
    except Exception as e:
        st.exception(f"Hashing failed: {e}")
        return None

# --- HASH GENERATOR ---
with tab1:
    st.subheader("Generate Hash")
    input_mode = st.radio("Select Input Type:", ["Text", "File"])

    if input_mode == "Text":
        text_input = st.text_area("Enter text:", height=150)
        if st.button("Generate Hash (Text)"):
            if not text_input:
                st.warning("Please enter some text.")
            else:
                hex_digest = safe_hash_bytes(text_input.encode("utf-8"))
                if hex_digest:
                    st.success("✅ Hash generated successfully!")
                    st.code(hex_digest, language="text")

    else:
        uploaded_file = st.file_uploader("Upload a file:", type=None, key="gen_file")
        if uploaded_file and st.button("Generate File Hash"):
            # Use getvalue() to reliably obtain file bytes
            data = uploaded_file.getvalue()
            if data is None:
                st.error("Could not read file bytes. Try re-uploading.")
            else:
                hex_digest = safe_hash_bytes(data)
                if hex_digest:
                    st.success(f"✅ Hash for **{uploaded_file.name}** generated:")
                    st.code(hex_digest, language="text")

# --- FILE/TEXT COMPARATOR ---
with tab2:
    st.subheader("Compare Two Inputs")
    compare_mode = st.radio("Compare:", ["Two Texts", "Two Files"])

    if compare_mode == "Two Texts":
        col1, col2 = st.columns(2)
        with col1:
            text1 = st.text_area("Text A", height=120, key="textA")
        with col2:
            text2 = st.text_area("Text B", height=120, key="textB")

        if st.button("Compare Text Hashes"):
            hash1 = safe_hash_bytes(text1.encode("utf-8"))
            hash2 = safe_hash_bytes(text2.encode("utf-8"))
            if hash1 and hash2:
                st.write("**Hash A:**", hash1)
                st.write("**Hash B:**", hash2)
                if hash1 == hash2:
                    st.success("✅ Both texts are identical.")
                else:
                    st.error("❌ Texts differ!")

    else:
        file1 = st.file_uploader("Upload File A", key="cmp_file_a")
        file2 = st.file_uploader("Upload File B", key="cmp_file_b")

        if st.button("Compare File Hashes"):
            if not file1 or not file2:
                st.warning("Please upload both files.")
            else:
                b1 = file1.getvalue()
                b2 = file2.getvalue()
                if b1 is None or b2 is None:
                    st.error("Failed to read one of the files. Try re-uploading.")
                else:
                    hash1 = safe_hash_bytes(b1)
                    hash2 = safe_hash_bytes(b2)
                    if hash1 and hash2:
                        st.write(f"**Hash A ({file1.name}):**", hash1)
                        st.write(f"**Hash B ({file2.name}):**", hash2)
                        if hash1 == hash2:
                            st.success("✅ Files are identical.")
                        else:
                            st.error("❌ Files differ!")

st.caption("Built with Streamlit and Python • Whirlpool Hash Implementation")
