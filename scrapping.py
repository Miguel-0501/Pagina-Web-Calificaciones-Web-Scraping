from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")  
    return webdriver.Chrome(options=chrome_options)

def obtener_tabla(driver, url):
    driver.get(url)
    logging.info("Esperando a que la página cargue...")
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]"))
    )

def extract_data(row):
    try:
        score = row.find_element(By.CLASS_NAME, 'score').text.strip()
        # Convertir el score a un float y verificar si es mayor o igual a 8
        if float(score) >= 8:
            return {
                'class': row.find_element(By.CLASS_NAME, 'response').text.strip(),
                'score': row.find_element(By.CLASS_NAME, 'score').text.strip(),
                'date': row.find_element(By.CLASS_NAME, 'date').text.strip(),
                'comment': row.find_element(By.CLASS_NAME, 'commentsParagraph').text.strip() or "No hay comentario"
        }
        else:
            return None #Retorna none si el score es menor a 8
    except Exception as e:
        logging.error(f"Error al procesar una fila: {e}")
        return None
    
def get_paginas_links(driver):
    paginas = driver.find_element(By.CLASS_NAME, 'pagination')
    links = paginas.find_elements(By.TAG_NAME, 'a')
    return [link.get_attribute('href') for link in links if link.get_attribute('href')]


def scrape_all_pages():
    base_url = 'https://www.misprofesores.com/profesores/Rene-Vazquez-Jimenez_37626'
    driver = setup_driver()
    datos = []

    try: 
        for page in range(1, 20): #Scrapear de la 1 hasta la 19
            url = f"{base_url}?pag={page}"  # Corregido: Cambiado '?' por '?pag='
            logging.info(f"Scraping página {page}")

            table = obtener_tabla(driver, url)
            rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

            page_data = [data for data in (extract_data(row) for row in rows) if data is not None]

            datos.extend(page_data)

            logging.info(f"Extraídas {len(page_data)} entradas de la página {page}")

        return datos
    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")
        return datos
    finally:
        driver.quit()

def main(): 
    data = scrape_all_pages()

    df = pd.DataFrame(data)
    df.to_csv('datos_de_tablas.csv', index=False, encoding='utf-8-sig')

    logging.info(f"Número total de entradas extraídas: {len(data)}")
    logging.info(f"Datos guardados en 'datos_de_tablas.csv'")

if __name__ == '__main__':
    main()