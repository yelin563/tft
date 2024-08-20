import streamlit as st
import pandas as pd
from PIL import Image


import matplotlib
import matplotlib.pyplot as plt

from streamlit_gsheets import GSheetsConnection
import requests

import numpy as np

import geopandas as gpd

st.set_page_config(layout="wide")

st.header('우리반 측정소')




    
if st.button('새로고침'):
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    rdf = conn.read(
    worksheet="response4",
    ttl="1s",
    usecols=[0,1,2,3],
    nrows=100
    )  
    st.session_state.rdf = rdf

rdf = st.session_state.get('rdf', pd.DataFrame())
if len(rdf)>0 :
    rdf = rdf.dropna(axis=0)
    st.dataframe(rdf) 
    n=st.selectbox(label='학번',options=rdf['학번'].unique(),index=None,placeholder='학번을 선택해주세요')
    
    #if n:
        
    #else:
        

        