
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import psycopg2
from selenium.common.exceptions import NoSuchElementException
from time import sleep


# initialize the web driver
driver = webdriver.Chrome()

# Step 1: Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="scrape",
    user="postgres",
    password="LA12OM17mz",
    port="5432"
)

print(conn)
cursor = conn.cursor()

# Step 2: Create the table
cursor.execute(
    "CREATE TABLE IF NOT EXISTS ACTIVITIES (id SERIAL PRIMARY KEY, TICKETID varchar, WONUM varchar, REPORTDATE varchar, CHANGEDATE varchar, STATUSDATE varchar, ACTSTART varchar, ACTFINISH varchar, SCHEDSTART varchar, SCHEDFINISH varchar, TASKID varchar, DESCRIPTION varchar, RUTA_ACTIVIDAD varchar, PARENT varchar, SMU varchar, STATUS varchar, WORKTYPE varchar, OWNER varchar, OWNERGROUP varchar, REGIONAL varchar, ALIADO varchar, INCMESTADO varchar, PROBLEM_CODE varchar, PROBLEM_DESCRIPTION varchar, CAUSE_CODE varchar, CAUSE_DESCRIPTION varchar, REMEDY_CODE varchar, REMEDY_DESCRIPTION varchar, OT_WFM varchar, RESOLUTOR varchar, WOPRIORITY varchar, DEPTO varchar, TIEMPO_REAL_ACT varchar, SUPERVISOR varchar, REPORTEDBY varchar, PMCHGTYPE varchar, EXTERNALREFID varchar, SGINTERVENTORIA varchar, LOCATION varchar )"
)
cursor.execute(
    "CREATE TABLE IF NOT EXISTS INCIDENTS (id SERIAL PRIMARY KEY, TICKETID varchar, ZONA_TKT varchar, TIPO_TKT varchar, CREATIONDATE varchar, CLOSEDATE varchar, ACTUALFINISH varchar, STATUSDATE varchar, STATUS varchar, INTERNALPRIORITY varchar, URGENCY varchar, IMPACT varchar, INCMESTADO varchar, CREATEDBY varchar, CHANGEDATE varchar, OWNER varchar, OWNERGROUP varchar, LOCATION varchar, MUN100 varchar, AFECTACION_TOTAL_CORE varchar, INCEXCLUIR varchar, INCMEXCLUSION varchar, PROVEEDORES varchar, TICKET_EXT varchar, DESCRIPTION varchar, EXTERNALSYSTEM varchar, RUTA_TKT varchar, INC_ALARMA varchar, INCSOLUCION varchar, GERENTE varchar, REGIONAL varchar, CIUDAD_MUNICIPIO varchar, FAILURECODE varchar, PROBLEM_CODE varchar, PROBLEM_DESCRIPTION varchar, CAUSE_CODE varchar, CAUSE_DESCRIPTION varchar, REMEDY_CODE varchar, REMEDY_DESCRIPTION varchar, TIEMPO_VIDA_TKT varchar, TIEMPO_RESOLUCION_TKT varchar, TIEMPO_DETECCION varchar, TIEMPO_ESCALA varchar, TIEMPO_FALLA varchar, TIEMPO_OT_ALM varchar, EYN varchar, SRVOZ varchar, SRDATOS varchar, SRTV varchar, SRINTERNET varchar, NEGOCIOS varchar, FECHA_CAMBIO_RUTA varchar, A_S_C varchar, TICKETREL varchar)"
)

# navigate to the login page with basic authentication credentials in the URL
driver.get("http://ECM9491G:22..ZteCol@100.126.20.133/maximo/ui")
driver.implicitly_wait(10)

# Go to incidents
driver.find_element(By.ID, "FavoriteApp_INCIDENT").click()

# wait for the page to load
driver.implicitly_wait(10)

# Go to consulta_indicador_hogares
driver.find_element(By.ID, "m9e1854a7_ns_menu_queryMenuItem_18_a").click()
driver.implicitly_wait(10)


# Step 4: Scrape and save the data
min = 0
max = 20
while True:
    obj = {}
    for i in range(min, max):
        driver.implicitly_wait(30)
        print("min: " + str(i))
        # find and click to show the details
        driver.find_element(By.ID,
                            "m6a7dfd2f_tdrow_[C:1]-c[R:"+str(i)+"]").click()
        data.push({
            "TICKETID": driver.find_element(By.ID, "m77a6936f-lb").text,
            "ZONA_TKT":
            "TIPO_TKT": "INCIDENT",
            "CREATIONDATE": driver.find_element(By.ID, "m77a6936f-lb").text,
            "CLOSEDATE": driver.find_element(By.ID, "ma0c8456f-tb").text,
            "ACTUALFINISH": driver.find_element(By.ID, "ma0c8456f-tb").text,
            "STATUSDATE":
            "STATUS":
            "INTERNALPRIORITY": driver.find_element(By.ID, "mbf5220a2-tb").text,
            "URGENCY": driver.find_element(By.ID, "m3ecd474c-tb").text,
            "IMPACT": driver.find_element(By.ID, "m9afef2b2-tb").text,
            "INCMESTADO":
            "CREATEDBY": driver.find_element(By.ID, "m6b900bc6-tb").text,
            "CHANGEDATE":
            "OWNER": driver.find_element(By.ID, "m4523aa85-tb").text,
            "OWNERGROUP": driver.find_element(By.ID, "mc100fe0e-tb").text,
            "LOCATION": driver.find_element(By.ID, "mad5af16c-tb").text,
            "MUN100": driver.find_element(By.ID, "m6b900bc6-tb").isSelected() ? "1": "0",
            "AFECTACION_TOTAL_CORE": driver.find_element(By.ID, "md0f7bc1b-cb").isSelected() ? "1": "0",
            "INCEXCLUIR": driver.find_element(By.ID, "m996c0c0e-cb").isSelected() ? "1": "0",
            "INCMEXCLUSION":
            "PROVEEDORES" driver.find_element(By.ID, "m97286c6f-tb").text,
            "TICKET_EXT": driver.find_element(By.ID, "mdb4f724f-tb").text,
            "DESCRIPTION": driver.find_element(By.ID, "m8672e47c-tb").text,
            "EXTERNALSYSTEM":
            "RUTA_TKT": driver.find_element(By.ID, "mc76799fb-tb").text,
            "INC_ALARMA":
            "INCSOLUCION":
            "GERENTE":
            "REGIONAL":
            "CIUDAD_MUNICIPIO":
            "FAILURECODE":
            "PROBLEM_CODE":
            "PROBLEM_DESCRIPTION":
            "CAUSE_CODE":
            "CAUSE_DESCRIPTION":
            "REMEDY_CODE":
            "REMEDY_DESCRIPTION":
            "TIEMPO_VIDA_TKT":
            "TIEMPO_RESOLUCION_TKT":
            "TIEMPO_DETECCION":
            "TIEMPO_ESCALA":
            "TIEMPO_FALLA":
            "TIEMPO_OT_ALM":
            "EYN":
            "SRVOZ":
            "SRDATOS":
            "SRTV":
            "SRINTERNET":
            "NEGOCIOS":
            "FECHA_CAMBIO_RUTA":
            "A_S_C":
            "TICKETREL":})

        # go back to the table
        driver.find_element(By.ID, "m397b0593-tabs_middle").click()

    try:
        min += 20
        max += 20
        next_page = driver.find_element(By.ID, "m6a7dfd2f-ti7")
        next_page.click()
    except NoSuchElementException:
        break

# Step 5: Commit the changes and close the connection


conn.close()
driver.close()
