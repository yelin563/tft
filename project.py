#10_schoolmap.py

import streamlit as st
import pandas as pd


import random
import requests

import numpy as np



from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide")



def Always_COO(p,i): # Player Always Choose Cooperate.
    # p : The Player Actions.
    p[i] = 0 # 0 Represents the Cooperate Action.
    return p[i] # Return The Next Action of the player.

def Always_DEF(p,i): # Player Always Choose Defect.
    # p : The Player Actions.
    p[i] = 1  # 1 Represents the Defect Action.
    return p[i] # Return The Next Action of the player.

def Tit_For_Tat(p1,p2,i): # Player Cooperate in the first round. Then in each subsequent round, play the opponent's action in the previous round.
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 0 # Make the first round of the player Cooperate.
    else:
        p1[i] = p2[i-1] # The other rounds is the opponent's action in the previous round.
    return p1[i] # Return The Next Action of the player.


def Suspicious_TFT(p1,p2,i): # Player Defect in the first round. Then in each subsequent round, play the opponent's action in the previous round.
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 1 # Make the first round of the player Defect.
    else:
        p1[i] = p2[i-1] # The other rounds is the opponent's action in the previous round.
    return p1[i] # Return The Next Action of the player.


def Reverse_TFT(p1,p2,i): # Defect in the first round, then plays the reverse of the opponent's action in the previous round.
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 1 # Make the first round of the player Defect.
    else:
        p1[i] = 1 - p2[i-1] # The other rounds is the Reverse of the opponent's action in the previous round.
    return p1[i] # Return The Next Action of the player.


def Random(p,i): # In each round, cooperate or defect with equal probabilities.
    # p : The Player Actions.
    actions = [0,1] # The possible actions to be choosen.
    p[i] = random.choice(actions) # Make the action Cooperate or defect based on equal probabilities.
    return p[i] # Return The Next Action of the player.


def Naive_Prober(p1,p2,i): #Cooperate in the first round. Then in each subsequent round, play the opponent's action in the previous round, but sometimes defect in lieu of cooperation with some probability.
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 0 # Make the first round of the player Defect.
    else:
        r = random.random() # Random Number to check the probability of make the next action to be defect
        if( 0 < r < 0.001):
            p1[i] = 1
        else:
            p1[i] = p2[i-1] # if not we will do same as we did in normal Tit For Tat
    return p1[i] # Return The Next Action of the player.


def hatred(p1,p2,i):
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 0 # Make the first round of the player Cooperate.
    else:
      if sum(p2)>0:
        p1[i] = 1
      else:
        p1[i]=0
    return p1[i] # Return The Next Action of the player.

def Suspicious_hatred(p1,p2,i):
    # p1 : The Player 1  Actions.
    # p2 : The Player 2  Actions.
    if(i == 0):
        p1[i] = 1 
    else:
      if sum(p2)>0:
        p1[i] = 1
      else:
        p1[i]=0
    return p1[i] # Return The Next Action of the player.

def calc_payoffs(p1,p2,payoff_matrix): # function to  calculate the payoffs
    fit1 = 0
    fit2 = 0
    temp1=[]
    temp2=[]
    for i in range(len(p1,)):
        fit1 += payoff_matrix[p1[i],p2[i]][0]
        fit2 += payoff_matrix[p1[i],p2[i]][1]
        temp1.append(fit1)
        temp2.append(fit2)
    #print(temp1,temp2)
    return fit1,fit2


