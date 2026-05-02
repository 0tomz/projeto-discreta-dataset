import pandas as pd
import re
import unicodedata

def padronizar_prolog(texto):
    if pd.isna(texto):
        return "desconhecido"
    texto = str(texto)
    # Remove acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    # Converte para minúsculas
    texto = texto.lower()
    # Substitui tudo que não é letra minúscula ou número por underscore
    texto = re.sub(r'[^a-z0-9]', '_', texto)
    # Remove múltiplos underscores consecutivos
    texto = re.sub(r'_+', '_', texto)
    # Remove underscores das pontas
    texto = texto.strip('_')
    return texto

def gerar_base_prolog(arquivo_entrada, arquivo_saida):
# 1. Extração: Carrega o CSV original
    df = pd.read_csv(arquivo_entrada)

    # 2. Transformação: Restringe aos 7 campos escolhidos
    colunas_selecionadas = ['Driver', 'Nationality', 'Active', 'Race_Starts', 'Race_Wins', 'Podiums', 'Points']
    df_filtrado = df[colunas_selecionadas].copy()
    
    # Aplica a padronização rigorosa para o formato Prolog
    df_filtrado['Driver'] = df_filtrado['Driver'].apply(padronizar_prolog)
    df_filtrado['Nationality'] = df_filtrado['Nationality'].apply(padronizar_prolog)
    df_filtrado['Active'] = df_filtrado['Active'].astype(str).str.lower()
    
    # 3. Carga: Escreve o arquivo com os fatos lógicos
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        for index, row in df_filtrado.iterrows():
            # Formata a string: piloto(nome, nacionalidade, ativo, corridas, vitorias, podios, pontos).
            fato = f"piloto({row['Driver']}, {row['Nationality']}, {row['Active']}, {int(row['Race_Starts'])}, {int(row['Race_Wins'])}, {int(row['Podiums'])}, {row['Points']}).\n"
            f.write(fato)

    print(f"Base de conhecimento gerada com {len(df_filtrado)} pilotos!")



# Executando a função
gerar_base_prolog('F1/F1Drivers_Dataset.pl', 'F1/base_conhecimento_f1.pl')
def filtrar_por_ano_pandas(arquivo_entrada, arquivo_saida, ano):
    # 1. Carrega o arquivo forçando o uso de um separador inexistente ('|') 
    # para não quebrar a estrutura nas vírgulas.
    df = pd.read_csv(arquivo_entrada, sep='|', header=None, names=['texto_bruto'], encoding='utf-8')
    
    # 2. O padrão agora busca apenas o número do ano, já que ele aparece como [2023] ou "[2021, 2022, 2023]"
    padrao = str(ano)
    
    # 3. Aplica a filtragem.
    df_filtrado = df[df['texto_bruto'].str.contains(padrao, regex=True, na=False)]
    
    # 4. Salva no novo arquivo.
    df_filtrado.to_csv(arquivo_saida, index=False, header=False)
    
    print(f"{len(df_filtrado)} pilotos encontrados para o ano {ano}.")
    return df_filtrado['texto_bruto'].tolist()

# Uso
# pilotos_2023 = filtrar_por_ano_pandas('F1/F1Drivers_Dataset.pl', 'F1/f1_2023.pl', 2023)
