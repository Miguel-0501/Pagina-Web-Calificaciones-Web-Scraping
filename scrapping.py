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
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless
    return webdriver.Chrome(options=chrome_options)

def get_table(driver, url):
    driver.get(url)
    logging.info("Esperando a que la página cargue...")
    return WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'table')]"))
    )

def extract_data(row):
    try:
        return {
            'class': row.find_element(By.CLASS_NAME, 'response').text.strip(),
            'score': row.find_element(By.CLASS_NAME, 'score').text.strip(),
            'date': row.find_element(By.CLASS_NAME, 'date').text.strip(),
            'comment': row.find_element(By.CLASS_NAME, 'commentsParagraph').text.strip() or "No hay comentario"
        }
    except Exception as e:
        logging.error(f"Error al procesar una fila: {e}")
        return None
    
def scrape_calificaciones():
    url = 'https://www.misprofesores.com/profesores/Gustavo-Adolfo-Alonso-Silverio_86282'
    driver = setup_driver()
    
    try:
        table = get_table(driver, url)
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # Ignoramos la primera fila (encabezado)
        logging.info(f"Número de filas encontradas: {len(rows)}")

        data = [extract_data(row) for row in rows if extract_data(row) is not None]
        
        return data

    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")
        return []
    finally:
        driver.quit()

def main():
    url = 'https://www.misprofesores.com/profesores/Gustavo-Adolfo-Alonso-Silverio_86282'
    driver = setup_driver()
    
    try:
        table = get_table(driver, url)
        rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # Ignoramos la primera fila (encabezado)
        logging.info(f"Número de filas encontradas: {len(rows)}")

        data = [extract_data(row) for row in rows if extract_data(row) is not None]

        df = pd.DataFrame(data)
        df.to_csv('data.csv', index=False, encoding='utf-8-sig')
        
        logging.info(f"Número total de entradas extraídas: {len(data)}")
        logging.info(f"Datos guardados en 'data.csv'")

    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()