def IPDGame(Strategy1,Strategy2,p1,p2,k):
    for i in range(k):
        if(Strategy1 == '항상협력자'):
            p1[i] = Always_COO(p1,i)
        if(Strategy1 == '항상배신자'):
            p1[i] = Always_DEF(p1,i)
        if(Strategy1 == '따라쟁이'):
            p1[i] = Tit_For_Tat(p1,p2,i)
        if(Strategy1 == '배신한 따라쟁이'):
            p1[i] = Suspicious_TFT(p1,p2,i)
        if(Strategy1 == '반대 따라쟁이'):
            p1[i] = Reverse_TFT(p1,p2,i)
        if(Strategy1 == '랜덤'):
            p1[i] = Random(p1,i)
        if(Strategy1 == '원한을 가진 자'):
            p1[i] = hatred(p1,p2,i)
        if(Strategy1 == 'Naive Prober'):
            p1[i] = Naive_Prober(p1,p2,i)
        if(Strategy1 == '배신한 원한을 가진 자'):
            p1[i] = Suspicious_hatred(p1,p2,i)
        if(Strategy2 == '항상협력자'):
            p2[i] = Always_COO(p2,i)
        if(Strategy2 == '항상배신자'):
            p2[i] = Always_DEF(p2,i)
        if(Strategy2 == '따라쟁이'):
            p2[i] = Tit_For_Tat(p2,p1,i)
        if(Strategy2 == '배신한 따라쟁이'):
            p2[i] = Suspicious_TFT(p2,p1,i)
        if(Strategy2 == '반대 따라쟁이'):
            p2[i] = Reverse_TFT(p2,p1,i)
        if(Strategy2 == '랜덤'):
            p2[i] = Random(p2,i)
        if(Strategy2 == '원한을 가진 자'):
            p2[i] = hatred(p2,p1,i)
        if(Strategy2 == '배신한 원한을 가진 자'):
            p2[i] = Suspicious_hatred(p2,p1,i)

        if(Strategy2 == 'Naive Prober'):
            p2[i] = Naive_Prober(p2,p1,i)

    payoff_matrix = np.array([[(2, 2), (-1, 3)], [(3, -1), (0,0)]], dtype=object)
    fit1,fit2 = calc_payoffs(p1,p2,payoff_matrix)
    #print(p1,p2)
    #if(fit1 > fit2):
        #print("The Winning Strategy is : " + Strategy1 + " Which belongs to Player 1" )
        #print(fit1,fit2)
    #elif(fit2 > fit1):
        #print("The Winning Strategy is : " + Strategy2 + " Which belongs to Player 2" )
        #print(fit1,fit2)
    #else:
        #print("Draw Game, Meaning that The two strategies are equal")
        #print(fit1,fit2)
    return fit1, fit2


def tournament(lst1,lst2):
  

  res=[]
  tl=[letter for letter, count in zip(lst2, lst1) for _ in range(count)]
  
  for j in range(len(tl)):
    temp=0
    for i in range(len(tl)):
      if i!=j:
          temp+=IPDGame(tl[j],tl[i],p1,p2,gn)[0]

      
    res.append(temp)
    
  return pd.DataFrame({'전략':tl,'총점':res})

@st.dialog("학번이름을 입력해주세요")
def name():
    
    num = st.text_input("예:20123홍길동")
    newnum = num.replace(" ", "")
    if st.button("제출하기"):
        st.session_state.name = newnum
        st.rerun()

if "name" not in st.session_state:
    st.write("아래 버튼을 눌러 학번이름을 제출해주세요.")
    if st.button("학번입력하기"):
        name()
  
else:
    f"학번 이름: {st.session_state.name}"

#if 'name' not in st.session_state:
    #st.session_state['name']='N'
    
#if st.session_state['name']=='N':
    #num=st.text_input('학번이름을 입력해주세요')
    #if num:
        #st.session_state['name']=num
st.title("협력 게임")
st.write(r'''<span style="font-size: 20px;">$\textsf{[학습목표] 협력 게임의 전략을 선택해보고 어떤 전략이 가장 점수가 높을 확률이 큰지 알아보자.}$</span>''', unsafe_allow_html=True)




st.divider()

#st.subheader("시뮬레이션")
st.write(r'''<span style="font-size: 15px;">$\textsf{각 전략의 명 수를 다양하게 설정해보며 어떤 전략이 점수가 높은지 살펴보세요. }$</span>''', unsafe_allow_html=True)

if 'cumulative_results' not in st.session_state:
    st.session_state.cumulative_results = pd.DataFrame(columns=['전략', '총점'])
  
st.divider()

col1, col2 = st.columns([1, 1,1])


