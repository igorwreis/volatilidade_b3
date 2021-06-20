# volatilidade_b3
Calcula histórico de volatilidade de ativos no mercado à vista da bolsa brasileira. 

O programa funciona com base nos arquivos .zip do menu de séries históricas da B3.

É necessário informar as informações abaixo:

D = dias-uteis a serem considerados no calculo da volatilidade
arquivos_zip = r'caminho\\para\\bases\\compactadas\\em\\formato\\.zip\\' # diretório onde constam os arquivos .zip
arquivos_txt = r'caminho\\para\salvar\\bases\em\\form\\.txt\\' # destino arquivos .txt
manipula = r'caminho\\para\\salvar\\arquivos\\.csv\\para\tratamento\\' # local para salvar bases de tratamento
salva_vol = r'caminho\\para\\salvar\\arquivo\\com\volatilidades\\' # local para salvar arquivo final

Caso deseje salvar todos os arquivos utilizados para os cálculos, é preciso ainda criar as subpastas abaixo

arquivoz_zip + 'antigos\\'
arquivos_txt + 'utilizados\\'

Deixar ambos os programas na mesma pasta; Rodar rotina apenas a partir do arquivo 'extrair'
