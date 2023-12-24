import os
import pandas as pd
import streamlit as st




st.title('Estatísticas - Tigres FA')

st.sidebar.image('tigres.png', width=150)

sidebar_option = st.sidebar.selectbox('Menu',['Team Leaders', 'Indy', 'Game stats', 'Dados Gerais'])
@st.cache_data


def load_players_data():
    arquivo = "dados/Dados Atletas - Tigres.csv"
    dados = pd.read_csv(arquivo, sep=';')
    return dados

def file_to_df(arquivo):
    nome = arquivo.split('-')

    d = {'Time': nome[3], 'Rodada': nome[2], 'Local': nome[4][:-4], 'Competicao': nome[1], 'Ano': nome[0]}
    df = pd.DataFrame(data=d, index=[0])

    return df

def load_game_data():
    files = os.listdir("dados/Jogos/")
    #print(files)
    df = {}
    dados_finais = []
    for file in files:
        dados = []
        dados.append(pd.read_csv("dados/Jogos/"+file, sep=','))
        dados.append(file_to_df(file))
        dados_finais.append(dados)
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

def jogos (df, temporada, competicao):
    games = []
    for x in range (len(df)):
        if df[x][1]['Ano'].to_string(index=False) in temporada:
            if df[x][1]['Competicao'].to_string(index=False) in competicao:
                game = df[x][1]['Ano'].to_string(index=False) + ' - ' + df[x][1]['Competicao'].to_string(index=False) + ' - ' + df[x][1]['Rodada'].to_string(index=False) + ' - vs. ' + df[x][1]['Time'].to_string(index=False)+ ' - ' + df[x][1]['Local'].to_string(index=False)
                if game in games:
                    continue
                else:
                    games.append(game)
    return games

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

def df_team_stats(df, game):
    jogo = game.split('-')
    
    #for x in range(len(df)):



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

def team_leaders(stat_name,df_gamestats):
    stats = df_gamestats.loc[:,['Numero',stat_name]]
    stats = df_nome_numero.merge(stats, on='Numero', how='left')
    stats = stats[stats[stat_name] > 0]

    return stats

def team_stats(df, game):
    game = game.split(' - ')
    for x in range(len(df)):
        if df[x][1]['Ano'].to_string(index=False) == game[0] and df[x][1]['Competicao'].to_string(index=False) == game[1] and df[x][1]['Rodada'].to_string(index=False) == game[2]:
            print('ok1') 
            return df[x][0]       


gamestats = load_game_data()
#st.write(gamestats[0][1])
#st.write(gamestats[0][1]['Ano'].to_string(index=False))
#st.write(temporadas(gamestats))
playerstats = load_players_data()

playerstats = playerstats.fillna(0)

if sidebar_option == 'Dados Gerais':
    
    st.header('Cadastro Geral de Atletas')

    
    unique_pos = ['RB','QB','WR','OL','DL','LB','DB']
    selected_pos = st.sidebar.multiselect('Posição', unique_pos, unique_pos)
    df_selected = playerstats[(playerstats.Pos.isin(selected_pos))]

    st.sidebar.write('Número total de atletas: ' + str(df_selected.shape[0]))
    st.dataframe(df_selected, hide_index=True)

elif sidebar_option == "Indy":
    #st.header('Estatísticas Individuais')

    option = st.sidebar.selectbox('Número do jogador',(playerstats['Numero']))
    resultado = playerstats[playerstats['Numero'] == option]
    st.sidebar.subheader(resultado['Apelido'].to_string(index=False))
    st.subheader(resultado['Nome'].to_string(index=False))
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
    st.write('Jogos (desde 2024): ')
    gamestats_tratado = df_stats(gamestats, selected_season, selected_comp)
    gamestats_tratado = gamestats_tratado.loc[gamestats_tratado['Numero'] == option]
    
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
    if resultado['Pos'].to_string(index=False) == "LB":
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

