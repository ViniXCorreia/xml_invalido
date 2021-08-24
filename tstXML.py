import os
import shutil
import getpass

def defineXML():
    cont = 0
    extensaoXML = ".xml"
    userPC = getpass.getuser()
    userPC = str("\\") + userPC + str("\\")
    print(userPC)
    caminho_pasta = (r"C:\Users" + userPC + "Downloads")
    print(caminho_pasta)
    for raiz, pastas, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            if extensaoXML in arquivo:
                cont+=1
                caminho_completo = os.path.join(raiz, arquivo)
                chaveXML = os.path.splitext(arquivo)[0]
                chaveXMLnfe = str("\\") +chaveXML + str("-nfe") + extensaoXML
                caminho_pastaXMLnfe = caminho_pasta + chaveXMLnfe
                os.rename(caminho_completo, caminho_pastaXMLnfe)
                copia_xml(caminho_pastaXMLnfe, chaveXMLnfe)
                exclui_xml(caminho_pastaXMLnfe)
    print(f"{cont} Arquivos .xml encontrados")

def copia_xml(caminho_completo, chaveXMLnfe):
    raizPC = (r"C:\Program Files (x86)\CompuFour\Clipp\Exe")
    for root, dirs, files in os.walk(raizPC):
        for dir in dirs:
            if dir == "Log":
                path_log_copia = os.path.join(root, dir)
                shutil.copy(caminho_completo, path_log_copia + chaveXMLnfe)
                print(path_log_copia)
            elif dir == "NFe":
                path_nfe_copia = os.path.join(root, dir)
                shutil.copy(caminho_completo, path_nfe_copia + chaveXMLnfe)
                print(path_nfe_copia)

def exclui_xml(caminho_completo):
    os.remove(caminho_completo)
    print("XML movido")

defineXML()
input("Pressione qualquer tecla para encerrar")




