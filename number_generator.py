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

# Funções de download e processamento de dados omitidas para brevidade

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

def generate_numbers_based_on_history(historical_data, num_numbers=9, max_number=60):
    all_numbers = []
    for draw in historical_data:
        for num in draw:
            if isinstance(num, (int, float)) and not np.isnan(num):
                all_numbers.append(int(num))

    number_frequency = Counter(all_numbers)
    probabilities = [number_frequency.get(i, 1) for i in range(1, max_number + 1)]
    probabilities = np.array(probabilities, dtype=float)
    total = np.sum(probabilities)
    if total == 0:
        probabilities = np.ones(max_number) / max_number
    else:
        probabilities /= total
    generated_numbers = np.random.choice(range(1, max_number + 1),
                                         size=num_numbers,
                                         replace=False,
                                         p=probabilities)
    return sorted(generated_numbers)

def get_generated_numbers(num_numbers=9):
    try:
        historical_data = load_historical_data()
        if historical_data:
            return generate_numbers_based_on_history(historical_data, num_numbers=num_numbers)
        else:
            raise Exception("Não foi possível carregar os dados históricos.")
    except Exception as e:
        print(f"Erro: {e}")
        return None

def get_most_frequent_numbers(n=5):
    try:
        df = pd.read_excel(DEFAULT_EXCEL_FILENAME)

        # Identificando as colunas das bolas
        ball_columns = [col for col in df.columns if col.lower().startswith('bola')]

        if not ball_columns:
            raise ValueError("Não foram encontradas colunas de bolas no arquivo.")

        # Combinando todos os números das colunas de bolas
        all_numbers = df[ball_columns].values.flatten()

        # Contando a frequência de cada número
        number_counts = Counter(all_numbers)

        # Obtendo os n números mais frequentes
        most_common = number_counts.most_common(n)

        # Formatando o resultado como uma lista de listas para a tabela
        ranking = [
            [i + 1, num, count]
            for i, (num, count) in enumerate(most_common)
        ]

        return ranking
    except Exception as e:
        print(f"Erro ao obter os números mais frequentes: {e}")
        return []

# Função auxiliar para debug
def print_excel_info():
    try:
        df = pd.read_excel(DEFAULT_EXCEL_FILENAME)
        print("Colunas no arquivo Excel:")
        print(df.columns.tolist())
        print("\nPrimeiras linhas do DataFrame:")
        print(df.head())
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")

def get_last_winning_games(n=5):
    try:
        df = pd.read_excel(DEFAULT_EXCEL_FILENAME)
        df = df.sort_values('Concurso', ascending=False).head(n)
        last_games = []
        for _, row in df.iterrows():
            game = [row['Concurso']] + [row[f'bola{i}'] for i in range(1, 7)]
            last_games.append(game)
        return last_games
    except Exception as e:
        print(f"Erro ao obter os últimos jogos ganhadores: {e}")
        return []
