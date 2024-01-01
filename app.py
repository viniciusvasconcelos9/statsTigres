import os
import pandas as pd
import streamlit as st

#st.sidebar.divider()
option_menu = [ 'Dados Gerais', 'Indy', 'Game Leaders', 'Team Leaders', 'Game Stats', 'Season Stats']
sidebar_option = st.sidebar.selectbox('Menu',option_menu)
st.sidebar.divider()

@st.cache_data

#FUNÇÃO PARA CAREEGAR ARQUIVO COM DADOS GERAIS DOS ATLETAS
def load_players_data():
    arquivo = "dados/Dados Atletas - Tigres.csv"
    dados = pd.read_csv(arquivo, sep=';')
    return dados

#FUNÇÃO PARA CRIAR DATAFRAME COM DADOS DA PARTIDA
def file_to_df(arquivo):
    nome = arquivo.split('-')

    d = {'Time': nome[3], 'Rodada': nome[2], 'Local': nome[4][:-4], 'Competicao': nome[1], 'Ano': nome[0]}
    df = pd.DataFrame(data=d, index=[0])

    return df

#FUNÇÃO PARA CRIAR DATAFRAME COM DADOS DE TODAS AS PARTIDAS DO BANCO DE DADOS
def load_game_data():
    files = os.listdir("dados/Jogos/indy/")
    #print(files)
    df = {}
    dados_finais = []
    for file in files:
        dados = []
        dados.append(pd.read_csv("dados/Jogos/indy/"+file, sep=','))
        dados.append(file_to_df(file))
        dados.append(pd.read_csv("dados/Jogos/"+file, sep=','))
        dados_finais.append(dados)
    return dados_finais

#FUNÇÃO PARA RETORNAR AS TEMPORADAS DOS JOGOS DO BANCO DE DADOS
def temporadas(df):
    temporadas = []
    for x in range (len(df)):
        ano = df[x][1]['Ano'].to_string(index=False)
        if ano in temporadas:
            continue
        else:
            temporadas.append(ano)
    return temporadas

#FUNÇÃO PARA RETORNAR AS COMPETIÇÕES DOS JOGOS DO BANCO DE DADOS
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

#FUNÇÃO QUE RETORNA OS JOGOS POR COMPETIÇÃO/TEMPORADA
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

#FUNÇÃO QUE RETORNA O DATAFRAME COM DADOS INDIVIDUAIS PARA OS JOGOS SELECIONADOS
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

#FUNÇÃO QUE RETORNA O DATAFRAME COM DADOS GERAIS PARA OS JOGOS SELECIONADOS
def season_stats(df, ano, campeonato):

    new_template = df[0][2]
    template_columns = new_template.columns
    new_dataframe = pd.DataFrame(0, columns=template_columns, index=range(1))

    for x in range(len(df)):
        if df[x][1]['Ano'].to_string(index=False) in ano:
            if df[x][1]['Competicao'].to_string(index=False) in campeonato:
                new_dataframe = pd.concat([new_dataframe, df[x][2]], ignore_index = True)

    return new_dataframe

#FUNÇÃO QUE CALCULA O QB RATING
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
            return df[x][0]    

def geral_stats(df, game):
    game = game.split(' - ')
    for x in range(len(df)):
        if df[x][1]['Ano'].to_string(index=False) == game[0] and df[x][1]['Competicao'].to_string(index=False) == game[1] and df[x][1]['Rodada'].to_string(index=False) == game[2]:
            return df[x][2]



gamestats = load_game_data()
#st.write(gamestats[0][2])
#st.write(gamestats[0][1]['Ano'].to_string(index=False))
#st.write(temporadas(gamestats))
playerstats = load_players_data()

playerstats = playerstats.fillna(0)
df_nome_numero = playerstats.loc[:,['Numero','Apelido']] 

if sidebar_option == 'Dados Gerais':
    st.title('- CADASTRO GERAL DE ATLETAS -')
        
    unique_pos = ['RB','QB','WR','OL','DL','LB','DB']
    selected_pos = st.sidebar.multiselect('Posição', unique_pos, unique_pos)
    df_selected = playerstats[(playerstats.Pos.isin(selected_pos))]

    st.sidebar.write('Número total de atletas: ' + str(df_selected.shape[0]))
    st.dataframe(df_selected, hide_index=True)

