# Anomalies des sources

Les bonnes réponses imprimées ne sont pas une preuve suffisante lorsque l’énoncé ou son explication est ambigu. Les 15 questions PDF du tableau ci-dessous sont consultables dans leur module, mais exclues des scores. Les six questions HTML signalées plus bas sont incluses dans les scores à la demande de l’utilisateur. Les réponses originales sont conservées, jamais remplacées sans le signaler.

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

### Ajout depuis le dossier `mi` — 13 octobre 2026

La page `mi/CCNA 200-301 Questions.html` fournit 192 questions. 46 correspondent aux questionnaires PDF déjà intégrés ; les 146 autres alimentent 19 modules auparavant vides. Les 134 fiches existantes sont conservées intégralement. Les PDF du dossier `mi` sont identiques aux documents correspondants dans `sources/`.

L’original HTML est conservé dans `sources/`. `CCNA 200-301 Questions - HTML archive.pdf` est une archive générée depuis cet HTML pour conserver les liens documentaires PDF du moteur existant ; ce n’est pas un PDF original fourni par l’utilisateur. Le champ `origin` des nouvelles fiches référence l’HTML original et son empreinte SHA-256. Les schémas et tableaux ont été capturés depuis le contenu HTML fourni, sans changer les équipements, connexions ou libellés. Le manifeste conserve leur correspondance exacte avec les images intégrées à l’archive.

À la demande explicite de l’utilisateur, les six questions ci-dessous sont incluses dans les entraînements, examens et scores avec les réponses exactes du HTML fourni. Les réserves suivantes sont conservées uniquement comme notes documentaires ; les énoncés, choix, clés, explications et schémas ne sont pas corrigés ni remplacés.

| ID | Module / question HTML | Problème |
|---|---|---|
| ccna-07-mi-q002 | VLAN & Trunking Questions 2 / Q2 | Dynamic Auto et Dynamic Desirable fonctionnent avec le voisin décrit ; l’explication reconnaît deux choix possibles. |
| ccna-11-mi-q003 | IP Address & Subnetting Questions / Q3 | Un /27 ne fournit que 30 adresses utilisables, pas 40 ; les adresses SVI proposées sont des adresses réseau. |
| ccna-08-mi-q011 | STP & VTP Questions / Q11 | La priorité 0 ne garantit pas de rester Root Bridge si un autre switch a la même priorité et une adresse MAC inférieure. |
| ccna-08-mi-q013 | STP & VTP Questions / Q13 | Même réserve sur la garantie absolue d’élection avec une priorité 0. |
| ccna-34-mi-q001 | Drag Drop Questions / Q1 | Le réseau 192.168.1.0/26 affiché ne correspond pas au sous-réseau 192.168.1.192/26 de l’hôte et de la passerelle. |
| ccna-40-mi-q006 | Miscellaneous Questions / Q6 | L’explication indique 12:00:00 pour minuit ; la commande choisie est valide mais l’heure correcte serait 00:00:00. |

Références de contrôle : [configuration des Trunks — Cisco](https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst_microswitches/software/releases/15_2_7_e/configuration_guide/vlan/b_1527e_vlan_cms_cg/configuring_vlan_trunks.html), [élection STP — Cisco](https://www.cisco.com/c/en/us/td/docs/switches/lan/c9000/lyr2-fwd/stp/stp-configuration-guide/m-stp.html), [nombre d’hôtes par sous-réseau — Cisco](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13790-8.html).

La banque contient désormais 280 fiches, dont 265 utilisables dans les scores, et 36 modules disponibles. NAT, HSRP, Security Questions et IPv6 restent vides : aucun questionnaire correspondant n’est présent dans les fichiers fournis.

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
