from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];qs=json.loads((root/'data/questions.json').read_text());by={q['id']:q for q in qs}
def setexp(id,en,fr):
 q=by[id];q['explanation']={'en':en,'fr':fr};q['translationStatus']='validated';q['translationReview']['explanationChecked']=True
setexp('ccna-32-q003', '''Control Plane Function
In its simplest form, the control plane provides layer-2 MAC reachability and layer-3 routing information to network devices that require this information to make packet forwarding decisions. In the case of firewalls, the control plane would include stateful flow information for inspection. Control plane functionality can implemented as follows:
+ Distributed — Conventional routers and switches operate using distributed protocols for control, i.e. where each device makes its own decisions about what to do, and communicate relevant information to other devices for input into their decision making process. For example, the Spanning Tree Protocol (STP), Fabric Path, and routing protocols such as IS-IS and BGP provide distributed control of packet forwarding functionality to networking devices.
+ Centralized — In this case, a centralized controller provides the necessary information for a network element to make a decision. For example, these controller(s) instruct networking devices on where to forward packets by explicitly programming their MAC and FIBs.
Reference: https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Data_Center/VMDC/SDN/SDN.html''', '''Fonction du plan de contrôle
Dans sa forme la plus simple, le plan de contrôle fournit les informations de joignabilité MAC de couche 2 et de routage de couche 3 dont les équipements ont besoin pour décider de l’acheminement des paquets. Pour les pare-feu, il inclut les informations d’état des flux à inspecter. Il peut être implémenté ainsi :
+ Distribué : les routeurs et commutateurs conventionnels utilisent des protocoles distribués. Chaque équipement prend ses propres décisions et communique les informations utiles aux autres. STP, Fabric Path et des protocoles tels qu’IS-IS et BGP assurent par exemple un contrôle distribué de l’acheminement.
+ Centralisé : un contrôleur central fournit les informations nécessaires aux décisions d’un élément réseau. Ces contrôleurs indiquent où envoyer les paquets en programmant explicitement les tables MAC et FIB.
Référence : https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Data_Center/VMDC/SDN/SDN.html''')
setexp('ccna-32-q004', '''Most traditional devices use a distributed architecture, in which each control plane is resided in a networking device. Therefore they need to communicate with each other via messages to work correctly.
In contrast to distributed architecture, centralized (or controller-based) architectures centralizes the control of networking devices into one device, called SDN controller -> Answer 'Only controller-based networks decouple the control plane and the data plane' is correct.''', '''La plupart des équipements traditionnels utilisent une architecture distribuée : chaque plan de contrôle réside dans un équipement réseau. Ils doivent donc échanger des messages pour fonctionner correctement.
À l’inverse, l’architecture centralisée, ou pilotée par contrôleur, centralise le contrôle dans un équipement appelé contrôleur SDN. La proposition « seuls les réseaux pilotés par contrôleur séparent les plans de contrôle et de données » est donc correcte.''')
setexp('ccna-32-q006', '''OpenFlow is a well-known southbound API. OpenFlow defines the way the SDN Controller should interact with the forwarding plane to make adjustments to the network, so it can better adapt to changing business requirements.
The Network Configuration Protocol (NetConf) uses Extensible Markup Language (XML) to install, manipulate and delete configuration to network devices.
Other southbound APIs are:
+ onePK: a Cisco proprietary SBI to inspect or modify the network element configuration without hardware upgrades.
+ OpFlex: an open-standard, distributed control system. It send “summary policy” to network elements.''', '''OpenFlow est une API southbound connue. Elle définit comment le contrôleur SDN interagit avec le plan d’acheminement pour ajuster le réseau aux besoins métier changeants.
Network Configuration Protocol (NetConf) utilise XML pour installer, modifier et supprimer la configuration des équipements.
Autres API southbound :
+ onePK : une SBI propriétaire Cisco qui examine ou modifie la configuration sans mise à niveau matérielle.
+ OpFlex : un système de contrôle distribué ouvert standard qui envoie une politique résumée aux éléments réseau.''')
setexp('ccna-38-q002', '''If the DHCP Server is not on the same subnet with the DHCP Client, we need to configure the router on the DHCP client side to act as a DHCP Relay Agent so that it can forward DHCP messages between the DHCP Client & DHCP Server. To make a router a DHCP Relay Agent, simply put the “ip helper-address <IP-address-of-DHCP-Server>” command under the interface that receives the DHCP messages from the DHCP Client.
As we know, router does not forward broadcast packets (it drops them instead) so DHCP messages like DHCPDISCOVER message will be dropped. But with the “ip helper-address ...” command, the router will accept that broadcast message and cover it into a unicast packet and forward it to the DHCP Server. The destination IP address of the unicast packet is taken from the “ip helper-address ...” command.''', '''Si le serveur DHCP n’est pas dans le même sous-réseau que le client, le routeur du côté client doit agir comme agent relais pour transmettre les messages entre le client et le serveur. Configurez « ip helper-address <IP-address-of-DHCP-Server> » sur l’interface qui reçoit les messages du client.
Un routeur ne transmet pas les broadcasts : des messages tels que DHCPDISCOVER seraient donc supprimés. Avec « ip helper-address ... », il accepte le broadcast, le convertit en unicast et l’envoie au serveur DHCP. L’adresse IP destination provient de la commande « ip helper-address ... ».''')
setexp('ccna-38-q003', '''To configure DHCP snooping feature, at least three steps must be done:
1. Configure global DHCP snooping
Switch(config)# ip dhcp snooping
2. Configure trusted ports (as least on 1 port). By default, all ports are untrusted
Switch(config-if)# ip dhcp snooping trust
3. Configure DHCP snooping for the selected VLANs
Switch(config)# ip dhcp snooping vlan {VLAN-ID | VLAN range}
Note: To configure DHCP snooping with Dynamic ARP Inspection we need to add the command “ip arp inspection vlan vlan-id” in global configuration mode and “ip arp inspection trust” in interface mode.
In a normal network environment, we should trust interfaces that are connected to routers, not end points.''', '''DHCP snooping nécessite au moins trois étapes :
1. Activer DHCP snooping globalement :
Switch(config)# ip dhcp snooping
2. Définir au moins un port de confiance. Par défaut, tous les ports sont untrusted :
Switch(config-if)# ip dhcp snooping trust
3. Activer DHCP snooping pour les VLAN choisies :
Switch(config)# ip dhcp snooping vlan {VLAN-ID | VLAN range}
Pour l’associer à Dynamic ARP Inspection, ajoutez « ip arp inspection vlan vlan-id » en configuration globale et « ip arp inspection trust » en mode interface.
Dans un réseau normal, on fait confiance aux interfaces connectées à des routeurs, et non aux terminaux.''')
setexp('ccna-38-q001', '''The following example shows how to configure a DHCP Server on a Cisco router:
Router(config)#ip dhcp pool CLIENTS
Create a DHCP Pool named CLIENTS
Router(dhcp-config)#network 10.1.1.0 /24
Specifies the subnet and mask of the DHCP address pool
Router(dhcp-config)#default-router 10.1.1.1
Set the default gateway of the DHCP Clients
Router(dhcp-config)#dns-server 10.1.1.1
Configure a Domain Name Server (DNS)
Router(dhcp-config)#domain-name 9tut.com
Configure a domain-name
Router(dhcp-config)#lease 0 12
Duration of the lease (the time during which a client computer can use an assigned IP address). The syntax is “lease {days[hours] [minutes] | infinite}”. In this case the lease is 12 hours. The default is a one-day lease. Before the lease expires, the client typically needs to renew its address lease assignment with the server.
Router(dhcp-config)#exit
Router(config)# ip dhcp excluded-address 10.1.1.1 10.1.1.10
The IP range that a DHCP Server should not assign to DHCP Clients. Notice this command is configured under global configuration mode.
Manual bindings are IP addresses that have been manually mapped to the MAC addresses of hosts that are found in the DHCP database.
All DHCP clients send a client identifier (DHCP option 61) in the DHCP packet. To configure manual bindings, you must enter the client-identifier DHCP pool configuration command with the appropriate hexadecimal values identifying the DHCP client. For example:
ip dhcp pool SERVER
host 172.16.200.100 255.255.255.0
client-identifier 01aa.bbcc.0003.00
default-router 172.16.200.1
!
Therefore two requirements for DHCP binding is the IP address and the hardware address (MAC address) of the client. Notice that in the above example “aabb.cc00.0300” is the MAC address of the client while prefix “01” represents the Ethernet media type.
Note: In fact, this question should ask “When implementing a router as a DHCP server, which one of these features must be configured?”. Because we only need to configure either an “address pool” or “manual binding”.''', '''Voici un exemple de configuration d’un serveur DHCP sur un routeur Cisco :
Router(config)#ip dhcp pool CLIENTS
Crée un pool DHCP nommé CLIENTS.
Router(dhcp-config)#network 10.1.1.0 /24
Précise le sous-réseau et le masque du pool.
Router(dhcp-config)#default-router 10.1.1.1
Définit la passerelle par défaut des clients.
Router(dhcp-config)#dns-server 10.1.1.1
Configure un serveur DNS.
Router(dhcp-config)#domain-name 9tut.com
Configure le nom de domaine.
Router(dhcp-config)#lease 0 12
Définit la durée pendant laquelle un client peut utiliser son adresse. Syntaxe : « lease {days[hours] [minutes] | infinite} ». Ici, le bail dure 12 heures. Par défaut, il dure un jour. Avant expiration, le client doit généralement renouveler son bail auprès du serveur.
Router(dhcp-config)#exit
Router(config)# ip dhcp excluded-address 10.1.1.1 10.1.1.10
Définit les adresses que le serveur ne doit pas attribuer. Cette commande est en mode de configuration globale.
Les associations manuelles relient manuellement des adresses IP aux adresses MAC d’hôtes présents dans la base DHCP.
Tous les clients envoient un identifiant client (option DHCP 61). Pour une association manuelle, client-identifier doit préciser les valeurs hexadécimales identifiant le client. Exemple :
ip dhcp pool SERVER
host 172.16.200.100 255.255.255.0
client-identifier 01aa.bbcc.0003.00
default-router 172.16.200.1
!
Les deux informations nécessaires sont l’adresse IP et l’adresse matérielle (MAC) du client. Ici, « aabb.cc00.0300 » est la MAC Address et le préfixe « 01 » indique Ethernet.
Remarque : la source indique que la question devrait demander une seule fonctionnalité : il suffit de configurer soit un pool d’adresses, soit une association manuelle.''')
q=by['ccna-29-q003'];q['verified']=False;q['issue']={'en':'Both restrict and shutdown can increment the violation counter and generate an SNMP trap. The question does not require the port to remain up.','fr':'restrict et shutdown peuvent tous deux incrémenter le compteur et générer un trap SNMP. L’énoncé n’exige pas que le port reste actif.'}
(root/'data/questions.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2))
