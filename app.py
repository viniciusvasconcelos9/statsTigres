import os
import pandas as pd
import streamlit as st




st.title('Estatísticas - Tigres FA')

#st.sidebar.image('tigres.png')
sidebar_option = st.sidebar.selectbox('Menu',['Dados Gerais','Team Leaders', 'Indy'])
@st.cache_data


def load_players_data():
    arquivo = "dados/Dados Atletas - Tigres.csv"
    dados = pd.read_csv(arquivo, sep=';')
    return dados

def file_to_df(arquivo):
    nome = arquivo.split('-')
    print(nome[3])

    d = {'Time': nome[3], 'Rodada': nome[2], 'Local': nome[4][:-4], 'Competicao': nome[1], 'Ano': nome[0]}
    df = pd.DataFrame(data=d, index=[0])
    print(df)

    return df

def load_game_data():
    files = os.listdir("dados/Jogos/")
    #print(files)
    df = {}
    dados_finais = []
    for file in files:
        print(file)
        dados = []
        dados.append(pd.read_csv("dados/Jogos/"+file, sep=','))
        dados.append(file_to_df(file))
        dados_finais.append(dados)
        print(dados[0])
    return dados_finais

def temporadas(df):
    temporadas = []
    for x in range (len(df)):
        ano = df[x][1]['Ano'].to_string(index=False)
        if ano in temporadas:
            continue
        else:
            temporadas.append(ano)
    return temporadas

def competicoes (df, temporada):
    camp = []
    for x in range (len(df)):
        if df[x][1]['Ano'].to_string(index=False) in temporada:
            comp = df[x][1]['Competicao'].to_string(index=False)
            if comp in camp:
                continue
            else:
                camp.append(comp)
    return camp 

def df_stats(df, ano, campeonato):
    
    new_template = df[0][0]
    template_columns = new_template.columns
    new_dataframe = pd.DataFrame(0, columns=template_columns, index=range(100))

    for x in range(len(df)):
        if df[x][1]['Ano'].to_string(index=False) in ano:
            if df[x][1]['Competicao'].to_string(index=False) in campeonato:
                new_dataframe += df[x][0]
    new_dataframe['Numero'] = range(100)         
    return new_dataframe

def rating(att, comp, yds, td, ints):

    a = (int(comp) / int(att) - 0.3) * 5
    b = (int(yds) / int(att) - 3) * 0.25
    c = (int(td) / int(att)) * 20
    d = 2.375 - (int(ints) / int(att) * 25)

    a = min(max(a, 0), 2.375)
    b = min(max(b, 0), 2.375)
    c = min(max(c, 0), 2.375)
    d = min(max(d, 0), 2.375)

    rat = ((a + b + c + d) / 6) * 100

    return rat


gamestats = load_game_data()
#st.write(gamestats[0][1]['Ano'].to_string(index=False))
#st.write(temporadas(gamestats))
playerstats = load_players_data()
playerstats = playerstats.fillna(0)

if sidebar_option == 'Dados Gerais':
    
    st.header('Cadastro Geral de Atletas')

    
    unique_pos = ['RB','QB','WR','OL','DL','LB','DB']
    selected_pos = st.multiselect('Position', unique_pos, unique_pos)
    df_selected = playerstats[(playerstats.Pos.isin(selected_pos))]

    st.write('Número total de atletas: ' + str(df_selected.shape[0]))
    st.dataframe(df_selected, hide_index=True)

