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
        "indices_for_public_opinion",
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


import pandas as pd
import numpy as np

def CR(df,sort_by,k=3):
    CR_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    CR_df['Si']=CR_df['count']/len(df)
    CR=np.sum(CR_df['Si'][0:k]).round(3)
    return CR

import pandas as pd
import numpy as np

def HHI(df, sort_by):
    HHI_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    HHI_df['Si']=HHI_df['count']/len(df)
    HHI=np.sum(np.square(HHI_df['Si'])*10000)
    return HHI

import pandas as pd
import numpy as np

def Gini(df, sort_by):
    Gini_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index().sort_values('count')
    n=len(Gini_df)
    Mu=Gini_df['count'].sum()
    Gini_list=[]
    for i in range(0,n):
        for j in range(0,n):
            Gini_list.append([Gini_df['index'][i],Gini_df['index'][j],abs(Gini_df['count'][i]-Gini_df['count'][j])])
    Gini_df2=pd.DataFrame(Gini_list,columns=[sort_by+"1",sort_by+"2","abs"])
    Sum=Gini_df2['abs'].sum()
    Delta=Sum/(n*(n-1))
    Gini=(Delta/(2*Mu)).round(3)
    return Gini, Gini_df2


import pandas as pd
import numpy as np

def LQ(df, index_i, i, index_j,j, sort_by):
    LQ_df=df[[index_i,index_j,sort_by]].drop_duplicates()
    LQ_df2=pd.crosstab(LQ_df[index_j],LQ_df[index_i],margins=True)
    Q=LQ_df2['All']['All']
    Qi=LQ_df2[i]['All']
    Qj=LQ_df2['All'][j]
    Qij=LQ_df2[i][j]
    LQ=round((Qij/Qi)/(Qj/Q),3)
    return LQ,LQ_df2


##############################################################

df_news=pd.read_csv("df_news2.csv", encoding='cp949',index_col=0)
df_reply=pd.read_csv("df_reply.csv", encoding='cp949',index_col=0)
tabs=["df_news", "df_reply", "user ➕"]

#################################################################
st.sidebar.subheader("📈 indices for public opinion")





index = ['CR','HHI','Gini', 'LQ']
indices_selections = st.sidebar.multiselect(
    "Select indices to View", options=index, default=index
)

#################################################################

tab1, tab2,tab3 = st.tabs(tabs)

tab1.subheader("df_news")
tab1.write(df_news)
tab1.write(CR(df_news, 'COMPANY', 5))

tab2.subheader("df_reply")
tab2.write(df_reply)

tab3.subheader("user ➕")
uploaded_files = tab3.sidebar.file_uploader("Due to the limit of capacity, remove unnecessary columns and upload them.", type=['csv'], accept_multiple_files=True)

for uploaded_file in uploaded_files:
    dataframe = pd.read_csv(uploaded_file,index_col=0,encoding='cp949')
    tab3.write(dataframe)


