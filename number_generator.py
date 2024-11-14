import pandas as pd
import numpy as np
from collections import Counter
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re
import zipfile
import io

CAIXA_URL = "https://loterias.caixa.gov.br/Paginas/Download-Resultados.aspx"
AS_LOTERIAS_URL = "https://asloterias.com.br/download-todos-resultados-mega-sena"
CSV_FILENAME = "mega_sena_results.csv"
DEFAULT_EXCEL_FILENAME = "mega_sena_asloterias_ate_concurso_2796_sorteio.xlsx"


def download_mega_sena_file():
    try:
        # Tentativa de download do site da Caixa
        download_from_caixa()
    except Exception:
        print("Não foi possível baixar o arquivo do site da Caixa. Tentando fonte alternativa...")
        try:
            download_from_asloterias()
        except Exception:
            print("Não foi possível baixar um novo arquivo. Usando o arquivo existente.")


def download_from_caixa():
    response = requests.get(CAIXA_URL)
    response.raise_for_status()

    csv_link = re.search(r'href="([^"]*Mega[^"]*\.zip)"', response.text)
    if not csv_link:
        raise Exception("Não foi possível encontrar o link para o arquivo CSV da Mega Sena.")

    csv_url = "https://loterias.caixa.gov.br" + csv_link.group(1)

    zip_response = requests.get(csv_url)
    zip_response.raise_for_status()

    with open("mega_sena_temp.zip", "wb") as f:
        f.write(zip_response.content)

    with zipfile.ZipFile("mega_sena_temp.zip", "r") as zip_ref:
        zip_ref.extractall()

    extracted_file = [f for f in os.listdir() if f.endswith('.csv') and 'Mega' in f][0]
    os.rename(extracted_file, CSV_FILENAME)

    os.remove("mega_sena_temp.zip")
    print("Arquivo da Mega Sena baixado do site da Caixa e extraído com sucesso.")


def download_from_asloterias():
    response = requests.get(AS_LOTERIAS_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    download_link = soup.find('a', text="Download Todos resultados da Mega Sena em Excel por ordem de sorteio")

    if download_link:
        file_url = download_link['href']
        file_response = requests.get(file_url)
        file_response.raise_for_status()

        # Ler o arquivo Excel diretamente da resposta
        df = pd.read_excel(io.BytesIO(file_response.content))
    else:
        raise Exception("Link de download não encontrado no site asloterias.com.br")

    # Renomear as colunas para o formato esperado
    df.columns = ['Concurso', 'Data'] + [f'bola{i}' for i in range(1, 7)]

    # Salvar como CSV no formato esperado
    df.to_csv(CSV_FILENAME, index=False, sep=';')

    print("Dados da Mega Sena processados e salvos com sucesso.")


def ensure_updated_file():
    if not os.path.exists(CSV_FILENAME):
        if os.path.exists(DEFAULT_EXCEL_FILENAME):
            print(f"Usando arquivo padrão: {DEFAULT_EXCEL_FILENAME}")
            df = pd.read_excel(DEFAULT_EXCEL_FILENAME)
            df.columns = ['Concurso', 'Data'] + [f'bola{i}' for i in range(1, 7)]
            df.to_csv(CSV_FILENAME, index=False, sep=';')
        else:
            print("Arquivo não encontrado. Tentando baixar...")
            download_mega_sena_file()
    else:
        file_time = datetime.fromtimestamp(os.path.getmtime(CSV_FILENAME))
        if datetime.now() - file_time > timedelta(days=7):
            print("Arquivo desatualizado. Tentando baixar versão mais recente...")
            try:
                download_mega_sena_file()
            except Exception:
                print("Não foi possível baixar um novo arquivo. Usando o arquivo existente.")
        else:
            print("Arquivo atualizado encontrado.")


def load_historical_data():
    ensure_updated_file()
    try:
        df = pd.read_csv(CSV_FILENAME, delimiter=';', thousands=',', decimal='.')
        number_columns = [col for col in df.columns if col.startswith('bola')]
        historical_data = df[number_columns].values.tolist()
        return historical_data
    except Exception as e:
        print(f"Erro ao carregar dados históricos: {e}")
        return []


def generate_numbers_based_on_history(historical_data, num_numbers=6, max_number=60):
    all_numbers = [num for draw in historical_data for num in draw if pd.notna(num)]
    number_frequency = Counter(all_numbers)
    probabilities = [number_frequency.get(i, 1) for i in range(1, max_number + 1)]  # Use 1 como valor padrão
    probabilities = np.array(probabilities, dtype=float)
    total = np.sum(probabilities)
    if total == 0:
        # Se todos os valores forem zero, use distribuição uniforme
        probabilities = np.ones(max_number) / max_number
    else:
        probabilities /= total
    generated_numbers = np.random.choice(range(1, max_number + 1),
                                         size=num_numbers,
                                         replace=False,
                                         p=probabilities)
    return sorted(generated_numbers)



def get_generated_numbers():
    try:
        historical_data = load_historical_data()
        if historical_data:
            return generate_numbers_based_on_history(historical_data)
        else:
            raise Exception("Não foi possível carregar os dados históricos.")
    except Exception as e:
        print(f"Erro: {e}")
        return None