elif sidebar_option == "Indy":
    #st.header('Estatísticas Individuais')


    #st.write(playerstats['Numero'])
    option = st.sidebar.selectbox('Número do jogador',(playerstats['Numero']))
    resultado = playerstats[playerstats['Numero'] == option]
    st.sidebar.subheader(resultado['Apelido'].to_string(index=False))

    col2, col3 = st.sidebar.columns(2)

    col2.write('Posição: ' + resultado['Pos'].to_string(index=False))
    col2.write('Altura: ' + resultado['Altura'].to_string(index=False))
    col2.write('Peso: ' + resultado['Peso'].to_string(index=False))
    col2.write('Idade: ')
    col2.write('Experiência: ')

    col3.write('Supino: ' + resultado['Supino'].to_string(index=False))
    col3.write('Agachamento: ' + resultado['Agachamento'].to_string(index=False))
    col3.write('Desenvolvimento: ' + resultado['Desenvolvimento'].to_string(index=False))
    col3.write('Salto horizontal: ' + resultado['Salto horizontal'].to_string(index=False))
    col3.write('40 yds: ' + resultado['40 yds'].to_string(index=False))
    
    st.subheader('Estatísticas')
      
    selected_season = st.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))

    gamestats_tratado = df_stats(gamestats, selected_season, selected_comp)
    gamestats_tratado = gamestats_tratado.loc[gamestats_tratado['Numero'] == option]
    st.write(gamestats_tratado)
    if resultado['Pos'].to_string(index=False) == 'QB':
        st.write('Passes lançados: ' + gamestats_tratado['Passes tentados'].to_string(index=False))
        st.write('Passes completos: '+ gamestats_tratado['Passes completos'].to_string(index=False))
        st.write('TD: '+ gamestats_tratado['TD passado'].to_string(index=False))
        st.write('TD corrido: ' + gamestats_tratado['TD corrido'].to_string(index=False))
        st.write('Jardas lançadas: ' + gamestats_tratado['Jardas passadas'].to_string(index=False))
        st.write('Jardas corridas: ' + gamestats_tratado['Jardas corridas'].to_string(index=False))
        st.write('Interceptações: ' + gamestats_tratado['INT'].to_string(index=False))
        qb_rating = rating(gamestats_tratado['Passes tentados'].to_string(index=False), gamestats_tratado['Passes completos'].to_string(index=False), gamestats_tratado['Jardas passadas'].to_string(index=False), gamestats_tratado['TD passado'].to_string(index=False), gamestats_tratado['INT'].to_string(index=False))
        st.write('Rating: '+ str(round(qb_rating, 1)))
    if resultado['Pos'].to_string(index=False) == "RB":
        st.write('Corridas tentadas: ' + gamestats_tratado['Corridas tentadas'].to_string(index=False))
        st.write('Jardas corridas: ' + gamestats_tratado['Jardas corridas'].to_string(index=False))
        st.write('TD correndo: ' + gamestats_tratado['TD corrido'].to_string(index=False))
        st.write('Alvo: ' + gamestats_tratado['Alvo'].to_string(index=False))
        st.write('Passes recebidos: ' + gamestats_tratado['Passes recebidos'].to_string(index=False))
        st.write('Drop: ' + gamestats_tratado['Drop'].to_string(index=False))
        st.write('Jardas recebidas: ' + gamestats_tratado['Jardas recebidas'].to_string(index=False))
        st.write('TD recebendo: ' + gamestats_tratado['TD recebendo'].to_string(index=False))
        st.write('Fumble: ' + gamestats_tratado['Fumbles sofridos'].to_string(index=False))
    if resultado['Pos'].to_string(index=False) == "WR":
        st.write('Alvo: ' + gamestats_tratado['Alvo'].to_string(index=False))
        st.write('Passes recebidos: ' + gamestats_tratado['Passes recebidos'].to_string(index=False))
        st.write('Drop: ' + gamestats_tratado['Drop'].to_string(index=False))
        st.write('Jardas recebidas: ' + gamestats_tratado['Jardas recebidas'].to_string(index=False))
        st.write('TD recebendo: ' + gamestats_tratado['TD recebendo'].to_string(index=False))
        st.write('Corridas tentadas: ' + gamestats_tratado['Corridas tentadas'].to_string(index=False))
        st.write('Jardas corridas: ' + gamestats_tratado['Jardas corridas'].to_string(index=False))
        st.write('TD correndo: ' + gamestats_tratado['TD corrido'].to_string(index=False))
        st.write('Fumble: ' + gamestats_tratado['Fumbles sofridos'].to_string(index=False))
    if resultado['Pos'].to_string(index=False) == "OL":
        st.subheader('OL')
    if resultado['Pos'].to_string(index=False) == "DL":
        st.write('Tackle: ' + gamestats_tratado['Tackle'].to_string(index=False))
        st.write('Tackle for loss: ' + gamestats_tratado['Tackle for loss'].to_string(index=False))
        st.write('Sack: ' + gamestats_tratado['D-Sack'].to_string(index=False))
        st.write('Interceptações: ' + gamestats_tratado['Interceptação'].to_string(index=False))
        st.write('Passes defletados: ' + gamestats_tratado['Passe defletado'].to_string(index=False))
        st.write('TD: ' + gamestats_tratado['TD defesa'].to_string(index=False))
        st.write('Fumble forçado: ' + gamestats_tratado['FF'].to_string(index=False))
        st.write('Fumble recuperado: ' + gamestats_tratado['FR'].to_string(index=False))
    if resultado['Pos'].to_string(index=False) == "DB":
        st.write('Tackle: ' + gamestats_tratado['Tackle'].to_string(index=False))
        st.write('Tackle for loss: ' + gamestats_tratado['Tackle for loss'].to_string(index=False))
        st.write('Sack: ' + gamestats_tratado['D-Sack'].to_string(index=False))
        st.write('Interceptações: ' + gamestats_tratado['Interceptação'].to_string(index=False))
        st.write('Passes defletados: ' + gamestats_tratado['Passe defletado'].to_string(index=False))
        st.write('TD: ' + gamestats_tratado['TD defesa'].to_string(index=False))
        st.write('Fumble forçado: ' + gamestats_tratado['FF'].to_string(index=False))
        st.write('Fumble recuperado: ' + gamestats_tratado['FR'].to_string(index=False))

