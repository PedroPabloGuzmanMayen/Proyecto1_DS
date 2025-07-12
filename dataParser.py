from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd



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

#Buscamos el botón que sirve para hacer la búsqueda




for i in dptos_id:
    # Ahora obtenemos la lista de departamentos
    select_departamento = wait.until(
    EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_cmbDepartamento"))
    )
    departamento_dropdown = Select(select_departamento)
    departamento_dropdown.select_by_value(i) #Seleccionamos el valor actual
    boton_consultar = wait.until(
        EC.element_to_be_clickable((By.ID, "_ctl0_ContentPlaceHolder1_IbtnConsultar"))
    ) #Buscar el botón para hacer la búsqueda
    boton_consultar.click() #Hacemos click en el botón
    time.sleep(10)
    establecimientos_list = wait.until(
        EC.presence_of_element_located((By.ID, "_ctl0_ContentPlaceHolder1_dgResultado"))
    )


    print(establecimientos_list)


