
# DESCOMPACTA ZIP E ENVIA ARQUIVOS TXT PARA OS DIRETORIO DESEJADOS - informar abaixo
import os, zipfile, glob, shutil
from time import sleep
from funcoes_apoio import agrega, volatilidade # manter modulo no mesmo diretorio deste programa

os.system('mode con: cols=43 lines=12')


# In[2]:


D = 21 # dias-uteis a serem considerados no calculo da volatilidade
arquivos_zip = r'caminho\\para\\bases\\compactadas\\em\\formato\\.zip\\' # arquivos .zip
arquivos_txt = r'caminho\\para\salvar\\bases\em\\form\\.txt\\' # destino arquivos .txt
manipula = r'caminho\\para\\salvar\\arquivos\\.csv\\para\tratamento\\' # local para salvar bases de tratamento
salva_vol = r'caminho\\para\\salvar\\arquivo\\com\volatilidades\\' # local para salvar arquivo final


# In[3]:


# DESCOMPACTA ARQUIVOS
print('\nDescompactando arquivos...\n')
sleep(1)
os.chdir(arquivos_zip)
for item in os.listdir(arquivos_zip):
    if item.endswith('.ZIP'):
        arquivo = os.path.abspath(item)
        zip_ref = zipfile.ZipFile(arquivo)
        zip_ref.extractall(arquivos_txt)
        zip_ref.close()
        try:
            # criar pasta baixo, ou remover o arquivo
            shutil.move(os.path.join(arquivos_zip, arquivo), arquivos_zip + 'antigos\\')
            #os.remove(arquivo) # caso deseje remover os arquivos em vez de move-los
        except:
            pass


# In[4]:


print('Consolidando dados...\n')
sleep(1)
# CONSOLIDA BASE COM NOVOS ARQUIVOS TXT
os.chdir(arquivos_txt)
for item in os.listdir(arquivos_txt):
    if item.endswith('.TXT'):
        try:
            agrega(item, arquivos_txt, manipula)
            # criar pasta baixo, ou remover o arquivo
            shutil.move(os.path.join(arquivos_txt, item), arquivos_txt + 'utilizados\\')
            #os.remove(arquivo) # caso deseje remover os arquivos em vez de move-los
        except:
            pass


# In[5]:


print('Calculando volatilidades...\n')
sleep(1)
# CALCULA VOLATILIDADE ANUAL E SALVA ARQUIVO
volatilidade(D, manipula, salva_vol)
print('Processo finalizado. Verifique arquivos.')
sleep(5)

