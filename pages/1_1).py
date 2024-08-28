#10_schoolmap.py

import streamlit as st
import pandas as pd


import random
import requests

import numpy as np



from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")




res1=st.text_area("내 전략을 설명해주세요")
option = st.selectbox("자신의 전략에서 첫 수는 협력인가요 배신인가요?",
    ("협력", "배신"),)
score=st.number_input("나의 평균 점수를 입력해주세요(반올림하여 자연수로 입력해주세요).",placeholder="나의 평균 점수를 입력해주세요(반올림하여 자연수로 입력해주세요).", min_value=0, step=1, value=0)
if st.button('제출하기'):
    if st.session_state['name']=='N':
        st.write('첫 페이지의 위에 학번 이름을 입력해주세요')
    else:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df1 = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1kOEltiz9y8b5HCuFegEAyfUbfo95xYrdPlh59GB3EhU/edit?gid=1194618377#gid=1194618377",
        worksheet="response1",
        ttl="1s",
        usecols=[0, 1],
        nrows=100
        )  
        df1 = df1.dropna(axis=0)
        st.dataframe(df1) 
        new_data=pd.DataFrame({'학번':st.session_state['name'],'전략':res1,'첫수':option,'평균점수':score},index=[0])
        st.dataframe(new_data) 
        conn.update(worksheet="response1",data=pd.concat([df1, new_data], ignore_index=True))

    
    
    
    
