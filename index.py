
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

cursor = conn.cursor()

# Step 2: Create the table

cursor.execute(
    "CREATE TABLE IF NOT EXISTS INCIDENTS (id SERIAL PRIMARY KEY, TICKETID varchar, ZONA_TKT varchar, TIPO_TKT varchar, INTERNALPRIORITY varchar, URGENCY varchar, IMPACT varchar, INCMESTADO varchar, CREATEDBY varchar, CHANGEDATE varchar, OWNER varchar, OWNERGROUP varchar, LOCATION varchar, MUN100 varchar, AFECTACION_TOTAL_CORE varchar, INCEXCLUIR varchar, INCMEXCLUSION varchar, PROVEEDORES varchar, TICKET_EXT varchar, EXTERNALSYSTEM varchar, INC_ALARMA varchar, INCSOLUCION varchar, GERENTE varchar, REGIONAL varchar, CIUDAD_MUNICIPIO varchar, PROBLEM_CODE varchar, PROBLEM_DESCRIPTION varchar, CAUSE_CODE varchar, CAUSE_DESCRIPTION varchar, REMEDY_CODE varchar, REMEDY_DESCRIPTION varchar, TIEMPO_VIDA_TKT varchar, TIEMPO_RESOLUCION_TKT varchar, TIEMPO_DETECCION varchar, TIEMPO_ESCALA varchar, TIEMPO_FALLA varchar, TIEMPO_OT_ALM varchar, EYN varchar, SRVOZ varchar, SRDATOS varchar, SRTV varchar, SRINTERNET varchar, NEGOCIOS varchar, FECHA_CAMBIO_RUTA varchar, A_S_C varchar, TICKETREL varchar )"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS WORKLOG (id SERIAL PRIMARY KEY, WORKLOGID varchar, RECORDKEY varchar, CREATEDATE varchar, DESCRIPTION varchar, MODIFYDATE varchar, MODIFYBY varchar, DESCRIPTION_LONGDESCRIPTION varchar, CLASS varchar, LOGTYPE varchar, ID varchar, PRIM_US_NOTA varchar, DOCUMENTOS varchar, CREATEBY varchar)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS WOSTATUS (id SERIAL PRIMARY KEY, WOSTATUSID varchar, TICKETID varchar, WONUM varchar, ORGID varchar, CHANGEBY varchar, CHANGEDATE varchar, PARENT varchar, STATUS varchar, STATUS_TIME varchar)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS ACTIVTIES (id SERIAL PRIMARY KEY, TICKETID varchar, WONUM varchar, REPORTDATE varchar, CHANGEDATE varchar, STATUSDATE varchar, ACTSTART varchar, ACTFINISH varchar, SCHEDSTART varchar, SCHEDFINISH varchar, TASKID varchar, DESCRIPTION varchar, RUTA_ACTIVIDAD varchar, PARENT varchar, SMU varchar, STATUS varchar, WORKTYPE varchar, OWNER varchar, OWNERGROUP varchar, REGIONAL varchar, ALIADO varchar, INCMESTADO varchar, PROBLEM_CODE varchar, PROBLEM_DESCRIPTION varchar, CAUSE_CODE varchar, CAUSE_DESCRIPTION varchar, REMEDY_CODE varchar, REMEDY_DESCRIPTION varchar, OT_WFM varchar, RESOLUTOR varchar, WOPRIORITY varchar, DEPTO varchar, TIEMPO_REAL_ACT varchar, SUPERVISOR varchar, REPORTEDBY varchar, PMCHGTYPE varchar, EXTERNALREFID varchar, SGINTERVENTORIA varchar, LOCATION varchar)"
)

# navigate to the login page with basic authentication credentials in the URL
driver.get("http://ECM9491G:22..ZteCol@100.126.20.133/maximo/ui")

# wait for the page to load
driver.implicitly_wait(10)


