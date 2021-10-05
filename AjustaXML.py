from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import webbrowser
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
      self.busca.grid(row=3, column=3, sticky= N)
      self.portalNfe = Button(self.widget1)
      self.portalNfe["text"] = "Acessar Consulta NFe"
      self.portalNfe["font"] = ("Calibri", "12")
      self.portalNfe["bd"] = 0
      self.portalNfe["fg"] = "#2548E3"
      self.portalNfe["command"] = self.openSite
      self.portalNfe.grid(row = 1, column=3)
      self.checkButton = Checkbutton(self.widget1)
      self.checkButton["text"] = "Manter arquivo XML original"
      self.checkButton["height"] = 2
      self.checkButton["font"] = ("Calibri", "12")
      self.checkButton["variable"] = valor_check
      self.checkButton.grid(row = 2, column= 3, sticky = N)
      self.vazio = Label(self.widget1)
      self.vazio["text"] = " "
      self.vazio.grid(row = 5, column = 3)
      self.cancela = Button(self.widget1)
      self.cancela["text"] = "Finalizar"
      self.cancela["font"] = ("Calibri", "10")
      self.cancela["width"] = 25
      self.cancela["height"] = 2
      self.cancela["command"] = self.finalizaArquivo
      self.cancela.grid(row = 6, column=3, sticky= N)
 
   def buscarArquivo(self):
      Tk().withdraw()
      filename = askopenfilename(
         filetypes=[("Arquivos XML", ".xml")],
         initialdir= (home + "\Downloads"),
         title="Buscar XML",
         multiple = False)
      extensaoXML = ("-nfe.xml")
      caminhoChaveXML = os.path.splitext(filename)[0]
      caminhoChaveXML = caminhoChaveXML + extensaoXML
      chaveXML = caminhoChaveXML.split("/")
      print(caminhoChaveXML)
      print(chaveXML)
      if len(chaveXML[-1]) == 52:
         chaveXML = chaveXML[-1]
         self.ajustaXML(filename, caminhoChaveXML, chaveXML)  
      elif len(chaveXML[-1]) > 52:
         if chaveXML[-1].find(" ") == 44:
            spacePosition = chaveXML[-1].find(" ")
            tracePosition = chaveXML[-1].find("-nfe")
            teste = chaveXML[-1][spacePosition:tracePosition]
            chaveXML[-1] = chaveXML[-1].replace(teste, "")
            chaveXML = chaveXML[-1]
            self.ajustaXML(filename, caminhoChaveXML, chaveXML)
         else:
            messagebox.showerror("Ajuste XML", "Nome do arquivo inválido! \nVerifique se existem apenas 44 números na chave de acesso!")
      elif len(chaveXML[-1]) > 8 and len(chaveXML[-1]) < 52:
         messagebox.showerror("Ajuste XML", "Nome do arquivo inválido! \nEstá faltando números na chave de acesso!")
      else:
         messagebox.showerror("Ajusta XML", "Ocorreu um erro, entre em contato com o Suporte Técnico!")

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
            if dir.lower() == "log":
               path_log_copia = os.path.join(root, dir)
               shutil.copy(caminhoChaveXML, path_log_copia + "/" + chaveXML )
               verificaLog = True
               for raiz, pastas, arquivos in os.walk(path_log_copia):
                  for pasta in pastas:
                     if pasta.lower() == "nfe":
                        path_nfe_copia = os.path.join(raiz, pasta)
                        shutil.copy(caminhoChaveXML, path_nfe_copia + "/" + chaveXML)
                        messagebox.showinfo("Ajuste XML", "Arquivo XML ajustado com sucesso! \nConsulte novamente sua NFe!")
                        verificaNfe = True
      if not verificaLog:
         newDir = os.path.join(dirUsado, "Log")
         os.mkdir(newDir)
         newDirNFe = os.path.join(newDir, "NFe")
         os.mkdir(newDirNFe)
         messagebox.showwarning("Ajuste XML", "Pastas Log e Nfe criadas!")
         self.copiar_xml(caminhoChaveXML, chaveXML)
      elif not verificaNfe:
         messagebox.showerror("Ajuste XML", "Pasta Nfe não encontrada! \nEntre em contato com o Suporte Técnico!")
      
   
   def apaga_xml(self, filename):
      os.remove(filename)
   
   def openSite(self):
      webbrowser.open("https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx?tipoConsulta=resumo&tipoConteudo=d09fwabTnLk=")

   def finalizaArquivo(self):
      root.quit()

root = Tk()
root.title("Ajuste XML")
width_window = 550
height_window = 530
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
posx = screen_width/2 - width_window/2
posy = screen_height/2 - height_window/2
root.geometry("%dx%d+%d+%d" %(width_window, height_window, posx, posy))
root.resizable(width=False, height=False)
dirUsado = os.getcwd()
root.iconbitmap(os.path.join(dirUsado, "Imagens\c4red.ico"))
img = PhotoImage(file= os.path.join(dirUsado, "Imagens\c4.png"))
valor_check = IntVar(value=1)
home = str(Path.home())
Application(root)
root.mainloop()
