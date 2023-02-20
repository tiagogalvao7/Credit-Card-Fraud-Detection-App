from venv import create
import streamlit as st
import streamlit.components.v1 as components
import psycopg2 
import time
import datetime

from PIL import Image
from pathlib import Path
#from modelo import predictResults
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

##MACHINE LEARNING
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns


#---------------------------HOME-------------------------------------------------------
##DONE
def home():
    
    ##Blank space
    st.text("")
    ##Info text
    info = '<p style="font-family:sans-serif;color:White;font-size: 22px;">According to the most recent studies, around 100 milion people a year are affected by bank fraud problems.'
    st.markdown(info, unsafe_allow_html=True)
    ##Blank space
    st.text("")

    ##Import Images
    fraud_image = Image.open('Images/fraud.jpg')
    fraud_image2 = Image.open('Images/fraud2.jpg')

    col1, col2 = st.columns(2)

    with col1:
        st.image(fraud_image, width = 350)
    with col2:
        st.image(fraud_image2, width = 350)


    ##Blank space
    st.text("")
    ##Info text
    info2 = '<p style="font-family:sans-serif;color:White;font-size: 22px;">There are several types of fraud and they are increasingly frequent, according to some studies. most bank fraud occurs digitally due to people lack of experience.'
    #st.markdown(f'<h1 style="color:Black;font-size:20px;">{"Sign Up"}</h1>', unsafe_allow_html=True)
    st.markdown(info2, unsafe_allow_html=True) 


# ---------------------------ABOUT US-------------------------------------------------------
##DONE
def aboutUs():
    #st.title("Deteção de Fraudes em Pagamentos Bancários")
    st.text("")
    st.text("")
    
    ## PART 1
    #col1, col2, col3, col4 = st.columns(4)
    st.markdown("<h1 style='text-align:center;color:BLUE;font-size:45px;'>OUR</h1>", unsafe_allow_html=True)

    ## PART2
    st.markdown("<h1 style='text-align:center;color: GREEN;font-size:40px;'>MISSION   IS  TO</h1>", unsafe_allow_html=True)

    ## PART3
    st.markdown("<h1 style='text-align:center;color:RED;font-size:100px;'>S   T   O   P</h1>", unsafe_allow_html=True)

    ## PART4
    creditCard_image = Image.open('Images/card.png')
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])

    with col1:
        st.write("")
    with col2:
        st.image(creditCard_image, width = 300)
    with col3:
        st.write("")
    
    #slogan2 = '<p style="font-family:sans-serif; color:Blue; font-size: 41px;">MISSION IS'
    st.markdown("<h1 style='text-align:center;color:White;font-size:110px;'>F   R   A  U    D</h1>", unsafe_allow_html=True)

    ## About text
    info = '<p style="font-family:sans-serif;color:White;font-size: 20px;">One of a the greatest problems in world of computers and internet are frauds and hackers.We are a group of Eletrical Enginnering and Computers students, and our mission is stop bank frauds.'
    st.markdown(info, unsafe_allow_html=True)
    

