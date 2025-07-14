from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
import os



driver = webdriver.Chrome()
    

# Primero vamos a la página

driver.get("https://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/")
        
# Esperaramos a que se carge
wait = WebDriverWait(driver, 10)

# Buscamos el select que nos ayuda a seleccionar el nivel educativo    
select_nivel = wait.until(
    EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_cmbNivel"))
)
nivel_dropdown = Select(select_nivel)
nivel_dropdown.select_by_value("46") 
        

dptos_id = [
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"
] #Esta lista tiene todos los values de los departamentos del dropdown
dptos_nombres= [
    "CIUDAD CAPITAL",   # 00
    "GUATEMALA",        # 01
    "EL PROGRESO",      # 02
    "SACATEPEQUEZ",     # 03
    "CHIMALTENANGO",    # 04
    "ESCUINTLA",        # 05
    "SANTA ROSA",       # 06
    "SOLOLA",           # 07
    "TOTONICAPAN",      # 08
    "QUETZALTENANGO",   # 09
    "SUCHITEPEQUEZ",    # 10
    "RETALHULEU",       # 11
    "SAN MARCOS",       # 12
    "HUEHUETENANGO",    # 13
    "QUICHE",           # 14
    "BAJA VERAPAZ",     # 15
    "ALTA VERAPAZ",     # 16
    "PETEN",            # 17
    "IZABAL",           # 18
    "ZACAPA",           # 19
    "CHIQUIMULA",       # 20
    "JALAPA",           # 21
    "JUTIAPA"           # 22
]

nombres_variables = set() #Este conjunto lo usamos para guardar los nombres de las variables
resultado_final = []
for i in range(len(dptos_id)):
    # Ahora obtenemos la lista de departamentos
    select_departamento = wait.until(
    EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_cmbDepartamento"))
    )
    departamento_dropdown = Select(select_departamento)
    departamento_dropdown.select_by_value(dptos_id[i]) #Seleccionamos el valor actual
    boton_consultar = wait.until(
        EC.element_to_be_clickable((By.ID, "_ctl0_ContentPlaceHolder1_IbtnConsultar"))
    ) #Buscar el botón para hacer la búsqueda
    boton_consultar.click() #Hacemos click en el botón
    time.sleep(10)
    establecimientos_list = wait.until(
        EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_dgResultado"))
    )
    filas = establecimientos_list.find_elements(By.TAG_NAME, "tr")
    encabezados = [td.text.strip() for td in filas[0].find_elements(By.TAG_NAME, "td")][1:] #Hallar los nonbres de las variables
    nombres_variables.update(encabezados) #Acumular en el conjunto

    datos = []
    for fila in filas[1:]:
        celdas = fila.find_elements(By.TAG_NAME, "td")[1:]  # ignorar primera celda
        fila_datos = [celda.text.strip() for celda in celdas]
        datos.append(fila_datos)

    df = pd.DataFrame(datos, columns=encabezados)
    resultado_final.append(df)


df_final = pd.concat(resultado_final, ignore_index=True)
df_final.to_csv("establecimientos.csv", index=False, encoding="utf-8-sig")
#Guardar las variables encontradas
with open("nombres_variables.txt", "w", encoding="utf-8") as f:
    for nombre in sorted(nombres_variables):
        f.write(nombre + "\n")
