import pathlib
from pathlib import Path
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
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
      for i in chaveXML:
         if len(i) == 52:
            chaveXML = i
      os.rename(filename, caminhoChaveXML)
      self.copiar_xml(caminhoChaveXML, chaveXML)
      os.rename(caminhoChaveXML, filename)
      if valor_check.get() == 0:
         self.checkButton["command"] = self.apaga_xml(filename)
      

   def copiar_xml(self, caminhoChaveXML, chaveXML):
      for root, dirs, files in os.walk(dirUsado):
         for dir in dirs:
               if dir == "Log":
                  path_log_copia = os.path.join(root, dir)
                  shutil.copy(caminhoChaveXML, path_log_copia + "/" + chaveXML )
               elif dir == "NFe":
                  path_nfe_copia = os.path.join(root, dir)
                  shutil.copy(caminhoChaveXML, path_nfe_copia + "/" + chaveXML)
      self.vazio["text"] = "Arquivo XML movido com sucesso!"
   
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
