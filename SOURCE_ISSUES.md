# Anomalies des sources

Les bonnes réponses imprimées ne sont pas une preuve suffisante lorsque l’énoncé ou son explication est ambigu. Les 15 questions suivantes sont consultables dans leur module, mais exclues des scores. Les réponses originales sont conservées, jamais remplacées sans le signaler.

| ID | Source / question / page | Problème |
|---|---|---|
| ccna-21-q007 | CCNA Training » Access-list Quiz.pdf / Q7 / p.5 | La source reconnaît que C peut aussi être correcte alors que deux réponses sont demandées. |
| ccna-39-q007 | CCNA Training » Automation Quiz.pdf / Q7 / p.4 | REST ne limite pas ses représentations à XML et JSON ; l’explication concerne Cisco APIC. |
| ccna-39-q009 | CCNA Training » Automation Quiz.pdf / Q9 / p.5 | Les propositions décrivent REST plutôt qu’une API en général. |
| ccna-27-q003 | CCNA Training » DNS Quiz.pdf / Q3 / p.2 | L’activation de la résolution et la définition d’un serveur DNS interviennent ; l’énoncé est ambigu. |
| ccna-36-q008 | CCNA Training » Drag Drop Quiz 3.pdf / Q8 / p.9 | La base recense les baux DHCP appris, pas les hôtes inconnus ; trusted caractérise avant tout une interface. |
| ccna-09-q005 | CCNA Training » EtherChannel Quiz.pdf / Q5 / p.3 | La source évoque trois réponses pour deux demandées ; STP peut bloquer un EtherChannel logique. |
| ccna-18-q002 | CCNA Training » NTP Quiz.pdf / Q2 / p.1 | La source marque l’authentification obligatoire, puis indique qu’elle ne l’est pas toujours. |
| ccna-15-q007 | CCNA Training » OSPF Quiz 2.pdf / Q7 / p.4 | L’explication affirme à tort qu’OSPF négocie le type de réseau et les temporisateurs. Ceux-ci doivent correspondre. |
| ccna-15-q008 | CCNA Training » OSPF Quiz 2.pdf / Q8 / p.4 | La réponse marquée ne garantit pas le voisinage sans adjacence et contredit les conditions expliquées. |
| ccna-06-q002 | CCNA Training » Trunking Quiz.pdf / Q2 / p.2 | Le mode de SW2 n’est pas précisé ; la source suppose Dynamic Auto. |
| ccna-30-q004 | CCNA Training » Wireless Quiz.pdf / Q4 / p.2 | Le nombre de 23 canaux dépend du domaine réglementaire et de leur disponibilité, non précisés. |
| ccna-29-q003 | CCNA Training » Port Security Quiz.pdf / Q3 / p.2 | restrict et shutdown peuvent tous deux incrémenter le compteur et générer un trap SNMP. L’énoncé n’exige pas que le port reste actif. |
| ccna-38-q001 | CCNA Training » DHCP Quiz.pdf / Q1 / p.1 | La source indique explicitement qu’une seule fonctionnalité devrait être demandée. |
| ccna-38-q009 | CCNA Training » DHCP Quiz.pdf / Q9 / p.5 | show ip interface et show interface peuvent tous deux indiquer l’utilisation de DHCP. |
| ccna-35-q009 | CCNA Training » Drag Drop Quiz 2.pdf / Q9 / p.6 | 802.1x n’est pas la protection directe contre la saturation MAC ; DHCP snooping seul ne bloque pas l’usurpation ARP. |

## Autres observations

- Drag Drop Quiz 2 (1).pdf est identique bit pour bit à Drag Drop Quiz 2.pdf (SHA-256 c141ed44994b447a9c26410957febf58d827798e1614ca18737dcbdc563431d9). Une seule banque de dix questions est créée.
- Port Security, SDN, DHCP et Drag Drop Quiz 2 sont des documents scannés. L’OCR intégral est archivé, mais les choix et clés ont été lus visuellement. Les caractères OCR erronés (par exemple « dhep » pour « dhcp ») ne sont pas repris comme commandes lorsqu’ils ne figurent pas réellement dans l’image source.
- L’option A d’Access-list Q1 imprime « onfig t » ; l’option A de Security 2 Q4 imprime « 1(config) » ; ces défauts source sont conservés dans les originaux. Les guillemets typographiques des exemples JSON sont également conservés. Ces exemples ne doivent pas être utilisés comme du code copié-collé valide sans contrôle de la source.
- Les explications et commentaires peuvent contenir des coquilles, des simplifications ou des références URL coupées par la mise en page. La transcription anglaise conserve ces éléments ; une reformulation française n’est pas une correction technique du contenu source.
- Les titres des modules fournis par l’utilisateur sont conservés, notamment DNA Center ; aucun renommage lié à l’évolution des produits n’a été imposé.

## Sources techniques de contrôle

Les ambiguïtés OSPF et de sécurité ont été comparées notamment avec les documents officiels suivants :

- [États des voisins OSPF — Cisco](https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13685-13.html)
- [Configuration des fonctions de sécurité de couche 2 — Cisco](https://www.cisco.com/c/en/us/support/docs/switches/catalyst-3750-series-switches/72846-layer2-secftrs-catl3fixed.html)
- [Vérification DAI et IP Source Guard — Cisco](https://www.cisco.com/c/en/us/support/docs/switches/lan-switch-software/222274-troubleshoot-dynamic-arp-inspection-dai.html)

L’absence d’une anomalie dans cette liste ne constitue pas une certification par Cisco ou une relecture par un instructeur externe.