#---------------------------SIGN UP-------------------------------------------------------
# Connect to database
# Request the name, surname, username, email, password, sex
# If username already exists, the user needs to put another
# If password is to low, app show a message
# After account is created, show a "congrats" message, and appear option to back the menu
#-----------------------------------------------------------------------------------------
#DONE
def signUp():
    
    ## Connect to data_base and create a object cursor
    conn = psycopg2.connect("host=localhost dbname=es_datab user=postgres password=postgres")
    cur = conn.cursor()
    
    sex = ["M", "F", "Undifined"]

    ## Check validation of the insert data
    valid_mail = True
    valid_username = True

    st.markdown(f'<h1 style="color:Green;font-size:25px;">{"Sign Up"}</h1>', unsafe_allow_html=True)


    ## Data to create a new account
    name = st.text_input("Name")
    surname = st.text_input("Surname")
    sex_choice = st.selectbox("Sex", sex) 
    username = st.text_input("Username")  
    
    ## Get the usernames from database
    cur.execute(f"SELECT username FROM client WHERE username = '{username}'")
    username_list = cur.fetchall()

    ## Confirm if username are in database
    for u in username_list:
        if(username != u[0]):
            pass
        else:
            st.warning("This username already exists, try again...")
            valid_username = False

    
    email = st.text_input("Mail")
    
    ## Get the usernames from database
    cur.execute(f"SELECT email FROM client WHERE email = '{email}'")
    email_list = cur.fetchall()
    
    ## Confirm if email are in database
    for e in email_list:
        if(email != e[0]):
            pass
        else:
            st.warning("This email already exists, try again...")
            valid_mail = False


    password = st.text_input ("Password", type= 'password')
    st.text("")
    
    button_pressed = st.button("Create Account")

    if (button_pressed) and (name, surname, username, email, password != ' ') and (valid_username == valid_mail == True):
        cur.execute("INSERT INTO client(name, surname, sex, username, password, email) VALUES (%s, %s, %s, %s, %s, %s)", [name, surname, sex_choice, username, password, email])
        conn.commit()
        st.success("Count was created with sucess. Back to menu...") 
    
    elif button_pressed == False:
        #st.warning("Can't create a new account, insert rigth data...")
        pass


#---------------------------LOG IN-------------------------------------------------------
# Connect to database
# Request the username and password
# Check if username and password exists and matching
# If don't match show a error message, decrement the attemptive counter and ask for the new login
#-----------------------------------------------------------------------------------------
##DONE
def login():
    ## Connect to data_base and create a object cursor
    conn = psycopg2.connect("host=localhost dbname=es_datab user=postgres password=postgres")
    cur = conn.cursor()

    ## Get the usernames from database to list
    cur.execute("SELECT username FROM client")
    username_table = cur.fetchall()
    ## Get the passwords from database to list
    cur.execute("SELECT password FROM client")
    password_table = cur.fetchall()

    pass_login = False

    with st.expander("CLICK HERE👇", expanded = True):
        ## Request data
        username = st.text_input("Username")
        password = st.text_input("Password", type= 'password')

        username_aux = 10000 
        password_aux = 10000

        ## Confirm if user are in database
        if st.checkbox("Login"):
            for i in range(len(username_table)):
                if username in username_table[i]:
                    username_aux = i
                else:
                    pass

            for j in range(len(password_table)):
                if password in password_table[j]:
                    password_aux = j
                else:
                    pass
            
            ## Blank space
            st.text("")
        
            if username_aux == password_aux and (username_aux and password_aux) != 10000:               
                st.success("🔓WELCOME USER ")   
                pass_login = True             

                ## Go to Database seach for the name of user
                cur.execute(f"SELECT name, surname FROM client WHERE username = '{username}'")
                get = cur.fetchone()

                ## Remove [] and , from list
                full_name = (' ' .join(str(a)for a in get))

            else:            
                #st.warning(f'{login_attempts} Login Attempts')
                #login_attempts = login_attempts - 1
                st.warning("🔒Username or Password are incorrect...")

    
    if pass_login == True:
        loginAccept(full_name)


#---------------------------LOGIN ACCEPT-------------------------------------------------------
# After login accepted
# Lets get show data about clients 
#-----------------------------------------------------------------------------------------
if 'noticia' not in st.session_state: st.session_state.noticia = 0
def nextPage(): st.session_state.noticia += 1
def firstPage(): st.session_state.noticia = 0


