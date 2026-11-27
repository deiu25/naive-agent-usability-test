# Testul "angajat nou" pe {aplicatia}

{Data}. Un agent fara nicio informatie despre aplicatie a primit un bilet "de la sef" si a facut treaba unui
{rolul}, doar cu ecranul, mouse-ul si tastatura.

## Pe scurt

- **Sarcina:** {ce era de facut, in cuvintele biletului}.
- **Rulari:** {cate, cu cati agenti, cat a durat fiecare, cate gesturi din transcript}. {Care e valabila
  cap-coada si de ce.}
- **Ce a mers:** {pasii scurti, in cuvinte simple}.
- **Ce lipseste:** {unde se pierde omul, intr-o propozitie}.

Testul a rulat pe o copie izolata a aplicatiei, cu datele din {sursa, data}. {Productia a fost doar citita.}

Folosirea, pe scurt ({fisierul pasului 1}): {doua-trei randuri: cine foloseste fluxul, cat de des, ce
asteapta dupa el; de ce tinteste testul aici}.

## Cat a costat fiecare pas

| Pas | Gesturi | Pe ce s-au dus |
|---|---|---|
| {pasul} | {n, din transcript} | {cautare, ajutor citit, refaceri, verificari} |

Gesturile sunt numarate din transcript ({unealta}). Numaratoarea agentului: {n}. {De ce difera, daca difera.}

## Unde se pierde un om nou

In ordinea drumului. "Ambele" = s-a intamplat in ambele rulari.

### {N}. {Titlul, in cuvintele omului} ({ambele / rularea X})

{Ce s-a intamplat, cu captura.} {Eticheta: confirmat (fisier:linie sau interogarea) / perceptie: agentul a
crezut..., aplicatia face... / neverificat: ce ar lamuri.}

Ar ajuta: {cea mai mica schimbare}.

## Afirmatiile agentului, verificate

| Afirmatia | Eticheta | Dovada |
|---|---|---|
| {afirmatia} | {confirmat / artefact al uneltei / perceptie / neverificat} | {fisier:linie, interogarea, limita uneltei} |

## Ce a mers bine

- {pasul care a mers din prima}

## Ce a scris agentul in baza

{Doar inregistrarile de pe bilet / ce altceva a atins si de ce a fost usor.} {Niciun mesaj trimis.}

## Ce nu spune testul

- **Agentul nu e om.** Citeste tot ecranul si are rabdare. Unde s-a blocat el, se blocheaza si un om. Unde a
  trecut el, un om se poate inca pierde.
- **Un singur scenariu:** {ce n-a fost incercat}.
- **Viteza nu se poate judeca** pe copia de test.
- **De ce oamenii ocolesc fluxul** nu se vede in acest test.

## Retest (dupa reparatii)

| Pas | Reper | {Retest 1} | {Retest 2} | Tinta |
|---|---|---|---|---|
| {pasul} | {n} | {n} | {n} | {n} |
| Ajutor citit inainte de primul gest | {n} | {n} | {n} | |
| Total (din transcript) | {n} | {n} | {n} | {n} |

- {Pasii care au coborat si reparatia care explica fiecare.}
- {Pasii care au urcat sau au ramas peste tinta: de ce.}
- {Diferenta dintre cele doua rulari: cat variaza un agent.}
- Masura reala: interogarile din {fisierul pasului 1}, la {data, cateva saptamani dupa ultima urcare}.
