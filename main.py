import streamlit as st
from number_generator import get_generated_numbers

# Configuração da página
st.set_page_config(page_title="Gerador Mega Sena", page_icon="🍀", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    .custom-button {
        width: 100%;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        transition: all 0.3s;
        position: relative;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .custom-button:hover {
        background-color: #45a049;
    }
    .custom-button .tooltip {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .custom-button:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    h1, h2 {
        color: #2E7D32;
    }
    .welcome-text, .rules-text {
        font-size: 18px;
        line-height: 1.6;
        color: #333;
    }
    .rules-container {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.title("Gerador de Números da Mega Sena")

# Texto de boas-vindas
st.markdown("""
<p class='welcome-text'>
Bem-vindo ao Gerador de Números da Mega Sena! Este aplicativo auxilia na geração de números para o jogo de loteria Mega Sena da Loteria Federal do Governo Brasileiro.
</p>
""", unsafe_allow_html=True)

# Criando colunas para os botões
col1, col2 = st.columns(2)

# Botão "Gerar Número" com tooltip
if col1.button("Gerar Número"):
    with st.spinner("Gerando números..."):
        generated_numbers = get_generated_numbers()
    if generated_numbers:
        st.success(f"Números gerados baseados no histórico: {' '.join(map(str, generated_numbers))}")


    else:
        st.error("Não foi possível gerar números devido a um erro nos dados históricos.")

# Botão "Gerar Número com Meus Temperos" com tooltip
if col2.button("Gerar Número com Meus Temperos"):
    st.info("Funcionalidade de temperos será implementada posteriormente.")

# Regras da Mega-Sena
st.markdown("""
<div class="rules-container">
    <h2>Regras da Mega-Sena</h2>
    <ul class="rules-text">
        <li>Escolha de 6 a 15 números entre 1 e 60.</li>
        <li>Aposta mínima: 6 números por R$ 5,00.</li>
        <li>Sorteios: geralmente às quartas e sábados.</li>
        <li>Premiação: acertos de 4, 5 ou 6 números.</li>
        <li>Chances de ganhar (aposta mínima): 1 em 50.063.860.</li>
        <li>Prazo para retirada do prêmio: 90 dias após o sorteio.</li>
    </ul>
    <p class="rules-text">Fonte oficial: <a href="https://www.caixa.gov.br/loterias/mega-sena/" target="_blank">Caixa Econômica Federal</a></p>
</div>
""", unsafe_allow_html=True)

# Adicionar responsividade para dispositivos móveis
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
""", unsafe_allow_html=True)