# scrape the data from the .jsp file
link = driver.find_element(By.ID, "FavoriteApp_INCIDENT")
link.click()

consulta_indicador_hogares = driver.find_element(
    By.ID, "m9e1854a7_ns_menu_queryMenuItem_18_a")
consulta_indicador_hogares.click()

wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located(
    (By.ID, "m6a7dfd2f_tdrow_[C:1]-c[R:0]")))


# Step 4: Scrape and save the data
cont = 0
while True:
    driver.implicitly_wait(30)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    table = soup.find("table", {"id": "m6a7dfd2f_tbod-tbd"})

    rows = table.tbody.find_all("tr", recursive=False)

    data_incidents = []
    data_worklog = []
    data_wostatus = []
    data_activities = []

    del rows[:3]
    del rows[-1]
    print(len(rows))

    for row in rows:
        obj_incidents = {}
        obj_worklog = {}
        obj_wostatus = {}
        obj_activities = {}
        cols = row.find_all("td")
        del cols[:2]
        if cols:
            obj_incidents["TICKETID"] = cols[0].text.strip()
            obj_incidents["DESCRIPTION"] = cols[1].text.strip()
            obj_incidents["CREATIONDATE"] = cols[2].text.strip()
            # Fecha de inicio en la tabla
            obj_incidents["ACTUALFINISH"] = cols[3].text.strip()
            obj_incidents["CLOSEDATE"] = cols[4].text.strip()  # F. Resolucion
            # obj_incidents["REPORTEDBY"] = cols[5].text.strip()
            obj_incidents["INTERNALPRIORITY"] = cols[6].text.strip()
            # obj_incidents["AFECTACION_TOTAL_CORE"] = cols[7].text.strip() Afectacion total core
            # obj_incidents["ARTICULO CONFIGURACION"] = cols[8].text.strip()  # CHECK
            obj_incidents["LOCATION"] = cols[9].text.strip()
            obj_incidents["RUTA_TKT"] = cols[10].text.strip()
            obj_incidents["FAILURECODE"] = cols[11].text.strip()
            obj_incidents["STATUS"] = cols[12].text.strip()
            obj_incidents["STATUSDATE"] = cols[13].text.strip()
            # obj_incidents["PROPERTY"] = cols[14].text.strip() # CHECK
            # obj_incidents["CREATION_FLUJO"] = cols[15].text.strip() # CHECK
            obj_incidents["OWNERGROUP"] = cols[16].text.strip()

            # get id of col 0
            print(obj_incidents)
            driver.implicitly_wait(30)
            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.element_to_be_clickable(
                (By.ID, "m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:"+str(cont)+"]")))
            driver.find_element(By.ID,
                                "m6a7dfd2f_tdrow_[C:1]_ttxt-lb[R:"+str(cont)+"]").click()
            print(cont)
            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.element_to_be_clickable(
                (By.ID, "mbf28cd64-tab_anchor")))

            driver.find_element(By.ID, "mbf28cd64-tab_anchor").click()
            driver.implicitly_wait(30)

            obj_incidents["TICKETID"] = driver.find_element(
                By.ID, "m77a6936f-lb").text
            obj_incidents["ZONA_TKT"] = ""
            obj_incidents["TIPO_TKT"] = "INCIDENT"
            obj_incidents["INTERNALPRIORITY"] = driver.find_element(
                By.ID, "mbf5220a2-tb").text
            obj_incidents["URGENCY"] = driver.find_element(
                By.ID, "m3ecd474c-tb").text
            obj_incidents["IMPACT"] = driver.find_element(
                By.ID, "m9afef2b2-tb").text
            obj_incidents["INCMESTADO"] = ""
            obj_incidents["CREATEDBY"] = driver.find_element(
                By.ID, "m6b900bc6-tb").text
            obj_incidents["CHANGEDATE"] = ""
            obj_incidents["OWNER"] = driver.find_element(
                By.ID, "m4523aa85-tb").text
            obj_incidents["OWNERGROUP"] = driver.find_element(
                By.ID, "mc100fe0e-tb").text
            obj_incidents["LOCATION"] = driver.find_element(
                By.ID, "mad5af16c-tb").text
            obj_incidents["MUN100"] = "1" if driver.find_element(
                By.ID, "m6b900bc6-tb").is_selected() else "0"

            obj_incidents["AFECTACION_TOTAL_CORE"] = "1" if driver.find_element(
                By.ID, "md0f7bc1b-cb").is_selected() else "0"
            obj_incidents["INCEXCLUIR"] = "1" if driver.find_element(
                By.ID, "m996c0c0e-cb").is_selected() else "0"
            obj_incidents["INCMEXCLUSION"] = ""
            obj_incidents["PROVEEDORES"] = driver.find_element(
                By.ID, "m97286c6f-tb").text
            obj_incidents["TICKET_EXT"] = driver.find_element(
                By.ID, "mdb4f724f-tb").text
            obj_incidents["EXTERNALSYSTEM"] = ""
            obj_incidents["INC_ALARMA"] = ""
            obj_incidents["INCSOLUCION"] = ""
            obj_incidents["GERENTE"] = ""
            obj_incidents["REGIONAL"] = ""
            obj_incidents["CIUDAD_MUNICIPIO"] = ""
            obj_incidents["PROBLEM_CODE"] = ""
            obj_incidents["PROBLEM_DESCRIPTION"] = ""
            obj_incidents["CAUSE_CODE"] = ""
            obj_incidents["CAUSE_DESCRIPTION"] = ""
            obj_incidents["REMEDY_CODE"] = ""
            obj_incidents["REMEDY_DESCRIPTION"] = ""
            obj_incidents["TIEMPO_VIDA_TKT"] = ""
            obj_incidents["TIEMPO_RESOLUCION_TKT"] = ""
            obj_incidents["TIEMPO_DETECCION"] = ""
            obj_incidents["TIEMPO_ESCALA"] = ""
            obj_incidents["TIEMPO_FALLA"] = ""
            obj_incidents["TIEMPO_OT_ALM"] = ""
            obj_incidents["EYN"] = ""
            obj_incidents["SRVOZ"] = ""
            obj_incidents["SRDATOS"] = ""
            obj_incidents["SRTV"] = ""
            obj_incidents["SRINTERNET"] = ""
            obj_incidents["NEGOCIOS"] = ""
            obj_incidents["FECHA_CAMBIO_RUTA"] = ""
            obj_incidents["A_S_C"] = ""
            obj_incidents["TICKETREL"] = ""

            data_incidents.append(obj_incidents)

            obj_worklog["WORKLOGID"] = ""
            obj_worklog["RECORDKEY"] = ""
            obj_worklog["CREATEDATE"] = ""
            obj_worklog["DESCRIPTION"] = ""
            obj_worklog["MODIFYDATE"] = ""
            obj_worklog["MODIFYBY"] = ""
            obj_worklog["DESCRIPTION_LONGDESCRIPTION"] = ""
            obj_worklog["CLASS"] = ""
            obj_worklog["LOGTYPE"] = ""
            obj_worklog["ID"] = ""
            obj_worklog["PRIM_US_NOTA"] = ""
            obj_worklog["DOCUMENTOS"] = ""
            obj_worklog["CREATEBY"] = ""

            obj_wostatus["WOSTATUSID"] = ""
            obj_wostatus["TICKETID"] = ""
            obj_wostatus["WONUM"] = ""
            obj_wostatus["ORGID"] = ""
            obj_wostatus["CHANGEBY"] = ""
            obj_wostatus["CHANGEDATE"] = ""
            obj_wostatus["PARENT"] = ""
            obj_wostatus["STATUS"] = ""
            obj_wostatus["STATUS_TIME"] = ""

            driver.find_element(
                By.ID, "mac74095a-tab_anchor").click()  # Tareas

            obj_woactivity["WOSEQUENCE"] = driver.find_element(
                By.ID, "m97286c6f-tb").text

            obj_activities["TICKETID"] = ""
            obj_activities["WONUM"] = ""
            obj_activities["REPORTDATE"] = ""
            obj_activities["CHANGEDATE"] = ""
            obj_activities["STATUSDATE"] = ""
            obj_activities["ACTSTART"] = ""
            obj_activities["ACTFINISH"] = ""
            obj_activities["SCHEDSTART"] = ""
            obj_activities["SCHEDFINISH"] = ""
            obj_activities["TASKID"] = ""
            obj_activities["DESCRIPTION"] = ""
            obj_activities["RUTA_ACTIVIDAD"] = ""
            obj_activities["PARENT"] = ""
            obj_activities["SMU"] = ""
            obj_activities["STATUS"] = ""
            obj_activities["WORKTYPE"] = ""
            obj_activities["OWNER"] = ""
            obj_activities["OWNERGROUP"] = ""
            obj_activities["REGIONAL"] = ""
            obj_activities["ALIADO"] = ""
            obj_activities["INCMESTADO"] = ""
            obj_activities["PROBLEM_CODE"] = ""
            obj_activities["PROBLEM_DESCRIPTION"] = ""
            obj_activities["CAUSE_CODE"] = ""
            obj_activities["CAUSE_DESCRIPTION"] = ""
            obj_activities["REMEDY_CODE"] = ""
            obj_activities["REMEDY_DESCRIPTION"] = ""
            obj_activities["OT_WFM"] = ""
            obj_activities["RESOLUTOR"] = ""
            obj_activities["WOPRIORITY"] = ""
            obj_activities["DEPTO"] = ""
            obj_activities["TIEMPO_REAL_ACT"] = ""
            obj_activities["SUPERVISOR"] = ""
            obj_activities["REPORTEDBY"] = ""
            obj_activities["PMCHGTYPE"] = ""
            obj_activities["EXTERNALREFID"] = ""
            obj_activities["SGINTERVENTORIA"] = ""
            obj_activities["LOCATION"] = ""

            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.element_to_be_clickable(
                (By.ID, "m397b0593-tabs_middle")))
            back_button = driver.find_element(By.ID, "m397b0593-tabs_middle")
            back_button.click()

            cont += 1
    cursor.execute("INSERT INTO INCIDENTS (TICKETID, ZONA_TKT, TIPO_TKT, INTERNALPRIORITY, URGENCY, IMPACT, INCMESTADO, CREATEDBY, CHANGEDATE, OWNER, OWNERGROUP, LOCATION, MUN100, AFECTACION_TOTAL_CORE, INCEXCLUIR, INCMEXCLUSION, PROVEEDORES, TICKET_EXT, EXTERNALSYSTEM, INC_ALARMA, INCSOLUCION, GERENTE, REGIONAL, CIUDAD_MUNICIPIO, PROBLEM_CODE, PROBLEM_DESCRIPTION, CAUSE_CODE, CAUSE_DESCRIPTION, REMEDY_CODE, REMEDY_DESCRIPTION, TIEMPO_VIDA_TKT, TIEMPO_RESOLUCION_TKT, TIEMPO_DETECCION, TIEMPO_ESCALA, TIEMPO_FALLA, TIEMPO_OT_ALM, EYN, SRVOZ, SRDATOS, SRTV, SRINTERNET, NEGOCIOS, FECHA_CAMBIO_RUTA, A_S_C, TICKETREL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data_incidents)
    conn.commit()

    try:
        driver.implicitly_wait(30)
        next_page = driver.find_element(By.ID, "m6a7dfd2f-ti7")
        next_page.click()
    except NoSuchElementException:
        break

# Step 5: Commit the changes and close the connection


conn.close()
driver.close()
