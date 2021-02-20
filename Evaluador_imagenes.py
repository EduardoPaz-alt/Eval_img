import streamlit as st
import os
import pandas as pd
import re
import string
import warnings
import csv
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import sqlite3
from sqlite3 import Connection
warnings.filterwarnings('ignore')
#from session_state import SessionState
import SessionState
#from streamlit.ScriptRunner import StopException, RerunException

################ Evaluador

URI_SQLITE_DB = "test_img.db"
def main():
    st.title("Evaluación")
    st.write("Califica y no olvides salvar tus datos")
    
    conn = get_connection(URI_SQLITE_DB)
    init_db(conn)
    #build_inputs(conn)
    build_sidebar(conn)
    display_data(conn)
    #run_file(conn)
    #run_calculator(conn)

def init_db(conn: Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS test_img
            (
                INPUT1 INT,
                INPUT2 INT,
                INPUT3 INT,
                INPUT4 INT
            );"""
    )
    conn.commit()

def build_sidebar(conn: Connection):
    #st.sidebar.header("Configuration")
    input1 = st.sidebar.radio("¿Es un meme?", ('Si', 'No'))
    if input1 == "Si":
        input1 = 1
    else:
        input1 = 2
        
    input2 = st.sidebar.radio("¿Qué emoción te provoca?", ('alegria', 'confianza', 'miedo', 'sorpresa', 'tristeza', 'aversión', 'ira', 'anticipación'))
    if input2 == 'alegría':
        input2 = 1
    elif input2 == 'confianza':
        input2 = 2
    elif input2 == 'miedo':
        input2 = 3    
    elif input2 == 'sorpresa':
        input2 = 4    
    elif input2 == 'tristeza':
        input2 = 5
    elif input2 == 'aversión':
        input2 = 6
    elif input2 == 'ira':
        input2 = 7
    else:
        input2 = 8
    
    input4 = st.sidebar.radio("Calificador:", ('AnaLee', 'Angel', 'Eduardo', 'Eloy', 'Mariel', 'Nelly', 'Paola'))
    if input4 == 'AnaLee':
        input4 = 1
    elif input4 == 'Angel':
        input4 = 2
    elif input4 == 'Eduardo':
        input4 = 3    
    elif input4 == 'Eloy':
        input4 = 4    
    elif input4 == 'Mariel':
        input4 = 5
    elif input4 == 'Nelly':
        input4 = 6
    else:
        input4 = 7
    
    if st.sidebar.button("Guardar en DB"):
        conn.execute(f"INSERT INTO test_img (INPUT1, INPUT2, INPUT3, INPUT4) VALUES ({input1}, {input2}, {input3}, {input4})")
        conn.commit()
        st.write('======GUARDADO====')
        st.write({input1}, {input2}, {input3}, {input4})

#def run_file(conn: Connection):

tweetdf = pd.read_csv('tabladogs.csv')
tweetdf = pd.DataFrame(tweetdf)
#st.write(tweetdf)

####
## Obtiene un mensaje de la base de pandas
pd.set_option('max_colwidth', 8000)
tweetdf['númber'] = tweetdf.reset_index().index
pd_random = tweetdf.sample(n = 1)
pd_random = pd.DataFrame(pd_random)
#st.write(pd_random)
txt = pd_random._get_value(0,2, takeable = True)
#st.write(txt)
rw_number = pd_random._get_value(0,4, takeable = True)
rw_calif = 'Eduardo'


img = Image.open(txt)
#st.image(img, caption='Sunrise by the mountains', use_column_width=True)
# Save the resulting image
session_state = SessionState.get(img = img, rw_number=rw_number, rw_calif = rw_calif)
img.save('result.png')
session_state = SessionState.get(name='', img=None)
my_image = session_state.img
st.image(my_image, channels='BGR', use_column_width=True)
##
input3 = session_state.rw_number
##
input4 = session_state.rw_calif
##
def display_data(conn: Connection):
    if st.checkbox("Muestra la base de datos"):
        st.dataframe(get_data(conn))

def get_data(conn: Connection):
    df = pd.read_sql("SELECT * FROM test_img", con=conn)
    return df


@st.cache(hash_funcs={Connection: id})
def get_connection(path: str):
    """Put the connection in cache to reuse if path does not change between Streamlit reruns.
    NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    """
    return sqlite3.connect(path, check_same_thread=False)


if __name__ == "__main__":
    main()
