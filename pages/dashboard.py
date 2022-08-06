import  streamlit as st
st.session_state.get(st.session_state["authentication_status"])
if st.session_state["authentication_status"]:
    st.title("Dashboard")
    st.markdown(f'# Welcome *{st.session_state["username"]}*')
else:
    st.warning("Please login")