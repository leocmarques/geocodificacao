import streamlit as st
import pandas as pd
import requests

# Título do app
st.title("Geocodificação com Geoapify")

# Entrada para a chave de API
api_key = st.text_input("Insira sua chave de API Geoapify:", type="password")

# Upload do arquivo com endereços
uploaded_file = st.file_uploader("Carregar arquivo Excel com endereços", type=["xlsx"])

# Função para geocodificar um endereço
def geoapify_geocode_address(address, api_key):
    url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data["features"]:
        location = data["features"][0]["geometry"]["coordinates"]
        return location[1], location[0]  # Retorna latitude e longitude
    return None, None

if uploaded_file and api_key:
    # Leitura do arquivo Excel
    df = pd.read_excel(uploaded_file)
    
    # Exibe a tabela inicial
    st.write("Primeiras linhas do arquivo carregado:")
    st.write(df.head())
    
    # Dropdown para selecionar a coluna de endereços
    address_column = st.selectbox("Selecione a coluna que contém os endereços:", df.columns)
    
    if address_column:
        # Filtra as primeiras 10 linhas como exemplo
        df_filtered = df.iloc[0:10]
        
        # Aplica a geocodificação
        st.write("Geocodificando os endereços...")
        df_filtered["latitude"], df_filtered["longitude"] = zip(*df_filtered[address_column].apply(lambda x: geoapify_geocode_address(x, api_key)))
        
        # Exibe o DataFrame com as coordenadas
        st.write("Resultados da Geocodificação:")
        st.write(df_filtered)
        
        # Opção para download do arquivo resultante
        output_file = "enderecos_geocodificados.xlsx"
        df_filtered.to_excel(output_file, index=False)
        st.download_button(label="Baixar arquivo com coordenadas", data=open(output_file, "rb"), file_name=output_file)
