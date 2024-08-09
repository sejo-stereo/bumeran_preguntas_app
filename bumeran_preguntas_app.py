import streamlit as st
import requests
from random import randint
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Preguntas Bumeran", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

load_dotenv()

scrape_api = os.getenv("SCRAPEOPS_API_KEY")

def get_headers_list():
  response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + scrape_api)
  json_response = response.json()
  return json_response.get('result', [])

def get_random_header(header_list):
  random_index = randint(0, len(header_list) - 1)
  randomHeader = header_list[random_index]
  randomHeader["referer"] = "https://www.bumeran.com.pe/empleos/asistente-contable-rsm-peru-1116412339.html"
  randomHeader["x-site-id"] = "BMPE"
  return randomHeader

def consultar_preguntas(link_id):
    header_list = get_headers_list()
    link_id = link_id[-15:-5]
    url = f"https://www.bumeran.com.pe/api/candidates/fichaAvisoNormalizada/{link_id}"
    r = requests.get(url=url, headers=get_random_header(header_list))
    data = r.json()
    preguntas = data["aviso"]["preguntas"]
    return preguntas

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("📝 Mira las preguntas de Bumeran:")

st.write("""
         Esta página te permitirá ver las preguntas de Bumeran antes de postular 🙂.  
         Escribe tus respuestas en la página original.
         """)

link = st.text_input(placeholder="https://www.bumeran.com.pe/empleos/asistente-contable-rsm-peru-1116412339.html",label="Ingresa el link: ")

if st.button("Consultar"):
  if link:
      preguntas = consultar_preguntas(link)
      if preguntas:
        for _,i in enumerate(preguntas,start=1):
          for j in i.values():
              st.write(f'**{_}. {j["texto"]}**')
              if "opciones" in j.keys():
                  for p in j["opciones"]:
                      st.write(f' - {p["opcion"]}')
      else:
         st.warning("No hay preguntas")
  else:
   st.write("Ingresa el link.")