elif sidebar_option == "Indy":
    st.title('- ESTATÍSTICAS INDIVIDUAIS -')
    
    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    player = st.sidebar.selectbox('Número do jogador',(playerstats['Nome']))
    option = playerstats[playerstats['Nome'] == player]
    option = float(option['Numero'].to_string(index=False))

    resultado = playerstats[playerstats['Numero'] == option]

    st.sidebar.subheader(resultado['Apelido'].to_string(index=False))
    st.subheader(resultado['Nome'].to_string(index=False))

    col2, col3 = st.sidebar.columns(2)

    col2.write('Posição: ' + resultado['Pos'].to_string(index=False))
    col2.write('Número: ' + (resultado['Numero'].to_string(index=False)).split('.')[0])
    col2.write('Altura: ' + resultado['Altura'].to_string(index=False))
    col2.write('Peso: ' + resultado['Peso'].to_string(index=False))
    col2.write('Idade: ')
    col2.write('Experiência: ')

    col3.write('Supino: ' + resultado['Supino'].to_string(index=False).split('.')[0])
    col3.write('Agachamento: ' + resultado['Agachamento'].to_string(index=False).split('.')[0])
    col3.write('Desenvolvimento: ' + resultado['Desenvolvimento'].to_string(index=False).split('.')[0])
    col3.write('Salto horizontal: ' + resultado['Salto horizontal'].to_string(index=False))
    col3.write('40 yds: ' + resultado['40 yds'].to_string(index=False))
     
    st.divider()
    st.write('Jogos (desde 2024): ')
    gamestats_tratado = df_stats(gamestats, selected_season, selected_comp)
    gamestats_tratado = gamestats_tratado.loc[gamestats_tratado['Numero'] == option]
    

    if resultado['Pos'].to_string(index=False) == 'QB':
        st.write('Pontos feitos: ' + gamestats_tratado['Pontos'].to_string(index=False))
        st.write('Passes lançados: ' + gamestats_tratado['Passes tentados'].to_string(index=False))
        st.write('Passes completos: '+ gamestats_tratado['Passes completos'].to_string(index=False))
        st.write('TD: '+ gamestats_tratado['TD passado'].to_string(index=False))
        st.write('TD corrido: ' + gamestats_tratado['TD corrido'].to_string(index=False))
        st.write('Jardas lançadas: ' + gamestats_tratado['Jardas passadas'].to_string(index=False))
        st.write('Jardas corridas: ' + gamestats_tratado['Jardas corridas'].to_string(index=False))
        st.write('Interceptações: ' + gamestats_tratado['INT'].to_string(index=False))
        qb_rating = rating(gamestats_tratado['Passes tentados'].to_string(index=False), gamestats_tratado['Passes completos'].to_string(index=False), gamestats_tratado['Jardas passadas'].to_string(index=False), gamestats_tratado['TD passado'].to_string(index=False), gamestats_tratado['INT'].to_string(index=False))
        st.write('Rating: '+ str(round(qb_rating, 1)))
    if (resultado['Pos'].to_string(index=False) == "WR" or resultado['Pos'].to_string(index=False) == "RB"):
        st.write('Pontos feitos: ' + gamestats_tratado['Pontos'].to_string(index=False))
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
    if (resultado['Pos'].to_string(index=False) == "DL" or resultado['Pos'].to_string(index=False) == "LB" or resultado['Pos'].to_string(index=False) == "DB"):
        st.write('Tackle: ' + gamestats_tratado['Tackle'].to_string(index=False))
        st.write('Tackle for loss: ' + gamestats_tratado['Tackle for loss'].to_string(index=False))
        st.write('Sack: ' + gamestats_tratado['D-Sack'].to_string(index=False))
        st.write('Interceptações: ' + gamestats_tratado['Interceptação'].to_string(index=False))
        st.write('Passes defletados: ' + gamestats_tratado['Passe defletado'].to_string(index=False))
        st.write('TD: ' + gamestats_tratado['TD defesa'].to_string(index=False))
        st.write('Fumble forçado: ' + gamestats_tratado['FF'].to_string(index=False))
        st.write('Fumble recuperado: ' + gamestats_tratado['FR'].to_string(index=False))
        st.write('Pontos feitos: ' + gamestats_tratado['Pontos'].to_string(index=False))
    st.divider()

