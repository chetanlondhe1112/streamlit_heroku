import streamlit as st
import database as db
from PIL import Image
from datetime import datetime
import streamlit_authenticator as stauth

current_date = datetime.now()
global authentication_status

@st.experimental_singleton()
def main():
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = ""
        if "username" not in st.session_state:
            st.session_state["username"]=""
        if "lable" not in st.session_state:
            st.session_state["lable"] = ""



        Menu = ["Login", "Sign Up"]
        process = st.sidebar.selectbox("Menu", Menu)

        if process == "Login":
            users = db.fetch_all_users()

            username = [user["key"] for user in users]
            names = [user["name"] for user in users]
            hashed_password = [user["password"] for user in users]

            authenticator = stauth.Authenticate(names, username, hashed_password, "dfgdfg", "sdfgfg", cookie_expiry_days=30)

            names,authentication_status, username = authenticator.login("Login", "main")
            st.session_state["authentication_status"]=authentication_status
            if st.session_state["authentication_status"]:
                st.markdown(f'# Welcome *{st.session_state["username"]}*')
                authenticator.logout('Logout', 'sidebar')
            elif st.session_state["authentication_status"] == False:
                st.error('Username/password is incorrect')
            elif st.session_state["authentication_status"] == None:
                st.warning('Please enter your username and password')

        elif process == "Sign Up":
            users = db.fetch_all_users()
            usernames = [user["key"] for user in users]
            names = [user["name"] for user in users]

            st.subheader("Create New Account")
            name = st.text_input("name")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            if st.button("Sign Up"):
                if name in names and username in usernames:
                    st.warning("User already exist!")
                else:
                    hashed_password = stauth.Hasher([str(password)]).generate()
                    # print(hashed_password[0])
                    db.insert_user(username,name,str(hashed_password[0]))
                    st.success("Successfully created.")
                    st.balloons()

if __name__ == '__main__':
    main()
