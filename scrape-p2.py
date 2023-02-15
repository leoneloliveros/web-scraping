
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
    "CREATE TABLE IF NOT EXISTS INCIDENTS (id SERIAL PRIMARY KEY, WORKLOGID varchar, RECORDKEY varchar, CREATEDATE varchar, DESCRIPTION varchar, MODIFYDATE varchar, MODIFYBY varchar, DESCRIPTION_LONGDESCRIPTION varchar, CLASS varchar, LOGTYPE varchar, ID varchar, PRIM_US_NOTA varchar, DOCUMENTOS varchar, CREATEBY varchar)"
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

        obj["TICKETID"] = driver.find_element(By.ID, "m77a6936f-lb").text
        obj["ZONA_TKT"] = ""
        obj["TIPO_TKT"] = "INCIDENT"
        obj["CREATIONDATE"] = driver.find_element(
            By.ID, "m77a6936f-lb").text
        obj["CLOSEDATE"] = driver.find_element(By.ID, "ma0c8456f-tb").text
        obj["ACTUALFINISH"] = driver.find_element(
            By.ID, "ma0c8456f-tb").text
        obj["STATUSDATE"] = obj["STATUS"] = obj["INTERNALPRIORITY"] = driver.find_element(
            By.ID, "mbf5220a2-tb").text
        obj["URGENCY"] = driver.find_element(By.ID, "m3ecd474c-tb").text
        obj["IMPACT"] = driver.find_element(By.ID, "m9afef2b2-tb").text
        obj["INCMESTADO"] = obj["CREATEDBY"] = driver.find_element(
            By.ID, "m6b900bc6-tb").text
        obj["CHANGEDATE"] = obj["OWNER"] = driver.find_element(
            By.ID, "m4523aa85-tb").text
        obj["OWNERGROUP"] = driver.find_element(By.ID, "mc100fe0e-tb").text
        obj["LOCATION"] = driver.find_element(By.ID, "mad5af16c-tb").text
        obj["MUN100"] = driver.find_element(By.ID, "m6b900bc6-tb").isSelected() ? "1": "0"
        obj["AFECTACION_TOTAL_CORE"] = driver.find_element(By.ID, "md0f7bc1b-cb").isSelected() ? "1": "0"
        obj["INCEXCLUIR"] = driver.find_element(By.ID, "m996c0c0e-cb").isSelected() ? "1": "0"
        obj["INCMEXCLUSION"] = obj["PROVEEDORES"] = driver.find_element(
            By.ID, "m97286c6f-tb").text
        obj["TICKET_EXT"] = driver.find_element(By.ID, "mdb4f724f-tb").text
        obj["DESCRIPTION"] = driver.find_element(
            By.ID, "m8672e47c-tb").text
        obj["EXTERNALSYSTEM"] = obj["RUTA_TKT"] = driver.find_element(
            By.ID, "mc76799fb-tb").text
        obj["INC_ALARMA"] = ""
        obj["INCSOLUCION"] ""
        obj["GERENTE"] = ""
        obj["REGIONAL"] = ""
        obj["CIUDAD_MUNICIPIO"] = ""
        obj["FAILURECODE"] = ""
        obj["PROBLEM_CODE"] = ""
        obj["PROBLEM_DESCRIPTION"] = ""
        obj["CAUSE_CODE"] = ""
        obj["CAUSE_DESCRIPTION"] = ""
        obj["REMEDY_CODE"] = ""
        obj["REMEDY_DESCRIPTION"] = ""
        obj["TIEMPO_VIDA_TKT"] = ""
        obj["TIEMPO_RESOLUCION_TKT"] = ""
        obj["TIEMPO_DETECCION"] = ""
        obj["TIEMPO_ESCALA"] = ""
        obj["TIEMPO_FALLA"] = ""
        obj["TIEMPO_OT_ALM"] = ""
        obj["EYN"] = ""
        obj["SRVOZ"] = ""
        obj["SRDATOS"] = ""
        obj["SRTV"] = ""
        obj["SRINTERNET"] = ""
        obj["NEGOCIOS"] = ""
        obj["FECHA_CAMBIO_RUTA"] = ""
        obj["A_S_C"] = ""
        obj["TICKETREL"] = ""

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
