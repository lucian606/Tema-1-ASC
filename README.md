# Tema 1 ASC
## 334CC Iliescu Lucian-Marius

### Implementare marketplace:  
  - am folosit urmatorii membri pentru a ma ajuta la implementare:  
      - queue_size_per_producer: dimensiunea cozii fiecarui producator  
      - producer_id: id-ul producatorului care va apela register_producer  
      - cart_id: id-ul cartului care va fi generat cu new_cart  
      - queues: lista care contine cozile producatorilor  
      - mutex: Lock care va preveni race conditions
      - products_dict: dictionar in care retine producatorul fiecarui produs  
  - register_producer:  
      - dau lock la mutex sa previn race condition pe producer_id  
      - variabila producer_id este un int care reprezinta indexul cozii pe care  
        producatorul o va avea in lista de cozii  
      - la fiecare apel producer_id se incrementeaza  
      - dau unlock la mutex  
      - returnez valoarea acesteia  
  - publish:  
      - iau indexul cozii din id-ul producatorului  
      - verific daca coada e plina  
      - adaug produsul in coada producatorului  
      - pun produsul in dictionarul de produce impreuna cu indexu producatorului  
      - folosesc products_dict ca atunci cand se scoate un produs din cart  
        sa stiu de unde l-am luat  
  - new_cart:  
      - dau lock la mutex sa preivn race condition pe cart id  
      - variabila cart_id este un int care va retine indexul listei care  
        reprezinta cartul din lista carts  
      - la fiecare apel incrementez cart_id  
      - dau unlock la mutex  
      - returnez id-ul generat  
  - add_to_cart:  
      - parcurg toate cozile producatorilor  
      - daca gasesc produsul il bag in cartul respectiv  
      - daca nu il gasesc returnez False  
  - remove_from_cart:  
      - verific daca produsul e in cart, daca nu returnez False  
      - iau indexul_producatorului corespondent produsului scos ca sa stiu unde  
        trebuie sa il pun  
      - scot produsul din lista cartului  
      - adaug produsul in coada producatorului care l-a produs  
  - place_order:
      - iau lista cartului cu cart_id  
      - golesc lista din carts  
      - returnez produsele care erau in cart  

### Implementare producer:
  - pe langa membrii dati in schelet am folosit un string, care reprezinta  
    id-ul producatorului  
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
