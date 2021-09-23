from pathlib import Path
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import shutil

class Application:
   def __init__(self, master=None):
      self.widget1 = Frame(master)
      self.widget1.pack()
      self.imageC4 = Label(self.widget1, image=img)
      self.imageC4.grid(row = 0, column= 3, sticky=N)
      self.busca = Button(self.widget1)
      self.busca["text"] = "Buscar Arquivo XML"
      self.busca["font"] = ("Calibri", "12")
      self.busca["width"] = 35
      self.busca["height"] = 2
      self.busca["bd"] = 3
      self.busca["command"] = self.buscarArquivo
      self.busca.grid(row=2, column=3, sticky= N)
      self.checkButton = Checkbutton(self.widget1)
      self.checkButton["text"] = "Manter arquivo XML original"
      self.checkButton["height"] = 2
      self.checkButton["font"] = ("Calibri", "12")
      self.checkButton["variable"] = valor_check
      self.checkButton.grid(row = 1, column= 3, sticky = N)
      self.vazio = Label(self.widget1)
      self.vazio["text"] = " "
      self.vazio.grid(row = 4, column = 3)
      self.cancela = Button(self.widget1)
      self.cancela["text"] = "Finalizar"
      self.cancela["font"] = ("Calibri", "10")
      self.cancela["width"] = 25
      self.cancela["height"] = 2
      self.cancela["command"] = self.finalizaArquivo
      self.cancela.grid(row = 5, column=3, sticky= N)
 
   def buscarArquivo(self):
      Tk().withdraw()
      filename = askopenfilename(
         filetypes=[("Arquivos XML", ".xml")],
         initialdir= (home + "\Downloads"),
         title="Buscar XML",
         multiple = False)
      extensaoXML = ("-nfe.xml")
      caminhoChaveXML = os.path.splitext(filename)[0]
      caminhoChaveXML= "{}".format(caminhoChaveXML)
      caminhoChaveXML = caminhoChaveXML + extensaoXML
      caminhoChaveXML= "{}".format(caminhoChaveXML)
      chaveXML = caminhoChaveXML.split("/")
      if len(chaveXML[-1]) == 52:
         chaveXML = chaveXML[-1]
         self.ajustaXML(filename, caminhoChaveXML, chaveXML)  
      elif len(chaveXML[-1]) > 52:
         if chaveXML[-1].find(" ") == 44:
            spacePosition = chaveXML[-1].find(" ")
            tracePosition = chaveXML[-1].find("-")
            teste = chaveXML[-1][spacePosition:tracePosition]
            chaveXML[-1] = chaveXML[-1].replace(teste, "")
            chaveXML = chaveXML[-1]
            self.ajustaXML(filename, caminhoChaveXML, chaveXML)
         else:
            self.vazio["text"] = "Nome do arquivo inválido! Verifique se existem apenas 44 números na chave de acesso!"
      elif len(chaveXML[-1]) > 8 and len(chaveXML[-1]) < 52:
         self.vazio["text"] = "Nome do arquivo inválido! Está faltando números na chave de acesso!"

   def ajustaXML(self, filename, caminhoChaveXML, chaveXML):
         os.rename(filename, caminhoChaveXML)
         self.copiar_xml(caminhoChaveXML, chaveXML)
         os.rename(caminhoChaveXML, filename)
         if valor_check.get() == 0:
            self.checkButton["command"] = self.apaga_xml(filename)

   def copiar_xml(self, caminhoChaveXML, chaveXML):
      verificaLog = False
      verificaNfe = False
      for root, dirs, files in os.walk(dirUsado):
         for dir in dirs:
               if dir == "Log" or dir == "log":
                  path_log_copia = os.path.join(root, dir)
                  shutil.copy(caminhoChaveXML, path_log_copia + "/" + chaveXML )
                  verificaLog = True
                  for raiz, pastas, arquivos in os.walk(path_log_copia):
                     for pasta in pastas:
                        if pasta == "NFe" or pasta == "Nfe":
                           path_nfe_copia = os.path.join(raiz, pasta)
                           shutil.copy(caminhoChaveXML, path_nfe_copia + "/" + chaveXML)
                           self.vazio["text"] = "Arquivo XML ajustado com sucesso!"
                           verificaNfe = True
      if not verificaLog:
         newDir = os.path.join(dirUsado, "Log")
         os.mkdir(newDir)
         newDirNFe = os.path.join(newDir, "NFe")
         os.mkdir(newDirNFe)
         self.copiar_xml(caminhoChaveXML, chaveXML)
         self.vazio["text"] = "Pasta Log e NFe criadas! Arquivo XML ajustado com sucesso"
      elif not verificaNfe:
         self.vazio["text"] = "Pasta NFe não encontrada, entre em contato com o Suporte Técnico!"
      
   
   def apaga_xml(self, filename):
      os.remove(filename)

   def finalizaArquivo(self):
      root.quit()

root = Tk()
root.title("Ajuste XML")
width_window = 550
height_window = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
posx = screen_width/2 - width_window/2
posy = screen_height/2 - height_window/2
root.geometry("%dx%d+%d+%d" %(width_window, height_window, posx, posy))
root.resizable(width=False, height=False)
dirUsado = os.getcwd()
root.iconbitmap(os.path.join(dirUsado, "Imagens\c4red.ico"))
img = PhotoImage(file= os.path.join(dirUsado, "Imagens\c4.png"))
valor_check = IntVar()
home = str(Path.home())
Application(root)
root.mainloop()
