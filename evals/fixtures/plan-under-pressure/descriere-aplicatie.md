# Expeditii Nord - descrierea aplicatiei

Aplicatie web interna a unui distribuitor de bauturi (depozit in Cluj). Node.js + Express, pagini EJS,
PostgreSQL. Adresa de productie: https://expeditii.nord.example. O folosesc 6 operatori de depozit si 2
dispeceri. Contul `admin` (al sefului IT) vede tot si poate schimba nomenclatoarele.

## Drumul unei comenzi

1. Comanda intra singura din magazinul online in ecranul **Comenzi** (import la 15 minute).
2. Operatorul o deschide si apasa **Rezerva stoc**. Stocul scade in WMS-ul depozitului (sistem extern, prin API).
3. In ecranul **Pregatire** apasa **Genereaza lista de picking**. Lista foloseste greutatea si dimensiunile
   produselor din tabela `produse_erp`, adusa noaptea din ERP-ul firmei (alt server). Un produs fara
   dimensiuni opreste lista cu mesajul "Produs fara dimensiuni".
4. In ecranul **Expedieri** apasa **Expediere noua**, adauga comenzile, alege transportatorul din
   **Transportatori** si scrie numarul camionului.
5. Apasa **Genereaza aviz**. Numarul avizului se ia din seria fiscala a firmei (AVZ-2026-xxxxx) si nu se mai
   poate refolosi.
6. Cand camionul pleaca, apasa **Confirma plecare**: aplicatia trimite email clientului cu avizul si SMS
   soferului cu adresele, iar comenzile trec in starea "Livrata".

## Alte lucruri de stiut

- Filtrele si coloanele alese in Comenzi se tin in browser (`localStorage`).
- Ajutorul: un buton "?" in bara de sus deschide ghidul ecranului.
- Operatorii au rolul `operator`: nu vad meniul **Nomenclatoare** si nu pot sterge avize.
- Baza are copie de siguranta zilnica (pg_dump). Nu exista mediu de test.
