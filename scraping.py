import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import psycopg2
import csv

# 1.Inicia o navegador e o processo de pesquisa

search_text = input("O que você deseja pesquisar?")
driver = webdriver.Chrome()
driver.maximize_window()

url = "https://www.zoom.com.br/"
driver.get(url)
time.sleep(1)

search_box = driver.find_element(By.XPATH,
                                 "/html/body/div[1]/header/div[1]/div/div/div[3]/div/div/div[1]/input").send_keys(
    search_text)
time.sleep(1)

search_button = driver.find_element(By.XPATH,
                                    "/html/body/div[1]/header/div[1]/div/div/div[3]/div/div/div[1]/button").click()
time.sleep(5)

drop_down = Select(
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div[1]/div/div/div/div[2]/select"))
drop_down.select_by_value("price_asc")

time.sleep(5)

# 2.Parsea o HTML por meio do BeautifulSoup

page_content = driver.page_source
soup = BeautifulSoup(page_content, "html.parser")

# 3.Coleta os dados da página

products = soup.findAll(class_="Cell_Infos__KDy41")

list_products = []

for product in products:
    product_name = product.find(class_="Text_Text__VJDNU Text_LabelSmRegular__qvxsr")
    product_price = product.find(class_="Text_Text__VJDNU Text_LabelMdBold__uMr7_ CellPrice_MainValue__JXsj_")

    list_products.append([product_name.text, product_price.text])

# 4.Cria um DataFrame e aloca os dados em um arquivo .csv

products_data = pd.DataFrame(list_products, columns=["Nome do Produto", "Preço"])
products_data.to_csv("placas.csv", index=False)

print(products_data)

print("\n PROCESSO FINALIZADO!")

hostname = 'localhost'
database = 'Webscraping'
username = 'postgres'
pwd = 'Ricardo02$'
port_id = 5432
cur = None
conn = None

try:
    conn = psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id)

    cur = conn.cursor()  # variável para auxiliar na manipulação do sql

    cur.execute('DROP TABLE IF EXISTS produtos') #Para certificar que na implementação de novos dados não gere conflito com id

    create_script = ''' CREATE TABLE 
                            produtos  (
                            id      int PRIMARY KEY,
                            nome    varchar,
                            preco   varchar) '''

    cur.execute(create_script)

    conn.commit()


except Exception as error:
    print(error)
finally:  # Bloco para garantir que a conexão e o cursor foi encerrada.
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

with open("placas.csv", "r") as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=",")
    for linha in arquivo_csv:
        print(linha)



