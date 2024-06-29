import os

def ler_arquivo_com_os(local):
    try:
        # Abre o arquivo usando um descritor de arquivo
        fd = os.open(local, os.O_RDONLY)
        # Obtém o tamanho do arquivo
        file_size = os.path.getsize(local)
        # Lê o conteúdo do arquivo
        content = os.read(fd, file_size)
        # Fecha o descritor de arquivo
        os.close(fd)
        # Decodifica os bytes para string
        return content.decode('utf-8')
    except FileNotFoundError:
        print(f"O arquivo {local} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

# Caminho para o arquivo de texto
local = os.getcwd() + ""
lista_colaboradores = os.listdir(local + "\\creditos")
for colab in lista_colaboradores:
    local = local + "\\creditos" + "\\" + colab
# Lê o conteúdo do arquivo
conteudo = ler_arquivo_com_os(local)

if conteudo is not None:
    print("Conteúdo do arquivo:")
    print(conteudo)