import pandas as pd
import mysql.connector as sql
from mysql.connector import Error
import pytesseract
from PIL import Image
import re
import streamlit as st
import io

#Create mySQL function to run the queries
def create_server_connection(host_name,user_name,user_password):
    connection=None
    try:
        connection=sql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password)
    except Error:
        1
    return connection

def create_database(connection,query):
    mycursor=connection.cursor()
    try:
        mycursor.execute(query)
    except Error:
        1

def create_database_connection(host_name,user_name,user_password,db_name):
    connection=0
    try:
        connection=sql.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name)
    except Error:
        1
    return connection

#Connect to SQL Database
#host=input('Provide host name to connect to SQL Database: ')
#user=input('Provide user name to connect to SQL Database: ')
#password=input('Provide user password to connect to SQL Database: ')
host='localhost'
user='root'
password='Akash@1999'
connection=create_server_connection(host,user,password)

#Define database name
db_name='bizcardx'
database_query=f"create database if not exists {db_name}"
create_database(connection,database_query)

connection=create_database_connection(host,user,password,db_name)

mycursor=connection.cursor(buffered=True)

#Incase the table needs to be dropped
#mycursor.execute(
#    """drop table card_data"""
#    )

#Define the table in sql if not exists    
mycursor.execute(
    """create table if not exists card_data(UID int, Company_Name TEXT,
    Name TEXT, Designation TEXT, Phone1 TEXT, Phone2 TEXT, Email TEXT,
    Website TEXT, Area TEXT, City TEXT, State TEXT, Pincode TEXT,
    Image LONGBLOB, MaxID int)"""
    )

pytesseract.pytesseract.tesseract_cmd = (
    r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    )

st.write('# OCR Card Reader')

#Upload the image
img=Image.open('Test cards/1.png')
image=st.file_uploader('Upload a png or a jpg file',type=['png','jpg'])
if image is not None:
    img=Image.open(image)
st.write('### Uploaded image:')
st.image(img)

#Use OCR to read image
info=pytesseract.image_to_string(img)

#Dissect the read data into useful information and display in textboxes
#User can update the textboxes if OCR detection is innaccurate
name_pattern = r"([A-Za-z]+)"
name_match = re.search(name_pattern, info)
name = name_match.group() if name_match else "Not found"
info=info.replace(name,'')

email_pattern = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
email_match = re.search(email_pattern, info)
email_address = email_match.group() if email_match else "Not found"
info=info.replace(email_address,'')

site_pattern = r"([a-zA-Z0-9_.+-]+\.[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
site_match = re.search(site_pattern, info)
site = site_match.group() if site_match else "Not found"
info=info.replace(site,'')

phone_pattern1 = r"\+\d{2,3}-\d{3}-\d{4}"
phone_match1 = re.search(phone_pattern1, info)
phone_number1 = phone_match1.group() if phone_match1 else "Not Found"
info=info.replace(phone_number1,'')

phone_pattern2 = r"\+\d{2,3}-\d{3}-\d{4}"
phone_match2 = re.search(phone_pattern2, info)
phone_number2 = phone_match2.group() if phone_match2 else "Not Found"
info=info.replace(phone_number2,'')

desig_pattern = r"([A-Za-z ]+)"
desig_match = re.search(desig_pattern, info)
desig = desig_match.group() if desig_match else "Not found"
info=info.replace(desig,'')

pin_pattern = r"(\d{6,7})"
pin_match = re.search(pin_pattern, info)
pin = pin_match.group() if pin_match else "Not found"
info=info.replace(pin,'')

info=info.replace('\n','')
address=info.split(',')

if len(address)>2:
    Area=address[0].strip()
    City=address[1].strip()
    State=address[2].strip()
elif len(address)==2:
    Area=address[0].strip()
    City=address[1].strip()
    State="Not found"
else:
    Area=address[0].strip()
    City="Not found"
    State="Not found"

s1=set(re.split(r"[.@]",site))
s2=set(re.split(r"[.@]",email_address))
s_common=list(s1 & s2)
if len(s_common)==0:
    Company="Not found"
else:
    Company=s_common[0]
    for word in s_common:
        if len(word)>=len(Company):
            Company=word

st.write('### Card details:')
Company=st.text_input('Company Name:',Company)

#Now display all the extracted information
col1,col2=st.columns(2)
with col1:
    name=st.text_input('Name:',name)

with col2:
    desig=st.text_input('Designation:',desig)

col1,col2=st.columns(2)
with col1:
    phone_number1=st.text_input('Phone no. 1:',phone_number1)

with col2:
    phone_number2=st.text_input('Phone no. 2:',phone_number2)

col1,col2=st.columns(2)
with col1:
    email_address=st.text_input('Email ID:',email_address)

with col2:
    site=st.text_input('Webpage:',site)

col1,col2=st.columns(2)
with col1:
    Area=st.text_input('Area:',Area)

with col2:
    City=st.text_input('City:',City)

col1,col2=st.columns(2)
with col1:
    State=st.text_input('State:',State)