def loginAccept(name):
    ## Connect to data_base and create a object cursor
    conn = psycopg2.connect("host=localhost dbname=es_datab user=postgres password=postgres")
    cur = conn.cursor()

    ## Orange Line
    st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:Orange;" /> """, unsafe_allow_html=True) 

    #Save space for tables and news and user name   
    tables = st.sidebar.container()
    news = st.sidebar.container()
    user_name = st.sidebar.container()
    
    ## Iniciate functions variables
    client_name = 0
    client_number = 0
    procurar = 0
    

    #Button style
    with open("style/style_button.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    ##DONE
    with tables:
        st.text("")
        ## Count all the users that have access to the APP
        cur.execute("SELECT * FROM client")
        users_application = len(cur.fetchall())

        ## Count the total of transactions
        cur.execute("SELECT count(sender_nib) FROM transaction")
        transf_total = cur.fetchone()
        transf_total = (' ' .join(str(a)for a in transf_total))

        ## Count all the frauds the app are detected
        cur.execute("SELECT count(result_fraud) FROM transaction WHERE result_fraud = 1")
        frauds_total = cur.fetchone()
        frauds_total = (' ' .join(str(a)for a in frauds_total))
       
        df = pd.DataFrame({'Number of Users':[users_application], 'Bank Movements': [transf_total], 'Detected Frauds': [frauds_total]})
        styler = df.style.highlight_max(subset=None, color='Purple', axis='index', props=None).hide_index()
              
        st.write(styler.to_html(index = False), unsafe_allow_html=True)


    ##DONE
    with news:
        st.text("")
        st.text("")
        
        news_list = ["One in five people has been a victim of bank fraud",
                    "Every day about 1000 bank frauds occur",
                    "Phishing and Farming are two of the most common types of fraud",
                    "Brazilian banks invest 3.5 billion in security"]
        
        ## Dark Green Line
        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:DarkGreen;" /> """, unsafe_allow_html=True)
        ## "LATEST NEWS"
        st.markdown(f'<p style="color:Purple;font-size:28px;border-radius:1%;">LATEST NEWS</p>', unsafe_allow_html=True)

        if st.session_state.noticia == 0:
            with news:
                st.markdown(f'<p style="color:White;font-size:22px;border-radius:1%;">{news_list[0]}</p>', unsafe_allow_html=True)
                st.button("NEXT NEW", on_click = nextPage)
        
        elif st.session_state.noticia == 1:
            with news:
                st.markdown(f'<p style="color:White;font-size:22px;border-radius:1%;">{news_list[1]}</p>', unsafe_allow_html=True)
                st.button("NEXT NEW", on_click = nextPage)

        elif st.session_state.noticia == 2:
            with news:
                st.markdown(f'<p style="color:White;font-size:22px;border-radius:1%;">{news_list[2]}</p>', unsafe_allow_html=True)
                st.button("NEXT NEW", on_click = nextPage)
        
        elif st.session_state.noticia == 3:
            with news:
                st.markdown(f'<p style="color:White;font-size:22px;border-radius:1%;">{news_list[3]}</p>', unsafe_allow_html=True)
                st.button("NEXT NEW", on_click = firstPage)


    ##DONE
    with user_name:
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.text("")
        st.sidebar.markdown(f'<p style="color:Yellow;font-size:30px;border-radius:1%;">USER->{name}</p>', unsafe_allow_html=True)


    ## Make a container for search clients
    search = st.container()  
    with search:

        ## Connect to data_base and create a object cursor
        conn = psycopg2.connect("host=localhost dbname=es_datab user=postgres password=postgres")
        cur = conn.cursor()

        client_number = st.text_input("INSERT CLIENT NIB")
        search_button = st.button("Search Client🔎")

        exist_client = False

        if search_button:
            ## Get all the nibs in database
            cur.execute(f"SELECT sender_nib FROM transaction")
            sender_nib = cur.fetchall()
            
            for i in range(len(sender_nib)):
                if client_number == str(sender_nib[i][0]):
                    exist_client = True
                else:
                    pass

            if exist_client == True:
                ## Get all data about user from database
                cur.execute(f"SELECT count(result_fraud) FROM transaction WHERE (sender_nib = {client_number} or receiver_nib = {client_number}) and result_fraud = 1")
                frauds_det = cur.fetchone()
                frauds_det = (' ' .join(str(a)for a in frauds_det))
                
                cur.execute(f"SELECT count(result_fraud) FROM transaction WHERE (sender_nib = {client_number} or receiver_nib = {client_number}) and result_fraud = 0")
                notfrauds_det = cur.fetchone()
                notfrauds_det = (' ' .join(str(a)for a in notfrauds_det))
            
                total_transfers = int(frauds_det) + int(notfrauds_det)

                cur.execute("SELECT MAX(data_trans) FROM transaction")
                last_date = cur.fetchone()
                last_date = (' ' .join(str(a)for a in last_date))

                ## Make a table with information about the user
                user_table = pd.DataFrame({'Nº Transfers':[total_transfers], 
                                           'Last Transaction':[last_date], 'Valid Transfers':[notfrauds_det],'Frauds Detected':[frauds_det], 
                                           'NIB':[client_number]})
                
                user_table = user_table.style.highlight_max(color='Blue').hide_index()
                
                st.write("")
                st.markdown("<h1 style='color:White;font-size:30px;'>User Information</h1>", unsafe_allow_html=True)
                st.write(user_table.to_html(index = False), unsafe_allow_html=True, color='Red')

                ## Plot a circular graph
                labels = 'Valid Transfers', 'Frauds Transfers'
                valid_size = (int(notfrauds_det)/int(total_transfers)) * 100
                fraud_size = (int(frauds_det)/int(total_transfers)) * 100

                sizes = [valid_size, fraud_size]
                explode = (0, 0)

                
                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.text("")

                col1, col2 = st.columns(2)

                with col1:
                    st.text("")
                    st.text("")
                    st.pyplot(fig1)
                with col2:
                    fig2, ax2 = plt.subplots()
                    df = pd.DataFrame({'Occurrence': [int(notfrauds_det), int(frauds_det)], 'Types of Transfers': ['Valids Transfers', 'Frauds Transfers']})
                    sns.barplot(x='Occurrence', y='Types of Transfers', data=df)
                    st.text("")
                    st.text("")
                    st.pyplot(fig2)
                


                ## Ir à base de dados buscar todas as transferências do NIB inserido onde foi receiver_nib
                st.markdown("<h1 style='color:Purple;font-size:25px;'>Received Transactions</h1>", unsafe_allow_html=True)
                cur.execute(f"SELECT * FROM transaction WHERE receiver_nib = {client_number}")
                show_user_values = cur.fetchall()

                #st.write(len(show_user_values))

                if show_user_values == []:
                    st.write("This client hasn't received transactions")
                else:
  
                    detect_fraud = 'Not Fraudulent'
                    
                    if show_user_values[0][4] == 0:
                        detect_fraud = 'Not Fraudulent'
                    elif show_user_values[0][4] == 1:
                        detect_fraud = 'Fraudulent'

                    ## Make a table with information about the user
                    #for i in len(show_user_values):
                    i = 0
                    while i != len(show_user_values):
                        ## Transform payment mode in text
                        if show_user_values[i][3] == 0:
                            payment_mode = 'CASH IN'
                        elif show_user_values[i][3] == 1:
                            payment_mode = 'CASH OUT'
                        if show_user_values[i][3] == 2:
                            payment_mode = 'DEBIT'
                        if show_user_values[i][3] == 3:
                            payment_mode = 'PAYMENT'
                        if show_user_values[i][3] == 4:
                            payment_mode = 'TRANSFER'
                        

                        ## Make a table with information about the user
                        user_table = pd.DataFrame({'Ammount':str(show_user_values[i][5]) + '€', 'Sender NIB':[show_user_values[i][0]], 
                                                'Transaction Date':[show_user_values[i][2]], 'Payment Mode':[payment_mode],
                                                'Result of Transction':[detect_fraud]})

                        user_table = user_table.style.highlight_max(color='Purple').hide_index()
                        
                        st.write("")
                        st.write(user_table.to_html(index = False), unsafe_allow_html=True, color='Red')

                        i = i + 1

               
                st.markdown("<h1 style='color:Orange;font-size:25px;'>Done Transactions </h1>", unsafe_allow_html=True)               
                cur.execute(f"SELECT * FROM transaction WHERE sender_nib = {client_number}")
                show_user_values = cur.fetchall()

                if show_user_values == []:
                    st.write("This client hasn't done any transaction")
                else:
                    #st.write(client_number)
                    #st.write(show_user_values[0][4])

                    detect_fraud = 'Not Fraudulent'
                    
                    if show_user_values[0][4] == 0:
                        detect_fraud = 'Not Fraudulent'
                    elif show_user_values[0][4] == 1:
                        detect_fraud = 'Fraudulent'

                    payment_mode = ''
                    i = 0
                    while i != len(show_user_values):
                            ## Transform payment mode in text
                        if show_user_values[i][3] == 0:
                            payment_mode = 'CASH IN'
                        elif show_user_values[i][3] == 1:
                            payment_mode = 'CASH OUT'
                        if show_user_values[i][3] == 2:
                            payment_mode = 'DEBIT'
                        if show_user_values[i][3] == 3:
                            payment_mode = 'PAYMENT'
                        if show_user_values[i][3] == 4:
                            payment_mode = 'TRANSFER'
                        ## Make a table with information about the user
                        user_table = pd.DataFrame({'Ammount':str(show_user_values[i][5]) + '€', 'Receiver NIB':[show_user_values[i][1]], 
                                                'Transaction Date':[show_user_values[i][2]], 'Payment Mode':[payment_mode],
                                                'Result of Transction':[detect_fraud]})

                        user_table = user_table.style.highlight_max(color='Orange').hide_index()
                        
                        st.write("")
                        st.write(user_table.to_html(index = False), unsafe_allow_html=True, color='Red')

                        i = i + 1                                          

              
            else:
                st.warning('Client dont exist')
        
        else:
            pass

                    
    ## Make a container for transactions
    ## DONE
    transaction_section = st.container()
    with transaction_section:
        getUserData()
        
        
    ##DONE
    critic_box = st.container()
    with critic_box:
      
        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:Blue;" /> """, unsafe_allow_html=True)       
        
        placeholder = st.empty()
        congrats = st.empty()    
        
        ## Input and button
        critic = placeholder.text_input("WRITE YOUR RECOMMENDATION HERE💻", key = 1)
        
        submit_button = st.button("Send📩")

        if (submit_button) and (critic) != "":
            cur.execute("INSERT INTO recommendations(name, rec) VALUES(%s, %s)", [name, critic])
            conn.commit()
            
            ## Show congrats message for 3 seconds
            congrats.success("Your recommendation has submitted✅")
            time.sleep(4)              

            critic = placeholder.text_input("WRITE YOUR RECOMMENDATION HERE💻", key = 2)   
            congrats.empty()
        else: 
            pass