elif sidebar_option == 'Game Stats':
    

    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    selected_game = st.sidebar.selectbox('Jogo',jogos(gamestats, selected_season, selected_comp))

    team_gamestats = team_stats(gamestats, selected_game)
    geral_gamestats = geral_stats(gamestats, selected_game)
    geral_gamestats['Yds'] = geral_gamestats['Yds'].fillna(value=0)
    geral_gamestats['Yds'] = geral_gamestats['Yds'].astype(int)
    tigres_gamestats = geral_gamestats[geral_gamestats['Equipe'] == 'Tigres']
    rival_gamestats = geral_gamestats[geral_gamestats['Equipe'] != 'Tigres']
    rival = rival_gamestats['Equipe'].iloc[0]
    pontos_tigres = team_gamestats['TD corrido'].sum()*6 + team_gamestats['TD passado'].sum()*6 + team_gamestats['XP acertado'].sum() + team_gamestats['FG acertado'].sum()*3 + (tigres_gamestats['2-pts'] == "Sim").sum()*2
    pontos_rival = (rival_gamestats['TD'] == "Sim").sum()*6 + (rival_gamestats['FG'] == "Sim").sum()*3 + (rival_gamestats['XP'] == "Sim").sum() + (rival_gamestats['2-pts'] == "Sim").sum()*6

    st.title('- GAME STATS -')
    st.subheader('Tigres ' + str(pontos_tigres).split('.')[0] + ' x ' + str(pontos_rival).split('.')[0] + ' ' + rival)

    st.divider()
    st.subheader('Ataque')

    st.write('Posses: ' + str(tigres_gamestats['Posse'].max()).split('.')[0])
    st.write('Snaps totais: ' + str(team_gamestats['Corridas tentadas'].sum() + team_gamestats['Passes tentados'].sum()))
    st.write('Jardas totais: ' + str(team_gamestats['Jardas passadas'].sum() + team_gamestats['Jardas corridas'].sum()))
    st.write('Jardas corridas/tentativas: ' + str(team_gamestats['Jardas corridas'].sum()) + '/' + str(team_gamestats['Corridas tentadas'].sum()) + ' (' + str(round(team_gamestats['Jardas corridas'].sum()/team_gamestats['Corridas tentadas'].sum(),1)) + ' yds)')
    st.write('TD corrido: ' + str(team_gamestats['TD corrido'].sum()))
    st.write('Passes completos/tentados: ' + str(team_gamestats['Passes completos'].sum()) + '/' + str(team_gamestats['Passes tentados'].sum()) + ' (' + str(round(100*team_gamestats['Passes completos'].sum()/team_gamestats['Passes tentados'].sum(),1)) + '%)')
    st.write('Jardas aéreas: ' + str(team_gamestats['Jardas passadas'].sum()))
    st.write('TD aéreo: ' + str(team_gamestats['TD passado'].sum()))
    st.write('Conversão de 2-pts: ' + str((tigres_gamestats['2-pts'] == "Sim").sum()))
    st.write('Interceptações: ' + str(team_gamestats['INT'].sum()))
    st.write('QB rating: ' + str(round(rating(team_gamestats['Passes tentados'].sum(), team_gamestats['Passes completos'].sum(), team_gamestats['Jardas passadas'].sum(), team_gamestats['TD passado'].sum(), team_gamestats['INT'].sum()), 1)))
    st.write('Sack: ' + str(team_gamestats['O-Sack'].sum()))
    st.write('Total de first downs: ' + str((tigres_gamestats['1st down'] == 'Sim').sum()))
    st.write('Eficiência em 3rd down: ' + str(tigres_gamestats.loc[(tigres_gamestats['1st down'] == 'Sim') & (tigres_gamestats['3rd down'] == "Sim")].shape[0]) + '/'+ str((tigres_gamestats['3rd down'] == 'Sim').sum()))
    st.write('Eficiência em 4th down: '+ str(tigres_gamestats.loc[(tigres_gamestats['1st down'] == 'Sim') & (tigres_gamestats['4th down'] == "Sim")].shape[0]) + '/'+ str((tigres_gamestats['4th down'] == 'Sim').sum()))
    st.write('Eficiência de Red Zone (Situações/TD/FG): ')

    st.divider()
    st.subheader('Defesa')

    st.write('Posses do ataque rival: '+ str(rival_gamestats['Posse'].max()).split('.')[0])
    st.write('Snaps totais: ' + str((rival_gamestats['Jogada'] == 'Corrida').sum() + (rival_gamestats['Jogada'] == 'Passe').sum() + (rival_gamestats['Jogada'] == 'Sack').sum()))
    st.write('Jardas totais: ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])['Yds'].sum() + (rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])['Yds'].sum()))   
    st.write('Jardas corridas(tentativas): ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])['Yds'].sum()) + ' (' + str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])) + ')')
    st.write('TD corrido: ' + str(rival_gamestats.loc[(rival_gamestats['Jogada'] == 'Corrida') & (rival_gamestats['TD'] == "Sim")].shape[0]))
    st.write('Passes completos/tentados: ' + str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Passe']) - (rival_gamestats['Inc'] == 'Sim').sum()) + '/'+ str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])))
    st.write('Jardas aéreas: ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])['Yds'].sum()))
    st.write('TD aéreo: ' + str(rival_gamestats.loc[(rival_gamestats['Jogada'] == 'Passe') & (rival_gamestats['TD'] == "Sim")].shape[0]))
    st.write('Sack: ' + str(rival_gamestats.loc[(rival_gamestats['Sack'] == "Sim")].shape[0]))
    st.write('Tackle for loss: ' + str(team_gamestats['Tackle for loss'].sum()))
    st.write('Interceptações: ' + str(team_gamestats['Interceptação'].sum()))
    st.write('Fumble forçado/recuperados: ' + str(team_gamestats['FF'].sum()) + '/' + str(team_gamestats['FR'].sum()))
    st.write('Total de first downs: ' + str((rival_gamestats['1st down'] == 'Sim').sum()))
    st.write('Eficiência em 3rd down: ' + str(rival_gamestats.loc[(rival_gamestats['1st down'] == 'Sim') & (rival_gamestats['3rd down'] == "Sim")].shape[0]) + '/'+ str((rival_gamestats['3rd down'] == 'Sim').sum()))
    st.write('Eficiência em 4th down: '+ str(rival_gamestats.loc[(rival_gamestats['1st down'] == 'Sim') & (rival_gamestats['4th down'] == "Sim")].shape[0]) + '/'+ str((rival_gamestats['4th down'] == 'Sim').sum()))
    st.write('Eficiência de Red Zone (Situações/TD/FG): ')

    st.divider()
    st.subheader('Special teams')

    st.write('Punt: ' + str(team_gamestats['Punt'].sum()) + '/' + str(team_gamestats['Yds'].sum()) + ' (' + str(round(team_gamestats['Yds'].sum()/team_gamestats['Punt'].sum(),1)) + ' yds)')
    st.write('Field Goal: ' + str(team_gamestats['FG acertado'].sum()) + '/' + str(team_gamestats['FG tentados'].sum()))
    st.write('XP: ' + str(team_gamestats['XP acertado'].sum()) + '/' + str(team_gamestats['XP tentados'].sum()))
    st.write('TD Kickoff Return: ' + str(team_gamestats['TD KO Return'].sum()))
    st.write('TD Punt Return: ' + str(team_gamestats['TD Punt Return'].sum()))

    st.divider()

elif sidebar_option == 'Season Stats':  
    st.title('- SEASON STATS -')

    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    
    
    temp_stats = df_stats(gamestats, selected_season, selected_comp)
    geral_season_stats = season_stats(gamestats, selected_season, selected_comp)
    qtde_jogos = geral_season_stats['Equipe'].nunique()-2

    geral_season_stats['Yds'] = geral_season_stats['Yds'].fillna(value=0)
    geral_season_stats['Yds'] = geral_season_stats['Yds'].astype(int)
    tigres_gamestats = geral_season_stats[geral_season_stats['Equipe'] == 'Tigres']
    rival_gamestats = geral_season_stats[geral_season_stats['Equipe'] != 'Tigres']
    
    st.write('Total de jogos: ' + str(qtde_jogos))
    pontos_tigres = temp_stats['TD corrido'].sum()*6 + temp_stats['TD passado'].sum()*6 + temp_stats['XP acertado'].sum() + temp_stats['FG acertado'].sum()*3 + (tigres_gamestats['2-pts'] == "Sim").sum()*2
    pontos_rival = (rival_gamestats['TD'] == "Sim").sum()*6 + (rival_gamestats['FG'] == "Sim").sum()*3 + (rival_gamestats['XP'] == "Sim").sum() + (rival_gamestats['2-pts'] == "Sim").sum()*6
    
    st.divider()
    st.subheader('Ataque')

    st.write('Posses: ')
    st.write('Total de pontos feitos: ' + str(pontos_tigres).split('.')[0] + ' (*' + str(round(pontos_tigres/qtde_jogos,1)) + '*)')
    snap_totais = temp_stats['Corridas tentadas'].sum() + temp_stats['Passes tentados'].sum() + temp_stats['O-Sack'].sum()
    st.write('Snaps totais: ' + str(snap_totais) + ' (*' + str(round(snap_totais/qtde_jogos,1)) + ' por jogo*)')
    jardas_totais = temp_stats['Jardas passadas'].sum() + temp_stats['Jardas corridas'].sum()
    st.write('Jardas totais: ' + str(jardas_totais) + ' (*' + str(round(jardas_totais/qtde_jogos, 1)) + ' por jogo*)')
    st.write('Jardas corridas/tentativas: ' + str(temp_stats['Jardas corridas'].sum()) + '/' + str(temp_stats['Corridas tentadas'].sum()) + ' (' + str(round(temp_stats['Jardas corridas'].sum()/temp_stats['Corridas tentadas'].sum(),1)) + ' yds por corrida)')
    st.write('TD corrido: ' + str(temp_stats['TD corrido'].sum())  + ' (*' + str(round(temp_stats['TD corrido'].sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('Passes completos/tentados: ' + str(temp_stats['Passes completos'].sum()) + '/' + str(temp_stats['Passes tentados'].sum()) + ' (*' + str(round(100*temp_stats['Passes completos'].sum()/temp_stats['Passes tentados'].sum(),1)) + '%*)')
    st.write('Jardas aéreas: ' + str(temp_stats['Jardas passadas'].sum())  + ' (*' + str(round(temp_stats['Jardas passadas'].sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('TD aéreo: ' + str(temp_stats['TD passado'].sum())  + ' (*' + str(round(temp_stats['TD passado'].sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('Interceptações: ' + str(temp_stats['INT'].sum())  + ' (*' + str(round(temp_stats['INT'].sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('QB rating: ' + str(round(rating(temp_stats['Passes tentados'].sum(), temp_stats['Passes completos'].sum(), temp_stats['Jardas passadas'].sum(), temp_stats['TD passado'].sum(), temp_stats['INT'].sum()), 1)))
    st.write('Sack: ' + str(temp_stats['O-Sack'].sum())  + ' (*' + str(round(temp_stats['O-Sack'].sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('Total de first downs: ' + str((tigres_gamestats['1st down'] == 'Sim').sum())  + ' (*' + str(round((tigres_gamestats['1st down'] == 'Sim').sum()/qtde_jogos, 1)) + ' por jogo*)')
    st.write('Eficiência em 3rd down: ' + str(tigres_gamestats.loc[(tigres_gamestats['1st down'] == 'Sim') & (tigres_gamestats['3rd down'] == "Sim")].shape[0]) + '/'+ str((tigres_gamestats['3rd down'] == 'Sim').sum()))
    st.write('Eficiência em 4th down: '+ str(tigres_gamestats.loc[(tigres_gamestats['1st down'] == 'Sim') & (tigres_gamestats['4th down'] == "Sim")].shape[0]) + '/'+ str((tigres_gamestats['4th down'] == 'Sim').sum()))
    st.write('Eficiência de Red Zone (Situações/TD/FG): ')

    st.divider()
    st.subheader('Defesa')

    st.write('Posses do ataque rival: ')
    st.write('Total de pontos sofridos: ' + str(pontos_rival).split('.')[0] + ' (*' + str(round(pontos_rival/qtde_jogos,1)) + '*)')
    st.write('Snaps totais: ' + str((rival_gamestats['Jogada'] == 'Corrida').sum() + (rival_gamestats['Jogada'] == 'Passe').sum() + (rival_gamestats['Jogada'] == 'Sack').sum()))
    st.write('Jardas totais: ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])['Yds'].sum() + (rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])['Yds'].sum()))   
    st.write('Jardas corridas(tentativas): ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])['Yds'].sum()) + ' (' + str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Corrida'])) + ')')
    st.write('TD corrido: ' + str(rival_gamestats.loc[(rival_gamestats['Jogada'] == 'Corrida') & (rival_gamestats['TD'] == "Sim")].shape[0]))
    st.write('Passes completos/tentados: ' + str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Passe']) - (rival_gamestats['Inc'] == 'Sim').sum()) + '/'+ str(len(rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])))
    st.write('Jardas aéreas: ' + str((rival_gamestats[rival_gamestats['Jogada'] == 'Passe'])['Yds'].sum()))
    st.write('TD aéreo: ' + str(rival_gamestats.loc[(rival_gamestats['Jogada'] == 'Passe') & (rival_gamestats['TD'] == "Sim")].shape[0]))
    st.write('Sack: ' + str(rival_gamestats.loc[(rival_gamestats['Sack'] == "Sim")].shape[0]))
    st.write('Tackle for loss: ' + str(temp_stats['Tackle for loss'].sum()))
    st.write('Interceptações: ' + str(temp_stats['Interceptação'].sum()))
    st.write('Fumble forçado/recuperados: ' + str(temp_stats['FF'].sum()) + '/' + str(temp_stats['FR'].sum()))
    st.write('Total de first downs: ' + str((rival_gamestats['1st down'] == 'Sim').sum()))
    st.write('Eficiência em 3rd down: ' + str(rival_gamestats.loc[(rival_gamestats['1st down'] == 'Sim') & (rival_gamestats['3rd down'] == "Sim")].shape[0]) + '/'+ str((rival_gamestats['3rd down'] == 'Sim').sum()))
    st.write('Eficiência em 4th down: '+ str(rival_gamestats.loc[(rival_gamestats['1st down'] == 'Sim') & (rival_gamestats['4th down'] == "Sim")].shape[0]) + '/'+ str((rival_gamestats['4th down'] == 'Sim').sum()))
    st.write('Eficiência de Red Zone (Situações/TD/FG): ')

    st.divider()
    st.subheader('Special teams')

    st.write('Punt: ' + str(temp_stats['Punt'].sum()) + '/' + str(temp_stats['Yds'].sum()) + ' (' + str(round(temp_stats['Yds'].sum()/temp_stats['Punt'].sum(),1)) + ' yds)')
    st.write('Field Goal: ' + str(temp_stats['FG acertado'].sum()) + '/' + str(temp_stats['FG tentados'].sum()))
    st.write('XP: ' + str(temp_stats['XP acertado'].sum()) + '/' + str(temp_stats['XP tentados'].sum()))
    st.write('TD Kickoff Return: ' + str(temp_stats['TD KO Return'].sum()))
    st.write('TD Punt Return: ' + str(temp_stats['TD Punt Return'].sum()))

    st.divider()
elif sidebar_option == 'Game Leaders':
    st.title('- GAME LEADERS -')
    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    selected_game = st.sidebar.selectbox('Jogo',jogos(gamestats, selected_season, selected_comp))
    setor_option = st.sidebar.selectbox('Setor',['Ataque','Defesa'])
    gamestats_tratado = team_stats(gamestats, selected_game)

    if setor_option == "Defesa":
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
        
        col3.write('Pontos feitos')
        col3.dataframe(team_leaders('Pontos',gamestats_tratado).sort_values(by='Pontos', ascending=False), hide_index=True)

else:
    st.title('- TEAM LEADERS -')
    selected_season = st.sidebar.multiselect('Temporada', temporadas(gamestats),temporadas(gamestats))
    selected_comp = st.sidebar.multiselect('Campeonato', competicoes(gamestats, selected_season), competicoes(gamestats, selected_season))
    setor_option = st.sidebar.selectbox('Setor',['Ataque','Defesa'])
     

    if setor_option == "Defesa":
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
        
        col3.write('Pontos feitos')
        col3.dataframe(team_leaders('Pontos',gamestats_tratado).sort_values(by='Pontos', ascending=False), hide_index=True)