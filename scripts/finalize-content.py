from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1];qs=json.loads((root/'data/questions.json').read_text());by={q['id']:q for q in qs}
q=by['ccna-35-q009']
q['explanation']['en']='''VLAN Hopping: By altering the VLAN ID on packets encapsulated for trunking, an attacking device can send or receive packets on various VLANs, bypassing Layer 3 security measures. VLAN hopping can be accomplished by switch spoofing or double tagging.
a. Switch spoofing:
The attacker can connect an unauthorized Cisco switch to a Company switch port. The unauthorized switch can send DTP frames and form a trunk with the Company Switch. If the attacker can establish a trunk link to the Company switch, it receives traffic to all VLANs through the trunk because all VLANs are allowed on a trunk by default.
(Instead of using a Cisco Switch, the attacker can use a software to create and send DTP frames).
To mitigate this type of attack, we can disable DTP.
b. Double-Tagging attack:
In this attack, the attacking computer generates frames with two 802.1Q tags. The first tag matches the native VLAN of the trunk port (VLAN 10 in this case), and the second matches the VLAN of a host it wants to attack (VLAN 20).
When the packet from the attacker reaches Switch A, Switch answer " only sees the first VLAN 10 and it matches with its native VLAN 10 so this VLAN tag is removed. Switch answer " forwards the frame out all links with the same native VLAN 10. Switch answer " receives the frame with an tag of VLAN 20 so it removes this tag and forwards out to the Victim computer.
Note: This attack only works if the trunk (between two switches) has the same native VLAN as the attacker.
To mitigate this type of attack, we can use VLAN access control lists (VACLs, which applies to all traffic within a VLAN. We can use VACL to drop attacker traffic to specific victims/servers) or implement Private VLANs.
Answer:
+ 802.1q double-tagging VLAN-hopping attack: configure the native VLAN with a nondefault VLAN ID
+ MAC flooding attack: configure 802.1x authenticate
+ man-in-the-middle spoofing attack: configure DHCP snooping
+ switch-spoofing VLAN-hopping attack: disable DTP'''
q['explanation'].pop('fr',None);q['translationStatus']='partial';q['translationReview']['explanationChecked']=False
# Keep all original source extracts in the repository, including image-only documents.
(root/'sources/extracted').mkdir(exist_ok=True)
for p in (root/'tmp/extracted').glob('*.txt'):
 if p.name.startswith('CCNA Training') or p.name.startswith('ocr-CCNA Training'):
  (root/'sources/extracted'/p.name).write_text(p.read_text())
# Mark every extracted topology as original content and avoid declaring expert certification.
for q in qs:
 q['translationReview']['expertCertification']=False
 if q.get('images'):q['topologyStatus']='original-source-pixels'
(root/'data/questions.json').write_text(json.dumps(qs,ensure_ascii=False,indent=2))