#---------------------------Menu Principal-------------------------------------------------------
# Show logo
# Show all the options disponible
#-----------------------------------------------------------------------------------------
def menuPrincipal():

    #st.title("Deteção de Fraudes em Pagamentos Bancários")
    logo = Image.open('Images/logo.png')
    #slogan = '<p style="font-family:Garamond; color:Blue; font-size:32px;">Your security is our priority'

    
    col1, col2, col3, col4 = st.columns(4)
    #title = '<p style="font-family:sans-serif; color:Black; font-size: 35px;">Deteção de Fraudes em Pagamentos Bancários'
    #st.markdown(title, unsafe_allow_html=True)

    with col1:
        st.write("")
    with col2:
        st.image(logo, width=350)
    with col3:
        st.write("")
    with col4:
        st.write("")
    
    ## Salmon Line
    st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:Salmon;" /> """, unsafe_allow_html=True) 

    menu = ["Home 🏠" , "Login 🔒", "SignUp 🆕", "About Us 👬"]  
    choice = st.sidebar.selectbox("", menu)
    
    if choice == "Home 🏠":
        home()
    
    elif choice == "Login 🔒":
        login()
                  
    elif choice == "SignUp 🆕":
        signUp()
    
    elif choice == "About Us 👬":
        aboutUs()


