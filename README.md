# Tema 1 ASC
## 334CC Iliescu Lucian-Marius

### Implementare marketplace:  
  - pentru a implementa bufferele fiecarui producator am folosit o lista de cozi  
  - pentru ca fiecare producator sa stie ce coada trebuie sa acceseze, el se va  
  folosi de id-ul lui, unde generarea id-ului se va face la  
  instantierea producatorului  
  - id-ul generat e reprezentat de un numar, care pleaca de la 0 si se  
  incrementeaza la fiecare apel de generare al unui id
  - am folosit acest tip de generare deoarece facea o asociere imediata intre  
  producator si bufferul acestuie
  - se putea folosi un dictionar in loc de lista de liste unde cheia sa id-ul  
  si valoarea sa fie bufferul, dar abordarea curent mi se pare mai eficienta  
  deoarece as avea inserare in O(1) mereu, spre deosebire de un dictionar  
  unde am tot O(1) la inserare in majoritatea timpului, dar pot avea coliziuni  
  si inserarea sa necesite mai mult timp
  - de asemenea, am folosit o coada pentru fiecare producator deoarece  
  ele imi asigura sincronizare, fara sa mai trebuiasca sa folosesc lock-uri
  - un mecanism similar am folosit si pentru generarea id-urilor cosurilor
  - am folosit un lock, numit mutex, ca sa previn conditiile de cursa  
  pe variabilele de id

### Implementare producer:
  - pe langa membrii dati in schelet am folosit un string, care reprezinta  
    id-ul producatorului, acest id generandu-se la instantierea producatorului   
  - metoda run se bazeaza pe o bucla infinita in care:  
      - parcurg fiecare produs din lista de tupluri products a producatorului  
      - extrag cantitatea si timpul de producere din tuplu  
      - dau publish de cate ori imi zice cantitatea si daca returneaza False  
        mai incerc o data pana imi iese, fara sa avansez in iteratie  

### Implementare consumer:
  - metoda run este alcatuita din urmatoarele etape:  
      - parcurg fiecare cart din lista de carturi  
      - creez un id nou pentru cartul respectiv  
      - pentru fiecare comanda din cart extrag tipul comenzii, produsl, cantitatea  
      - daca tipul comenzii e add, apelez add_to_cart, ca sa adaug cantitatea  
        de produse in cos si daca returneaza False incerc pana se poate adagua  
      - daca tipul comenzii e move, apelez remove_from_cart si procedez similar  
        pasului anterior  
      - dupa ce am parcurs toate comenzile, apelez place place_order din  
        marketplace ca sa obtin produsele aflate in cart  
      - parcurg lista de produse si afisez numele consumatorlui  
        si ce a produs a cumparat  