elif sidebar_option == 'Game stats':

    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    selected_game = st.sidebar.selectbox('Jogo',jogos(gamestats, selected_season, selected_comp))

    team_gamestats = team_stats(gamestats, selected_game)
    #st.dataframe(team_gamestats)

    st.subheader('Ataque')

    st.write('Jardas totais: ' + str(team_gamestats['Jardas passadas'].sum()))
    st.write('Snaps totais: ' + str(team_gamestats['Corridas tentadas'].sum() + team_gamestats['Passes tentados'].sum()))
    st.write('Jardas corridas/tentativas: ' + str(team_gamestats['Jardas corridas'].sum()) + '/' + str(team_gamestats['Corridas tentadas'].sum()))
    st.write('TD corrido: ' + str(team_gamestats['TD corrido'].sum()))
    st.write('Passes completos/tentados: ' + str(team_gamestats['Passes completos'].sum()) + '/' + str(team_gamestats['Passes tentados'].sum()))
    st.write('Jardas aéreas: ' + str(team_gamestats['Jardas passadas'].sum()))
    st.write('TD aéreo: ' + str(team_gamestats['TD passado'].sum()))
    st.write('Total de first downs: ')
    st.write('Eficiência em 3rd down: ')

    st.subheader('Defesa')
    st.subheader('Special teams')

else:
    setor_option = st.sidebar.selectbox('Setor',['Ataque','Defesa'])
    df_nome_numero = playerstats.loc[:,['Numero','Apelido']]  

    if setor_option == "Defesa":
        selected_season = st.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
        selected_comp = st.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
        gamestats_tratado = df_stats(gamestats, selected_season, selected_comp) 
        col2, col3 = st.columns(2)

        
        col2.write('Tackle')
        col2.dataframe(team_leaders('Tackle',gamestats_tratado).sort_values(by='Tackle', ascending=False), hide_index=True)

        col3.write('Tackle for loss')
        col3.dataframe(team_leaders('Tackle for loss',gamestats_tratado).sort_values(by='Tackle for loss', ascending=False), hide_index=True)

        col2.write('Sack')
        col2.dataframe(team_leaders('D-Sack',gamestats_tratado).sort_values(by='D-Sack', ascending=False), hide_index=True)
        
        col3.write('Interceptações')
        col3.dataframe(team_leaders('Interceptação',gamestats_tratado).sort_values(by='Interceptação', ascending=False), hide_index=True)
        
        col3.write('Fumble forçado')
        col3.dataframe(team_leaders('FF',gamestats_tratado).sort_values(by='FF', ascending=False), hide_index=True)
        
        col3.write('Fumble recuperado')
        col3.dataframe(team_leaders('FR',gamestats_tratado).sort_values(by='FR', ascending=False), hide_index=True)
        
        col3.write('Passe defletado')
        col3.dataframe(team_leaders('Passe defletado',gamestats_tratado).sort_values(by='Passe defletado', ascending=False), hide_index=True)
        
    if setor_option == "Ataque":
        selected_season = st.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
        selected_comp = st.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
        gamestats_tratado = df_stats(gamestats, selected_season, selected_comp)

        col2, col3 = st.columns(2)

        
        col2.write('Passes recebidos')
        col2.dataframe(team_leaders('Passes recebidos',gamestats_tratado).sort_values(by='Passes recebidos', ascending=False), hide_index=True)
        
        col3.write('Alvo')
        col3.dataframe(team_leaders('Alvo',gamestats_tratado).sort_values(by='Alvo', ascending=False), hide_index=True)
        
        col2.write('Jardas recebidas')
        col2.dataframe(team_leaders('Jardas recebidas',gamestats_tratado).sort_values(by='Jardas recebidas', ascending=False), hide_index=True)
        
        col3.write('TD aéreo')
        col3.dataframe(team_leaders('TD recebendo',gamestats_tratado).sort_values(by='TD recebendo', ascending=False), hide_index=True)
        
        col2.write('Corridas tentadas')
        col2.dataframe(team_leaders('Corridas tentadas',gamestats_tratado).sort_values(by='Corridas tentadas', ascending=False), hide_index=True)
        
        col3.write('Jardas corridas')
        col3.dataframe(team_leaders('Jardas corridas',gamestats_tratado).sort_values(by='Jardas corridas', ascending=False), hide_index=True)
        
        col2.write('TD corrido')
        col2.dataframe(team_leaders('TD corrido',gamestats_tratado).sort_values(by='TD corrido', ascending=False), hide_index=True)
        