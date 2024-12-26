import pandas as pd
from datetime import datetime


def gerar_numeros_sorteados(arquivo_excel):
    # Carrega o arquivo Excel
    df = pd.read_excel(arquivo_excel)

    # Verifique os nomes das colunas
    print("Colunas disponíveis:", df.columns.tolist())

    # Certifique-se de que a coluna 'Data' está presente e converta para datetime
    if 'Data' not in df.columns:
        raise KeyError("A coluna 'Data' não foi encontrada no arquivo Excel.")

    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')

    # Obtenha o mês atual
    mes_atual = datetime.now().month

    # Filtra os sorteios do mesmo mês atual
    sorteios_mes_atual = df[df['Data'].dt.month == mes_atual]

    # Supondo que as colunas das bolas são 'bola 1', 'bola 2', ..., 'bola 15'
    colunas_bolas = [f'bola {i}' for i in range(1, 16)]

    # Calcula a frequência de cada número no histórico
    todos_numeros = df[colunas_bolas].values.flatten()
    frequencia_historica = pd.Series(todos_numeros).value_counts()

    # Calcula a frequência de cada número no mês atual
    numeros_mes_atual = sorteios_mes_atual[colunas_bolas].values.flatten()
    frequencia_mes_atual = pd.Series(numeros_mes_atual).value_counts()

    # Obtém os 15 números mais sorteados no histórico
    mais_sorteados_historico = frequencia_historica.nlargest(15).index.tolist()

    # Obtém os 15 números mais sorteados no mesmo mês
    mais_sorteados_mes = frequencia_mes_atual.nlargest(15).index.tolist()

    # Sugere 15 números com maior chance de serem sorteados novamente
    sugeridos = mais_sorteados_historico  # Aqui, usamos a mesma lógica dos mais sorteados no histórico

    return mais_sorteados_historico, mais_sorteados_mes, sugeridos


# Exemplo de uso
arquivo = "loto_facil_asloterias_ate_concurso_3277_sorteio.xlsx"
mais_sorteados_historico, mais_sorteados_mes, sugeridos = gerar_numeros_sorteados(arquivo)

print("15 números mais sorteados no histórico:", mais_sorteados_historico)
print("15 números mais sorteados no mesmo mês:", mais_sorteados_mes)
print("15 números sugeridos:", sugeridos)
