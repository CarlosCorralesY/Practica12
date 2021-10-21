from Lexer import return_tokens
from Lexer import entrada
import pandas as pd
import graphviz


class nodo: 
    global id
    def __init__(self, token, valor, padre = None):
      self.children = []
      self.valor = valor
      self.token = token
      self.visitado = False 
      self.dead = False 
      
    def agregar_hijo(self, hijo):
      self.children.append(hijo)
      hijo.padre = self

    def Preorden(self): 
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          nodes.pop(0)
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])

    def insertS(self, hijo, numero): 
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          if len(curr.children) == 0 and curr.dead == False:
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return
          nodes.pop(0)
          cont = 0
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])
              if curr.children[it].visitado == True:
                cont = cont + 1
          if cont == 0 and curr.dead == False:
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return

    def visitarNodo(self):
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          if curr.visitado == True:
            curr.dead = True
          if curr.visitado == False:
            curr.visitado = True
            return
          nodes.pop(0)
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it]) 

def sintaxis(): 
  if len(entrada) == 0:
    print ("Correcta")
    return True
  else:
    print ("Incorrecta")
    return False 

def parsing():
  stack = return_tokens('Prueba.txt') 

  df = pd.read_csv('tablaF.csv', index_col=0)

  stack =["$"] 
  entrada.append("$")
  valorToken = "PROGRAM"
  valorInput = entrada[0]

  numero = 1 
  raiz = nodo('PROGRAM', numero)
  raiz.visitado = True


  while (df.at[valorToken,valorInput]) == (df.at[valorToken,valorInput]):
    data = (df.at[valorToken,valorInput]).split(" ",2)
    data = data.pop()
    data = data.split(" ")
    if data[0] != 'ε':
      ramas=[]
      for i in range(len(data)):
        Token = data.pop()
        ramas.append(Token)
        stack.append(Token)
      ramas.reverse()
      for i in ramas:
        numero = numero + 1
        raiz.insertS(i, numero)
    else:
      numero = numero + 1
      raiz.insertS(data[0],numero)
      raiz.visitarNodo()

    valorToken = stack.pop()
    raiz.visitarNodo()

    while valorToken == valorInput:
      entrada.remove(valorInput)
      if len(entrada) == 0:
        break
      raiz.visitarNodo()

      valorToken = stack.pop()
      valorInput = entrada[0]
    
    print(valorToken," - ",valorInput)
    if len(entrada) == 0: 
      break
    if valorToken.islower():
      break

  raiz.Preorden()
  if sintaxis():
    crear_grafico(raiz)
    return True
  return False


def crear_grafico(raiz): 
  g = graphviz.Digraph('G', filename='grafico.gv')
  nodos = []
  nodos.append(raiz)

  while (len(nodos)):
    curr = nodos[0]
    g.node(str(curr.valor), str(curr.token))
    nodos.pop(0)
    for it in range(len(curr.children)): 
      nodos.insert(0,curr.children[it])
      if curr.children[it].token.islower():
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightcoral')
      else:
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightblue')
      
      g.edge(str(curr.valor),str(curr.children[it].valor))
  g.view()


if __name__=='__main__':
  parsing() 
  
 





