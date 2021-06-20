#!/usr/bin/env python
# coding: utf-8

# In[1]:


def agrega(arquivo, local_base, local_salvar):
    
    """
    -->> Acessa txt de série histórica fornecido pela B3, adequa formatos e salva bases para consulta. <<--, 

    Arg:
        arquivo (str): Obrigatorio - arquivo txt pesquisado
        local_base (str): Obrigatorio - local do arquivo txt acima
        local_salvar (str): Obrigatorio - local a salvar base consolidada 
    """

    import pandas as pd
    import os
    
    # EXTRAI ARQUIVO E SEPARA COLUNAS
    precos = pd.read_csv(local_base + arquivo, header=None)
    precos = precos.drop([precos.index[0], precos.index[len(precos)-1]]).reset_index(drop=True)
    
    precos['TIPREG'] = precos[0].str[0:2]
    precos['DT_PRG'] = precos[0].str[2:10]
    precos['CODBDI'] = precos[0].str[10:12]
    precos['CODNEG'] = precos[0].str[12:24]
    precos['TPMERC'] = precos[0].str[24:27]
    precos['NOMRES'] = precos[0].str[27:39]
    precos['ESPECI'] = precos[0].str[39:49]
    precos['PRAZOT'] = precos[0].str[49:52]
    precos['MODREF'] = precos[0].str[52:56]
    precos['PREABE'] = precos[0].str[56:69]
    precos['PREMAX'] = precos[0].str[69:82]
    precos['PREMIN'] = precos[0].str[82:95]
    precos['PREMED'] = precos[0].str[95:108]
    precos['PREULT'] = precos[0].str[108:121]
    precos['PREOFC'] = precos[0].str[121:134]
    precos['PREOFV'] = precos[0].str[134:147]
    precos['TOTNEG'] = precos[0].str[147:152]
    precos['QUATOT'] = precos[0].str[152:170]
    precos['VOLTOT'] = precos[0].str[170:188]
    precos['PREEXE'] = precos[0].str[188:201]
    precos['INDOPC'] = precos[0].str[201:202]
    precos['DATVEN'] = precos[0].str[202:210]
    precos['FATCOT'] = precos[0].str[210:217]
    precos['PTOEXE'] = precos[0].str[217:230]
    precos['CODISI'] = precos[0].str[230:242]
    precos['DISMES'] = precos[0].str[242:245]

    precos['CODNEG'] = precos['CODNEG'].str.strip()
    precos['NOMRES'] = precos['NOMRES'].str.strip()
    precos['ESPECI'] = precos['ESPECI'].str.strip()
    precos['MODREF'] = precos['MODREF'].str.strip()

    del precos[0]

    # SALVA BASE PARA TRATAMENTO - SALVAR E REABRIR FACILITA O
    # TRATAMENTO DE CAMPOS QUE POSSUEM ESPAÇOS ANTES DE VALORES
    precos.to_csv(local_salvar + 'base_trata.csv',  decimal=',', index=False, sep=';')
    precos2 = pd.read_csv(local_salvar + 'base_trata.csv', sep=';', decimal=',', skipinitialspace=True)
    
    # ACERTA FORMATOS
    precos2['TIPREG'] = precos2['TIPREG'].astype(str).str.zfill(2)
    precos2['CODBDI'] = precos2['CODBDI'].astype(int)
    precos2['TPMERC'] = precos2['TPMERC'].astype(int)
    precos2['INDOPC'] = precos2['INDOPC'].astype(str)
    precos2['DISMES'] = precos2['DISMES'].astype(str).str.zfill(3)

    precos2['PRAZOT'] = precos2['PRAZOT'].fillna(0)
    precos2['PRAZOT'] = precos2['PRAZOT'].astype(int)

    precos2['PREABE'] = precos2['PREABE'].astype(float) / 100
    precos2['PREMAX'] = precos2['PREMAX'].astype(float) / 100
    precos2['PREMIN'] = precos2['PREMIN'].astype(float) / 100
    precos2['PREMED'] = precos2['PREMED'].astype(float) / 100
    precos2['PREULT'] = precos2['PREULT'].astype(float) / 100
    precos2['PREOFC'] = precos2['PREOFC'].astype(float) / 100
    precos2['PREOFV'] = precos2['PREOFV'].astype(float) / 100
    precos2['TOTNEG'] = precos2['TOTNEG'].astype(int)
    precos2['QUATOT'] = precos2['QUATOT'].astype(int)
    precos2['VOLTOT'] = precos2['VOLTOT'].astype(float) / 100
    precos2['PREEXE'] = precos2['PREEXE'].astype(float) / 100
    precos2['FATCOT'] = precos2['FATCOT'].astype(int)
    precos2['PTOEXE'] = precos2['PTOEXE'].astype(float) / 100

    precos2['DT_PRG'] =  pd.to_datetime(precos2['DT_PRG'], format='%Y%m%d')
    precos2['DATVEN'] =  pd.to_datetime(precos2['DATVEN'], format='%Y%m%d', errors = 'coerce')
    
    # ABRE BASE ANTERIOR PARA AGREGAR NOVOS VALORES
    dftotal = pd.read_csv(local_salvar + 'base_total.csv', sep=';', decimal=',', skipinitialspace=True)
    dftotal['DT_PRG'] =  pd.to_datetime(dftotal['DT_PRG'], format='%Y-%m-%d')
    dftotal['DATVEN'] =  pd.to_datetime(dftotal['DATVEN'], format='%Y-%m-%d', errors = 'coerce')
    
    dftotal = dftotal.append(precos2).reset_index(drop=True)
    dftotal = dftotal.drop_duplicates(subset=['DT_PRG', 'CODNEG'], keep='first').reset_index(drop=True)
    dftotal = dftotal.sort_values(by=['DT_PRG']).reset_index(drop=True)
    dftotal = dftotal.drop_duplicates(subset=['DT_PRG', 'CODNEG'], keep='first').reset_index(drop=True)
    
    # SALVA ULTIMA BASE ABERTA E TAMBEM CONSOLIDO COM TODOS OS CAMPOS E ATIVOS
    precos2.to_csv(local_salvar + 'base_ultimo.csv',  decimal=',', index=False, sep=';')
    dftotal.to_csv(local_salvar + 'base_total.csv',  decimal=',', index=False, sep=';')
    
    # SEPARA APENAS MERCADO A VISTA E OPCOES, E CAMPOS DE INTERESSE
    df_hist = dftotal[['DT_PRG', 'CODBDI', 'CODNEG', 'TPMERC', 'NOMRES', 'ESPECI', 'PREABE',
                       'PREULT', 'TOTNEG', 'VOLTOT', 'PREEXE', 'DATVEN', 'CODISI']].copy().reset_index(drop=True)

    df_hist = df_hist[(df_hist['TPMERC'] != 17) & (df_hist['TPMERC'] != 20) &
                      (df_hist['CODBDI'].isin([2, 32, 33, 38, 42, 62, 71, 74, 75, 78, 82]))].reset_index(drop=True)

    # VERIFICA DUPLICACOES E MANTEM POR ORDEM DE PREGAO
    df_hist = df_hist.sort_values(by=['DT_PRG', 'CODNEG']).reset_index(drop=True)
    df_hist = df_hist.drop_duplicates(subset=['DT_PRG', 'CODNEG'], keep='first').reset_index(drop=True)

    # SALVA HISTORICO APENAS COM INFOSMACOES DE INTERESSE
    df_hist.to_csv(local_salvar + 'b3_historico.csv',  decimal=',', index=False, sep=';')
    
    
