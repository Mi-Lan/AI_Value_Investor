import streamlit as st

st.title("🧪 Test App")
st.write("If you can see this, Streamlit is working!")

# Test tikr_scraper import
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd()))
    from tikr_scraper import TIKRScraper
    st.success("✅ TIKRScraper imported successfully!")
except Exception as e:
    st.error(f"❌ Import failed: {e}")

if st.button("Test Button"):
    st.balloons()
    st.write("Button clicked!") 