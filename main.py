import streamlit as st
from number_generator import get_generated_numbers, get_most_frequent_numbers, get_last_winning_games
from lotoFacil import gerar_numeros_sorteados
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gerador de Loterias", page_icon="🍀", layout="wide")

# Menu lateral
opcao = st.sidebar.radio("Escolha a loteria", ["Mega Sena", "Loto Fácil"])

# Exibir a seção correspondente com base na opção selecionada
if opcao == "Mega Sena":
    # Título
    st.title("Gerador de Números da Mega Sena")

    # Texto de boas-vindas
    st.markdown("""
    <p class='welcome-text'>
    Bem-vindo ao Gerador de Números da Mega Sena! Este aplicativo auxilia na geração de números para o jogo de loteria Mega Sena da Loteria Federal do Governo Brasileiro.
    </p>
    """, unsafe_allow_html=True)

    # Criando colunas para os botões principais e entrada de número de dezenas
    col1, col2 = st.columns([1, 2])

    # Entrada para o número de dezenas
    num_dezenas = col2.number_input("Número de dezenas", min_value=6, max_value=15, value=9, step=1)

    # Botão "Gerar Número"
    if col1.button("Gerar Número"):
        with st.spinner("Gerando números..."):
            generated_numbers = get_generated_numbers(num_dezenas)
        if generated_numbers:
            st.success(f"Números gerados baseados no histórico: {', '.join(map(str, generated_numbers))}")
        else:
            st.error("Não foi possível gerar números devido a um erro nos dados históricos.")

    # Nova seção com botões adicionais
    st.markdown("---")  # Separador visual
    st.subheader("Outras opções:")

    col3, col4 = st.columns(2)

    if col3.button("Cinco números mais sorteados"):
        with st.spinner("Buscando os números mais sorteados..."):
            most_frequent = get_most_frequent_numbers()
            if most_frequent:
                st.success("Os cinco números mais sorteados são:")

                # Criando um DataFrame para a tabela
                df_most_frequent = pd.DataFrame(most_frequent)
                df_most_frequent.columns = ['Posição', 'Número', 'Frequência']
                df_most_frequent['Posição'] = df_most_frequent['Posição'].apply(lambda x: f"{x}º")
                df_most_frequent['Frequência'] = df_most_frequent['Frequência'].apply(lambda x: f"{x} vezes")

                # Exibindo a tabela
                st.table(df_most_frequent)
            else:
                st.error("Não foi possível obter os números mais sorteados.")

    if col4.button("Últimos 5 jogos ganhadores"):
        with st.spinner("Buscando os últimos jogos ganhadores..."):
            last_games = get_last_winning_games()
            if last_games:
                for game in last_games:
                    st.write(f"Número do jogo {game[0]}: {', '.join(map(str, game[1:]))}")
            else:
                st.error("Não foi possível carregar os dados dos últimos jogos.")

elif opcao == "Loto Fácil":
    # Título
    st.title("Gerador de Números da Loto Fácil")

    # Botão "Gerar números"
    if st.button("Gerar números"):
        with st.spinner("Gerando números..."):
            _, _, sugeridos = gerar_numeros_sorteados("loto_facil_asloterias_ate_concurso_3277_sorteio.xlsx")
        st.success(f"Números sugeridos: {', '.join(map(str, sugeridos))}")

    # Botão "Números mais sorteados até hoje"
    if st.button("Números mais sorteados até hoje"):
        with st.spinner("Buscando números mais sorteados..."):
            mais_sorteados_historico, _, _ = gerar_numeros_sorteados("loto_facil_asloterias_ate_concurso_3277_sorteio.xlsx")
        st.success(f"Números mais sorteados até hoje: {', '.join(map(str, mais_sorteados_historico))}")

    # Botão "Números mais sorteados no mês atual"
    if st.button("Números mais sorteados no mês atual"):
        with st.spinner("Buscando números mais sorteados no mês..."):
            _, mais_sorteados_mes, _ = gerar_numeros_sorteados("loto_facil_asloterias_ate_concurso_3277_sorteio.xlsx")
        st.success(f"Números mais sorteados no mês atual: {', '.join(map(str, mais_sorteados_mes))}")