def volatilidade(D, base, salvar):
    
    """
    -->> Calcula histórico de volatilidade anual para cada ativo
    a partir da rentabilidade e desvio dos ultimos D dias uteis. <<--, 

    Arg:
        D (int): Obrigatório - Dias úteis considerados no cálculo da vol
        base (str): Obrigatorio - arquivo-base a ser utilizado
        salvar (str): Obrigatorio - local a consolidado de volatilidades 
    """
    
    import pandas as pd
    from math import sqrt
    from numpy import log
    from datetime import date, datetime
    
    if type(D) != int:
        print('ERRO FORMATO')
        return False
    
    D = abs(D)

    # CONSULTA BASE PREPARADA PELA FUNCAO ACIMA
    df = pd.read_csv(base + 'b3_historico.csv', sep=';', decimal=',')

    # FILTRA APENAS MERCADO A VISTA
    df_vista = df[df['TPMERC'] == 10].copy().reset_index(drop=True)
    del df_vista['PREEXE']
    del df_vista['DATVEN']

    df_vista = df_vista.sort_values(by=['DT_PRG', 'CODNEG']).reset_index(drop=True)

    # QUANTIDADE DE DIAS COM PREGAO
    dias_pregao = df_vista.nunique()['DT_PRG']

    # REMOVE ATIVOS QUE NAO ESTAO EM TODOS OS DIAS DE NEGOCIACAO
    ativos_por_pregao = df_vista['CODNEG'].value_counts()
    # CASO DESEJE MANTER ATIVOS FALTANTES EM APENAS POUCOS DIAS DENTRO DA BASE,
    # BASTA SUBTRAIR O VALOR DESEJADO APOS dias_pregao NA LINHA ABAIXO
    remover = ativos_por_pregao[ativos_por_pregao < dias_pregao].index
    df_filtra = df_vista[~df_vista['CODNEG'].isin(remover)].reset_index(drop=True)

    df_filtra = df_filtra.sort_values(by=['DT_PRG', 'CODNEG']).reset_index(drop=True)

    # CALCULA RENTABILIDADE DIARIA
    df_filtra['RENT%'] = log(df_filtra['PREULT'] / df_filtra.groupby('CODNEG')['PREULT'].shift(1))

    # CALCULA DESVIO DAS ULTIMAS 22 RENTABILIDADES - alterar a qtde se desejar
    df_filtra['DESV'] = df_filtra.groupby('CODNEG')['RENT%'].rolling(D).std().reset_index(0, drop=True)

    # ANUALIZA VOLATILIDADE
    df_filtra['VOL_ANUAL'] = df_filtra['DESV'] * sqrt(252)

    df_filtra[['RENT%', 'DESV', 'VOL_ANUAL']] = df_filtra[['RENT%', 'DESV', 'VOL_ANUAL']].fillna(0)

    # EXCLUI LINHAS QUE NAO SAO DE INTERESSE
    df_vols = df_filtra[df_filtra['VOL_ANUAL'] != 0].copy().reset_index(drop=True)

    df_vols = df_vols.sort_values(by=['DT_PRG', 'CODNEG']).reset_index(drop=True)

    # SALVA VOLATILIDADES NO DIRETORIO INFORMADO
    df_vols.to_csv(salvar + 'volatilidades_b3.csv',  decimal=',', index=False, sep=';')

