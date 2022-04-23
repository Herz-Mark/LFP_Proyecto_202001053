from graphviz import Digraph
import uuid

g = Digraph('Ejemplo', filename='png')

def crearNodo(etiqueta: str) -> str:
    id = str(uuid.uuid1())
    g.node(id,etiqueta)
    return id

def agregarHijo(id_padre,id_hijo :str):
    g.edge(id_padre,id_hijo)

n1 = crearNodo('Batman')
n2 = crearNodo('Robin')

agregarHijo(n1,n2)

g.view()