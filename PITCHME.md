---?color=linear-gradient(110deg, #835196 50%, #F5F6F5 50%)

@title[Introductie]

<!--
Tip! Get started with this template as follows:
Step 1. Delete the contents of this PITCHME.md file.
Step 2. Start adding your own custom slide content.
Step 3. Copy slide markdown snippets from template/md directory as needed.
-->

@snap[west text-bold]
### Agentschap Onroerend Erfgoed
Vlaanderen is erfgoed
@snapend

@snap[south-west byline text-04 text-dark]
Presentatie Leersessie development pipeline & deployment tussen OVAM VMM VLM aOE dOMG
@snapend

---
@title[Voorbeeld applicatie Dossierdata]

@snap[north span 40]
### Deploy applicatie dossierdata
@snapend

@snap[midpoint span-40]
![GATEWAY](template/img/screenshot-dev-dossiers.png)
@snapend

@snap[south-west span-30 text-06 fragment]
@box[rounded text-white box-overzicht](Stap 1.#Lege server via dOMG.)
@snapend

@snap[south span-30 text-06 fragment]
@box[rounded text-white box-overzicht](Stap 2.#Voorbereidingen via Ansible.)
@snapend

@snap[south-east span-30 text-06 fragment]
@box[rounded text-white box-overzicht](Stap 3.#Deploy door Fabric.)
@snapend

---?include=template/md/oe-ansible/PITCHME.md