with col1:
    n1 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label_visibility="collapsed")
    n2 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label_visibility="collapsed")
    n6 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label='n6',label_visibility="collapsed")
    n3 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label='n3',label_visibility="collapsed")
    n7 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label='n7',label_visibility="collapsed")
    n4 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label='n4',label_visibility="collapsed")
    n5 = st.number_input("항상협력자",placeholder="명 수를 작성하세요.", min_value=0, max_value=50, step=1, value=0,label='n5',label_visibility="collapsed")
    gn= st.number_input("항상협력자",placeholder="라운드 수를 작성하세요.", min_value=5, max_value=50, step=1, value=5,label='gn',label_visibility="collapsed")
    
b1= st.button('결과 확인하기')
with col2:
    if b1:
        lst1=[]
        lst2=[]
        row=[]
        p1 = np.zeros(gn,dtype=int)
        p2 = np.zeros(gn,dtype=int)
        if n1>0:
            lst1.append(n1)
            lst2.append('항상협력자')
            
        if n2>0:
            lst1.append(n2)
            lst2.append('따라쟁이')
            
        
        if n3>0:
            lst1.append(n3)
            lst2.append('원한을 가진 자')
            
        if n4>0:
            lst1.append(n4)
            lst2.append('항상배신자')
            
        if n5>0:
            lst1.append(n5)
            lst2.append('랜덤')
            
        if n6>0:
            lst1.append(n6)
            lst2.append('배신한 따라쟁이')
        if n7>0:
            lst1.append(n7)
            lst2.append('배신한 원한을 가진 자')
            
        if len(lst1) > 1:
            # Run the tournament and update cumulative results
            new_results = tournament(lst1, lst2)
            
            # Append the new results to the existing cumulative results
            st.session_state.cumulative_results = pd.concat([st.session_state.cumulative_results, new_results], ignore_index=True)
            
            # Ensure that the '총점' column is numeric before calculating the top 10%
            st.session_state.cumulative_results['총점'] = pd.to_numeric(st.session_state.cumulative_results['총점'], errors='coerce')
            
            # Calculate top 10% cutoff
            total_strategies = len(st.session_state.cumulative_results)
            cutoff = int(0.1 * total_strategies) if total_strategies >= 10 else 1
            top_10_cutoff = st.session_state.cumulative_results['총점'].nlargest(cutoff).min()

            # Determine top 10% strategies
            st.session_state.cumulative_results['Top 10%'] = st.session_state.cumulative_results['총점'] >= top_10_cutoff

            # Calculate probabilities
            prob_df = st.session_state.cumulative_results.groupby('전략')['Top 10%'].mean().reset_index()
            prob_df.columns = ['전략', 'Top 10% 확률']

            # Display results
            #st.write("### 누적 결과")
            #st.dataframe(st.session_state.cumulative_results.sort_values('총점', ascending=False, ignore_index=True), width=500, height=400)
            # Run the tournament and get the current round results
            current_results = tournament(lst1, lst2)
            
            # Ensure that the '총점' column is numeric
            current_results['총점'] = pd.to_numeric(current_results['총점'], errors='coerce')
            
            # Calculate top 10% cutoff for the current round
            total_strategies_current = len(current_results)
            cutoff_current = int(0.1 * total_strategies_current) if total_strategies_current >= 10 else 1
            top_10_cutoff_current = current_results['총점'].nlargest(cutoff_current).min()
            
            # Add a new column to check if the strategy is in the top 10% for the current round
            current_results['Top 10% 여부'] = current_results['총점'] >= top_10_cutoff_current
            
            # Display the current results with the top 10% check
            st.write("### 현재 라운드 결과 (상위 10% 체크)")
            st.dataframe(current_results.sort_values('총점', ascending=False, ignore_index=True), width=500, height=400)
            
            
            st.write("### 각 전략이 상위 10%에 속할 확률")
            st.dataframe(prob_df.sort_values('Top 10% 확률', ascending=False, ignore_index=True), width=500, height=400)
        else:
            st.write('적어도 두 명은 존재해야 합니다')


    
    
    
