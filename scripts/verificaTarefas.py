mapa = {}
for line in lines[1:]:
     dados = line.split(",")
     cont = 0
     if mapa.has_key(dados[1].strip()):
             cont = mapa[dados[1].strip()]
     cont2 = 0
     if mapa.has_key(dados[2].strip()):
             cont2 = mapa[dados[2].strip()]
     cont = cont + 1
     cont2 = cont2 + 1
     mapa[dados[1].strip()] = cont
     mapa[dados[2].strip()] = cont2
