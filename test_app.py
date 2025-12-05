import streamlit as st

st.set_page_config(page_title="Streamlit Test")

st.title("✅ Streamlit is Working!")
st.write("If you see this message, your setup is perfect 🎉")

number = st.slider("Pick a number", 1, 10)
st.write("Your chosen number is:", number)