else:
    setor_option = st.sidebar.selectbox('Setor',['Ataque','Defesa'])
    if setor_option == "Defesa":
        selected_season = st.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
        selected_comp = st.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
        gamestats_tratado = df_stats(gamestats, selected_season, selected_comp)

        col2, col3, col4 = st.columns(3)

        col2.write('Tackle')
        tackle_stats = gamestats_tratado.sort_values(by='Tackle', ascending=False).iloc[0:10]
        tackle_stats = tackle_stats.loc[:,['Numero','Tackle']]
        col2.dataframe(tackle_stats, hide_index=True)

        col3.write('Tackle for loss')
        tackle_stats = gamestats_tratado.sort_values(by='Tackle for loss', ascending=False).iloc[0:5]
        tackle_stats = tackle_stats.loc[:,['Numero','Tackle for loss']]
        col3.dataframe(tackle_stats, hide_index=True)

        col4.write('Sack')
        tackle_stats = gamestats_tratado.sort_values(by='D-Sack', ascending=False).iloc[0:5]
        tackle_stats = tackle_stats.loc[:,['Numero','D-Sack']]
        col4.dataframe(tackle_stats, hide_index=True)
        
        col2.write('Interceptações')
        tackle_stats = gamestats_tratado.sort_values(by='Interceptação', ascending=False).iloc[0:10]
        tackle_stats = tackle_stats.loc[:,['Numero','Interceptação']]
        col2.dataframe(tackle_stats, hide_index=True)

        col3.write('Passe defletado')
        tackle_stats = gamestats_tratado.sort_values(by='Passe defletado', ascending=False).iloc[0:5]
        tackle_stats = tackle_stats.loc[:,['Numero','Passe defletado']]
        col3.dataframe(tackle_stats, hide_index=True)

        col4.write('Fumble forçado')
        tackle_stats = gamestats_tratado.sort_values(by='FF', ascending=False).iloc[0:5]
        tackle_stats = tackle_stats.loc[:,['Numero','FF']]
        col4.dataframe(tackle_stats, hide_index=True)

        col4.write('Fumble recuperado')
        tackle_stats = gamestats_tratado.sort_values(by='FR', ascending=False).iloc[0:5]
        tackle_stats = tackle_stats.loc[:,['Numero','FR']]
        col4.dataframe(tackle_stats, hide_index=True)