with col2:
    pin=st.text_input('Pincode:',pin)

submit=st.button('Add to Database')

#User can opt to submit so information can be added to the Database
if submit:
    mycursor.execute(
        """select max(MaxID) from card_data"""
        )
    temp=mycursor.fetchone()[0]
    if temp is None:
        UID=1
    else:
        UID=temp+1
    
    bytes_io = io.BytesIO()
    img.save(bytes_io, format='PNG')
    sql_img=bytes_io.getvalue()
    bytes_io.close()
    
    mycursor.execute(
         """insert into card_data(UID, Company_name, Name, Designation,
         Phone1, Phone2, Email, Website, Area, City, State, Pincode,
         Image, MaxID)
    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    (UID,Company, name, desig, phone_number1, phone_number2, email_address,
     site, Area, City, State, pin, sql_img, UID)
         )
    connection.commit()
    mycursor.execute(
        f"update card_data set MaxID = '{UID}'")
    connection.commit()
    
    st.success(f'Unique ID {UID} generated and uploaded!')

#User can select the UID of a past scan to either Update/Delete
mycursor.execute(
    """select * from card_data"""
    )
rows=mycursor.fetchall()
connection.commit()
column_names = [desc[0] for desc in mycursor.description]
data = pd.DataFrame(rows, columns=column_names)

UID_list=data['UID'].tolist()

st.write('## Information Update/Delete:')
selected_ID=st.selectbox(
    'Select the UID of data you want to Update/Delete:',
    UID_list
    )


mycursor.execute(
    """select Image from card_data where UID=%s""",
    (selected_ID,)
    )
img1_data=mycursor.fetchone()
connection.commit()
if img1_data==None:
    img1=1
else:
    img1=Image.open(io.BytesIO(img1_data[0]))

#Display all the data of the selected UID
if img1!=1:
    st.write(f'Details of selected ID (UID no. {selected_ID}):')
    st.write('#### Uploaded Image:')
    st.image(img1)

    Company1=st.text_input(
        'Company Name: ',
        data.loc[data['UID']==selected_ID,'Company_Name'].values[0]
        )

    col1,col2=st.columns(2)
    with col1:
        name1=st.text_input(
            'Name: ',
            data.loc[data['UID']==selected_ID,'Name'].values[0]
            )

    with col2:
        desig1=st.text_input(
            'Designation: ',
            data.loc[data['UID']==selected_ID,'Designation'].values[0]
            )

    col1,col2=st.columns(2)
    with col1:
        phone_number1_1=st.text_input(
            'Phone no. 1: ',
            data.loc[data['UID']==selected_ID,'Phone1'].values[0]
            )

    with col2:
        phone_number2_1=st.text_input(
            'Phone no. 2: ',
            data.loc[data['UID']==selected_ID,'Phone2'].values[0]
            )

    col1,col2=st.columns(2)
    with col1:
        email_address1=st.text_input(
            'Email ID: ',
            data.loc[data['UID']==selected_ID,'Email'].values[0]
            )
    
    with col2:
        site1=st.text_input(
            'Webpage: ',
            data.loc[data['UID']==selected_ID,'Website'].values[0]
            )
    
    col1,col2=st.columns(2)
    with col1:
        Area1=st.text_input(
            'Area: ',
            data.loc[data['UID']==selected_ID,'Area'].values[0]
            )
    
    with col2:
        City1=st.text_input(
            'City: ',
            data.loc[data['UID']==selected_ID,'City'].values[0]
            )
    
    col1,col2=st.columns(2)
    with col1:
        State1=st.text_input(
            'State: ',
            data.loc[data['UID']==selected_ID,'State'].values[0]
            )
    
    with col2:
        pin1=st.text_input(
            'Pincode: ',
            data.loc[data['UID']==selected_ID,'Pincode'].values[0]
            )
    
    col1,col2=st.columns(2)
    
    #User can choose to update record
    with col1:    
        if st.button('Update Details'):
            mycursor.execute(
                """update card_data set Company_Name=%s, Name=%s, Designation=%s,
                Phone1=%s, Phone2=%s, Email=%s, Website=%s, Area=%s, City=%s,
                State=%s, Pincode=%s where UID=%s""",
                (Company1, name1, desig1, phone_number1_1, phone_number2_1,
                 email_address1, site1, Area1, City1, State1, pin1, selected_ID)
                )
            connection.commit()
            st.success('Details Updated!')
    
    #User can choose to delete record
    with col2:
        if st.button('Delete record'):
            mycursor.execute(
                f"""delete from card_data where UID={selected_ID}"""
                )
            connection.commit()
            st.success('Record deleted!')
    
    #Display the database
    mycursor.execute(
        """select * from card_data"""
        )
    rows=mycursor.fetchall()
    connection.commit()
    column_names = [desc[0] for desc in mycursor.description]
    data = pd.DataFrame(rows, columns=column_names)
    
    st.write('## Database:')
    st.dataframe(data.iloc[:,:-2])

else:
    st.warning('### Database is currently empty!')