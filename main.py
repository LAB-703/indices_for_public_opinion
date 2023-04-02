from pathlib import Path
import streamlit as st
import pandas as pd
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


def CR(df,sort_by,k=3):
    CR_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    CR_df['Si']=CR_df['count']/len(df)
    CR=np.sum(CR_df['Si'][0:k]).round(3)
    return CR


def HHI(df, sort_by):
    HHI_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    HHI_df['Si']=HHI_df['count']/len(df)
    HHI=np.sum(np.square(HHI_df['Si'])*10000).round(1)
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



#################################################################
st.sidebar.subheader("📈 indices for public opinion")

indices_selections = st.selectbox(
    "Select index to Know",['CR','HHI','Gini', 'LQ']
)

tabs=["df_news", "df_reply", "user ➕"]
tab1, tab2,tab3 = st.tabs(tabs)

tab1.subheader("df_news")
tab1.write(df_news)


tab2.subheader("df_reply")
tab2.write(df_reply)

tab3.subheader("user ➕")


# 복수 허용 
# uploaded_files = tab3.file_uploader("Due to the limit of capacity, remove unnecessary columns and upload them.", type=['csv'], accept_multiple_files=True)

# for uploaded_file in uploaded_files:
#     dataframe = pd.read_csv(uploaded_file,index_col=0,encoding='cp949')
#     uploaded_file.str.find("name"
#     tab3.write(dataframe)
        

# file_selections = tab3.selectbox(
#     "Select file to apply",uploaded_files)

# tab3.write(uploaded_files)


uploaded_file = tab3.file_uploader("Due to the limit of capacity, remove unnecessary columns and upload them.", type=['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file,index_col=0,encoding='cp949')
    sort_by=tab3.selectbox("Select column to apply for sort_by", df.columns)
    tab3.write(df)  

##################################################################################1. CR

if indices_selections=="CR":
    st.sidebar.latex(r'''CR_{k}=\sum_{i=1}^{k}S_{i}
    ''')
    CR_code = '''import pandas as pd
import numpy as np

def CR(df,sort_by,k=3):
    CR_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    CR_df['Si']=CR_df['count']/len(df)
    CR=np.sum(CR_df['Si'][0:k]).round(3)
    return CR'''
    st.sidebar.code(CR_code, language='python')
    tab1.write('CR index for COMPANY')
    tab1.write(CR(df_news, 'COMPANY'))
    tab1.write('CR index for AUTHOR')
    tab1.write(CR(df_news, 'AUTHOR'))

    tab2.write('CR index for AUTHOR_RE')
    tab2.write(CR(df_reply, 'AUTHOR_RE'))
        
    if uploaded_file is not None:
        tab3.write(f'CR index for {sort_by}')       
        tab3.write(CR(df, sort_by))



##################################################################################2. HHI
        
if indices_selections=="HHI":
    st.sidebar.latex(r'''
    HHI=\sum_{i=1}^{N}{S_{i}}^{2}\times 10,000 
\\  
\\
 S_{i}=\frac{n_{i}}{N}
    ''')
    HHI_code = '''import pandas as pd
import numpy as np

def HHI(df, sort_by):
    HHI_df=pd.DataFrame({"count" : df[sort_by].value_counts()}).reset_index()
    HHI_df['Si']=HHI_df['count']/len(df)
    HHI=np.sum(np.square(HHI_df['Si'])*10000).round(1)
    return HHI'''
    st.sidebar.code(HHI_code, language='python')
        
    tab1.write('HHI for COMPANY')
    tab1.write(HHI(df_news, 'COMPANY'))
    tab1.write('HHI for AUTHOR')
    tab1.write(HHI(df_news, 'AUTHOR'))

    tab2.write('HHI for AUTHOR_RE')
    tab2.write(HHI(df_reply, 'AUTHOR_RE'))
        
    if uploaded_file is not None:
        tab3.write(f'HHI for {sort_by}')       
        tab3.write(HHI(df, sort_by))
##################################################################################3. Gini
         
if indices_selections=="Gini":
    st.sidebar.latex(r'''
    G=\frac{\Delta }{2\mu }\\
    \\  
\\
\Delta =\frac{1}{n(n-1)} \sum_{n}^{i=1}\sum_{n}^{j=1}\left|x_{i}-x_{j}\right|
    ''')
    Gini_code = '''def Gini(df, sort_by):
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
'''
    st.sidebar.code(Gini_code, language='python')
        
    tab1.write('Gini for COMPANY')
    tab1.write(Gini(df_news, 'COMPANY')[0])
    tab1.write(Gini(df_news, 'COMPANY')[1])
        
    tab1.write('Gini for AUTHOR')
    tab1.write(Gini(df_news, 'AUTHOR')[0])
    tab1.write(Gini(df_news, 'AUTHOR')[1])

    tab2.write('Gini for AUTHOR_RE')
    tab2.write(Gini(df_reply, 'AUTHOR_RE')[0])
    tab2.write(Gini(df_reply, 'AUTHOR_RE')[1])
        
    if uploaded_file is not None:
        tab3.write(f'Gini for {sort_by}')       
        tab3.write(Gini(df, sort_by)[0])
        tab3.write(Gini(df, sort_by)[1])
        
##################################################################################4. LQ
        
if indices_selections=="LQ":
    st.sidebar.latex(r'''
       LQ=\frac{Q_{ij}/Q_{i}}{Q_{j}/Q}
    ''')
    LQ_code = '''import pandas as pd
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
'''
    st.sidebar.code(LQ_code, language='python')
    option = st.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

    st.write('You selected:', option)


#     tab1.write('LQ for COMPANY and ENGINE')
#     selected_ENGINE = st.selectbox('select one in ENGINE', list(df.ENGINE.unique()))
#     selected_COMPANY = st.selectbox('select one in COMPANY', list(df.COMPANY.unique()))

    tab1.write(LQ(df_news, 'ENGINE','DAUM', 'COMPANY','M**', 'AUTHOR')[0])
    tab1.write(LQ(df_news, 'ENGINE','DAUM', 'COMPANY','M**', 'AUTHOR')[1])

#     tab1.write(LQ(df_news, 'COMPANY')[1])
        
#     tab1.write('LQ for AUTHOR')
#     tab1.write(LQ(df_news, 'AUTHOR')[0])
#     tab1.write(LQ(df_news, 'AUTHOR')[1])

#     tab2.write('LQ for AUTHOR_RE')
#     tab2.write(LQ(df_reply, 'AUTHOR_RE')[0])
#     tab2.write(LQ(df_reply, 'AUTHOR_RE')[1])
        
#    if uploaded_file is not None:
#         sort_by2=tab3.selectbox("Select column to apply for sort_by", df.columns)
#         tab3.write(f'LQ for {sort_by} and {sort_by2}')       
#         tab3.write(LQ(df_news, sort_by,'DAUM', sort_by2,'M**', 'AUTHOR')[0])
#         tab3.write(LQ(df_news, sort_by,'DAUM', sort_by2,'M**', 'AUTHOR')[1])
