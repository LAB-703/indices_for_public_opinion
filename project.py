#import functools
from pathlib import Path

import streamlit as st
#from st_aggrid import AgGrid
#from st_aggrid.shared import JsCode
#from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
#import plotly.express as px
import numpy as np

st.set_page_config(
        "Search Engine Dashboard",
        "📈",
        initial_sidebar_state="expanded",
        layout="wide",
    )

# 메인메뉴 없애고, 저작권 표시
hide_menu='''
<style>
#MainMenu {
    visibility:hidden;
}
#document{
    font-family:'Pretendard JP Variable', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Emoji', sans-serif;
    }
footer {
    visibility:visible;
    size: 10%;
    font-family: 'Pretendard JP Variable';
}
footer:after{
    content: 'SPDX-FileCopyrightText: © 2022 LAB-703 SPDX-License-Identifier: MIT';
    font-size: 30%;
    display:block;
    position:relative;
    color:silver;
    font-family: 'Pretendard JP Variable';
}
code {
    color: #C0504D;
    overflow-wrap: break-word;
    background: linen;
    font-family: 'Source Code Pro';
}
#root > div:nth-child(1) > div > div > a {
    visibility:hidden;
}    
    
    
div.stButton > button:first-child {
font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
  font-size:100%;
    background-color: #FCF9F6;
    font-color: #C0504D;
    
}
button.css-jgupqz.e10mrw3y2 {
    opacity: 0;
    height: 2.5rem;
    padding: 0px;
    width: 2.5rem;
    transition: opacity 300ms ease 150ms, transform 300ms ease 150ms;
    border: none;
    background-color: #C0504D;
    visibility: visible;
    color: rgba(0, 0, 0, 0.6);
    border-radius: 0.75rem;
    transform: scale(0);
}
div.viewerBadge_link__1S137 {
    display:none;
    background-color: #C0504D;
}
div.css-j7qwjs.e1fqkh3o5 {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
}
a.viewerBadge_container__1QSob {
    z-index: 50;
    font-size: .875rem;
    position: fixed;
    bottom: 0;
    right: 0;
    display: none;
}
div.streamlit-expanderHeader.st-ae.st-bq.st-ag.st-ah.st-ai.st-aj.st-br.st-bs.st-bt.st-bu.st-bv.st-bw.st-bx.st-as.st-at.st-by.st-bz.st-c0.st-c1.st-c2.st-b4.st-c3.st-c4.st-c5.st-b5.st-c6.st-c7.st-c8.st-c9 {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', sans-serif;
    font-weight: 200;
}
</style>
'''

st.markdown(hide_menu, unsafe_allow_html=True)

#chart = functools.partial(st.plotly_chart, use_container_width=True)
#COMMON_ARGS = {
#    "color": "symbol",
#    "color_discrete_sequence": px.colors.sequential.Greens,
#    "hover_data": [
#        "account_name",
#        "percent_of_account",
#        "quantity",
#        "total_gain_loss_dollar",
#        "total_gain_loss_percent",
#    ],
#}




##################################################################
st.sidebar.subheader("Search Engine")

keyword = st.sidebar.text_input('keyword', '탈원전')
st.sidebar.write('keyword is', keyword)


platform = ['naver_news','naver_cafe','naver_blog', 'daum_news','daum_cafe','daum_blog','youtube','tweeter','facebook','instagram']
platform_selections = st.sidebar.multiselect(
    "Select Platforms to View", options=platform, default=platform
)


Start_date = st.sidebar.date_input(
 "Start date")
st.sidebar.write('Start date is:', Start_date)

End_date = st.sidebar.date_input(
 "End date")
st.sidebar.write('End date is:', End_date)

##############################################################

df=pd.read_csv("example2.csv", encoding='utf8')

head="키워드 " +keyword+"에 대한 플랫폼별 검색결과는 "+str(len(df))+"건으로 다음과 같습니다."
st.header(head)

for platform in platform_selections:
    expander = st.expander(platform)
    dataframe=df[df['platform']==platform]
    #expander.write(dataframe)
    
    for i in range(0,len(dataframe)):
        info="작성자 : "+str(dataframe.iloc[i][7])+" | 작성일 : "+str(dataframe.iloc[i][5])
        link=" | [원문보기]("+str(dataframe.iloc[i][1])+")"
        expander.write(info+link)
        if dataframe.iloc[i][8] is np.NaN:
            expander.write("삭제된 댓글입니다.")
        else:
            expander.write(dataframe.iloc[i][8])
        expander.write("")
