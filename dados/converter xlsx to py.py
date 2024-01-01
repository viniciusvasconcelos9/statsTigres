import pandas as pd
import os

files = os.listdir("Jogos XLSX/")

for file in files:
    
    indy = pd.read_excel("Jogos XLSX/" + file, sheet_name = 'Indy' ) #geral
    sobre = pd.read_excel("Jogos XLSX/" + file, sheet_name = 'Sobre')
    
    ano = sobre['Ano'].to_string(index=False)
    camp = sobre['Competicao'].to_string(index=False)
    print(camp)
    rodada = sobre['Rodada'].to_string(index=False)
    time = sobre['Time'].to_string(index=False)
    local = sobre['Local'].to_string(index=False)
    nome = ano+'-'+camp+'-'+rodada+'-'+time+'-'+local+'.csv'
    indy.to_csv(nome)