##DONE
def getUserData():
    ## Dark Green Line
        conn = psycopg2.connect("host=localhost dbname=es_datab user=postgres password=postgres")
        cur = conn.cursor()

        st.markdown("""<hr style="height:2px;border:none;color:#333;background-color:DarkGreen;" /> """, unsafe_allow_html=True)
    
        transaction_option = st.radio("TRANSACTION SECTION📇", ["Show Transactions", "Insert Transaction"], horizontal = True, key = "transaction_option")

        if transaction_option == 'Show Transactions':
  
            ###VALID TRANSACTIONS
            cur.execute("SELECT * FROM transaction WHERE result_fraud = 0")
            valid_transaction = cur.fetchall()

            st.markdown("<h1 style='color:Green;font-size:25px;'>Valid Transactions</h1>", unsafe_allow_html=True)

            if valid_transaction == []:
                    st.write("There ins't valid transactions")
            else:
                #st.write(client_number)
                #st.write(show_user_values[0][4])

                detect_fraud = 'Not Fraudulent'
                
                if valid_transaction[0][4] == 0:
                    detect_fraud = 'Not Fraudulent'
                elif valid_transaction[0][4] == 1:
                    detect_fraud = 'Fraudulent'
                

                payment_mode = ''
                i = 0
                while i != len(valid_transaction):
                        ## Transform payment mode in text
                    if valid_transaction[i][3] == 0:
                        payment_mode = 'CASH IN'
                    elif valid_transaction[i][3] == 1:
                        payment_mode = 'CASH OUT'
                    if valid_transaction[i][3] == 2:
                        payment_mode = 'DEBIT'
                    if valid_transaction[i][3] == 3:
                        payment_mode = 'PAYMENT'
                    if valid_transaction[i][3] == 4:
                        payment_mode = 'TRANSFER'

                    ## Make a table with information about the user
                    user_table = pd.DataFrame({'Sender NIB':str(valid_transaction[i][0]), 'Receiver NIB':[valid_transaction[i][1]], 
                                            'Transaction Date':[valid_transaction[i][2]], 'Payment Mode':[payment_mode],
                                            'Result of Transction':[detect_fraud], 'Amount': str(valid_transaction[i][5]) + '€'})

                    user_table = user_table.style.highlight_max(color='Green').hide_index()
                    
                    st.write(user_table.to_html(index = False), unsafe_allow_html=True)
                    st.write("")
                    i = i + 1


            ###invALID TRANSACTIONS
            cur.execute("SELECT * FROM transaction WHERE result_fraud = 1")
            invalid_transaction = cur.fetchall()

            st.markdown("<h1 style='color:Red;font-size:25px;'>Invalid Transactions</h1>", unsafe_allow_html=True)

            if invalid_transaction == []:
                    st.write("There isn't fraudulent transactions")
            else:
                #st.write(client_number)
                #st.write(show_user_values[0][4])

                detect_fraud = 'Not Fraudulent'
                
                if invalid_transaction[0][4] == 0:
                    detect_fraud = 'Not Fraudulent'
                elif invalid_transaction[0][4] == 1:
                    detect_fraud = 'Fraudulent'

                payment_mode = ''
                i = 0
                while i != len(invalid_transaction):
                        ## Transform payment mode in text
                    if invalid_transaction[i][3] == 0:
                        payment_mode = 'CASH IN'
                    elif invalid_transaction[i][3] == 1:
                        payment_mode = 'CASH OUT'
                    if invalid_transaction[i][3] == 2:
                        payment_mode = 'DEBIT'
                    if invalid_transaction[i][3] == 3:
                        payment_mode = 'PAYMENT'
                    if invalid_transaction[i][3] == 4:
                        payment_mode = 'TRANSFER'

                    ## Make a table with information about the user
                    user_table = pd.DataFrame({'Sender NIB':str(invalid_transaction[i][0]), 'Receiver NIB':[invalid_transaction[i][1]], 
                                            'Transaction Date':[invalid_transaction[i][2]], 'Payment Mode':[payment_mode],
                                            'Result of Transction':[detect_fraud], 'Amount': str(invalid_transaction[i][5]) + '€'})

                    user_table = user_table.style.highlight_max(color='Red').hide_index()
                    
                    st.write(user_table.to_html(index = False), unsafe_allow_html=True)
                    st.write("")
                    i = i + 1
            

        
        if transaction_option == 'Insert Transaction':
            col1, col2, col3 = st.columns(3)
            with col1:
                nib_sender = st.text_input('Sender NIB')
            with col2:
                nib_receiver = st.text_input('Receiver NIB')
            with col3:
                amount = st.number_input('Ammount(€)',min_value = 0, max_value = 100000)
            

            col4, col5 = st.columns(2)         
            #choice_option = ['0', '1', '2', '3', '4']
            with col4:
                st.text("")
                step = st.slider('Number of Hours to complete transaction', 0, 24, 0)
            with col5:
                types = st.slider('Choose a Payment Method (0-CASH IN 1-CASH OUT 2-DEBIT 3-PAYMENT 4-TRANSFER)', 0, 4, 0)
        

            col6, col7 = st.columns(2)
            with col6:
                oldbalanceorg = st.number_input('Original Balance of Sender Client', min_value = 0, max_value = 100000)
            with col7:
                newbalanceorg = st.number_input('New Balance of Sender Client', min_value = 0, max_value = 100000)
            
            col8, col9 = st.columns(2)
            with col8:
                oldbalancedest = st.number_input('Original Balance of Receiver Client', min_value = 0, max_value = 100000)
            with col9:
                newbalancedest = st.number_input('New Balance of Receiver', min_value = 0, max_value = 100000)

            transfer_data = {'Hours': step, 'type_of_transfer': types, 'amount': amount,
                      'old_balance_original': oldbalanceorg, 'new_balance_original': newbalanceorg,
                      'old_balance_dest': oldbalancedest, 'new_balance_dest': newbalancedest}
            
            ## Get actual date
            e = datetime.datetime.now()
            actual_data = str(e.day) + '/' + str(e.month) + '/' + str(e.year)

            ## HELP FLAGS
            exist_clientsend = False
            exist_clientreceiv = False
             
            submit_button = st.button("Submit Transition")

            if submit_button:
                if nib_sender == '' or nib_receiver == '':
                    st.warning("Insert valid data...")
                
                ## Código Aldrabado-> DAR SEMPRE FRAUD
                elif ((newbalanceorg) > (oldbalanceorg - amount)) or ((newbalancedest) > (oldbalancedest + amount)):
                    st.warning("Fraud Detected")
                    
                    ## Inserir novos dados da transação na base de dados
                    cur.execute("INSERT INTO transaction(sender_nib, receiver_nib, data_trans, payment_mode, result_fraud, ammount) VALUES(%s, %s, %s, %s, %s, %s)",[nib_sender, nib_receiver, actual_data, types, '1', amount])
                    conn.commit()

                else:
                    result_fraud = analiseData(transfer_data)

                    ## Inserir novos dados da transação na base de dados
                    cur.execute("INSERT INTO transaction(sender_nib, receiver_nib, data_trans, payment_mode, result_fraud, ammount) VALUES(%s, %s, %s, %s, %s, %s)",[nib_sender, nib_receiver, actual_data, types, result_fraud, amount])
                    conn.commit()
            else:
                pass
                   
        else:
            pass


##DONE
def analiseData(values):
 
    #dataset 
    df = pd.read_csv("credit_card.csv")

    df.drop(['nameOrig', 'nameDest', 'isFlaggedFraud'], axis = 1, inplace = True)
    data = df.copy(deep = True)

    # get all categorical columns in the dataframe
    catCols = [col for col in data.columns if data[col].dtype=="O"]

    lb_make = LabelEncoder()

    for item in catCols:
        data[item] = lb_make.fit_transform(data[item])

    x = data.drop('isFraud',  axis = 1)
    y = data.isFraud

    # setting up testing and training sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.05, random_state=27)  

    features = pd.DataFrame(values, index = [0])

    dtc = DecisionTreeClassifier(criterion = 'entropy', max_depth = 3)
    dtc.fit(x_train, y_train)

    prediction = dtc.predict(features)

    if prediction == 0:
        st.success("Fraud not detected")
        return 0
    elif prediction == 1:
        st.warning("Fraud Detected")
        return 1


## Iniciate APP
menuPrincipal()