import requests
from bs4 import BeautifulSoup

url = 'https://www.misprofesores.com/profesores/Gustavo-Adolfo-Alonso-Silverio_86282'

response = requests.get(url, timeout=10)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra los elementos deseados
    classes = soup.find_all('span', class_='response')
    scores = soup.find_all('span', class_='score bueno')
    dates = soup.find_all('div', class_='date')
    comments = soup.find_all('p', class_='commentsParagraph')

    # Extraer y emparejar los datos
    results = []
    for i in range(min(len(classes), len(scores), len(dates), len(comments))):
        comment_text = comments[i].get_text(strip=True)
        if not comment_text:
            comment_text = "No comentarios"
        
        result = {
            'class': classes[i].get_text(strip=True),
            'score': scores[i].get_text(strip=True),
            'date': dates[i].get_text(strip=True),
            'comment': comment_text
        }
        results.append(result)
else:
    print('Error al obtener la página')

for r in results:
    print(r)