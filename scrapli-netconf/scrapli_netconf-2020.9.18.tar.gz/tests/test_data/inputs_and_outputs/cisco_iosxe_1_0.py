GET_SUBTREE_FILTER = """
<config-format-text-cmd>
 <text-filter-spec> | include interface </text-filter-spec>
</config-format-text-cmd>"""

GET_SUBTREE_ELEMENTS = ["cli-config-data"]

GET_SUBTREE_RESULT = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"><data><cli-config-data><cmd>interface GigabitEthernet1</cmd>
<cmd>interface GigabitEthernet2</cmd>
<cmd>interface GigabitEthernet3</cmd>
<cmd>interface GigabitEthernet4</cmd>
<cmd>interface GigabitEthernet5</cmd>
<cmd>interface GigabitEthernet6</cmd>
<cmd>interface GigabitEthernet7</cmd>
<cmd>interface GigabitEthernet8</cmd>
<cmd>interface GigabitEthernet9</cmd>
<cmd>interface GigabitEthernet10</cmd></cli-config-data></data></rpc-reply>"""

FULL_GET_CONFIG_ELEMENTS = ["cli-config-data-block"]

FULL_GET_CONFIG_RESULT = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"><data><cli-config-data-block>!
TIMESTAMP
!
version 16.12
service timestamps debug datetime msec
service timestamps log datetime msec
! Call-home is enabled by Smart-Licensing.
service call-home
platform qfp utilization monitor load 80
platform punt-keepalive disable-kernel-core
platform console serial
!
hostname csr1000v
!
boot-start-marker
boot-end-marker
!
!
enable secret 9 $9$h6Ayg86tb/EImk$2T6Ns.ke08cAlZ2TbMf3YRCYr7ngDGzgAxZB0YMe7lQ
!
no aaa new-model
call-home
 ! If contact email address in call-home is configured as sch-smart-licensing@cisco.com
 ! the email address configured in Cisco Smart License Portal will be used as contact email address to send SCH notifications.
 contact-email-addr sch-smart-licensing@cisco.com
 profile "CiscoTAC-1"
  active
  destination transport-method http
  no destination transport-method email
!
!
!
!
!
!
!
ip domain name example.com
!
!
!
login on-success log
!
!
!
!
!
!
!
subscriber templating
!
!
!
!
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
crypto pki trustpoint TP-self-signed-434383619
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-434383619
 revocation-check none
 rsakeypair TP-self-signed-434383619
!
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
!
!
crypto pki certificate chain TP-self-signed-434383619
 certificate self-signed 01
  3082032E 30820216 A0030201 02020101 300D0609 2A864886 F70D0101 05050030
  30312E30 2C060355 04031325 494F532D 53656C66 2D536967 6E65642D 43657274
  69666963 6174652D 34333433 38333631 39301E17 0D323030 36323530 32353734
  365A170D 33303031 30313030 30303030 5A303031 2E302C06 03550403 1325494F
  532D5365 6C662D53 69676E65 642D4365 72746966 69636174 652D3433 34333833
  36313930 82012230 0D06092A 864886F7 0D010101 05000382 010F0030 82010A02
  82010100 A623B1F7 12B3D726 1346CBD3 2F44B04D 929F9F10 366559A9 01969EB6
  60E64076 EA398FC2 AE1C5C9F 8D2FD967 F88CBC25 4CDC9A5E 2E6E24CD CAF5631D
  8DC66115 D6F2FB13 43AC4B5D A111D028 6C17CA28 468F642D 8D3CB037 F011BE9C
  12E8D946 9C18A3C3 749314EE 802AAF0C 576D51F3 0FAB8A46 8FB994F6 709B26E6
  BD2895A9 7B79D80F FDFECCB6 73F9E268 081E4E17 B482E52F 598FEA2F A6A60F55
  45C261CC E4BF4189 CA8CF8F1 CA97249C 15C4EBA9 49DB7549 3A9BA63E 05D838E8
  A337E954 BE6A836A BE2D2D9B 98B90EED 03FC0B1F 9E92CE5E 19ABDF73 959E6D01
  A4808C5D F23522E2 A044D2B3 E5027555 2EDACF05 EB1C383D 9E047873 08EEC7EE
  D2CC820F 02030100 01A35330 51300F06 03551D13 0101FF04 05300301 01FF301F
  0603551D 23041830 16801411 CC40D034 E445AA8E E969D900 E7A88813 5FAB9530
  1D060355 1D0E0416 041411CC 40D034E4 45AA8EE9 69D900E7 A888135F AB95300D
  06092A86 4886F70D 01010505 00038201 010027BE BF419A44 482041EA 8B0EBE69
  A8BFDB10 8BD6B831 77EF10EE B066394F 28F094F7 9DC33D17 0C22C05C 6C56C0C7
  2ADAE050 3B0BD408 BF84BB16 1E16020B 24726776 E14BE51C 81B7BA1B A471E812
  A85489B5 5C926888 3E3836E7 A8B201A5 1387D356 E834F172 CE23578E E3FD6E6F
  109E7FC2 6BF7FCAC 72627F7A 65C7C61D 7F94384D CF145B60 7FB8C67C C123A8CD
  73E6FF06 7C07390A E3442056 4CB57401 2C2D30B6 6F5118FC F695513C AEE57478
  7FDC0998 0216826A 86947EC3 B91979D6 2EA653ED 6169C944 AEFCFD45 0A807212
  1B5178AF 67468720 0061FDC0 EE5C3F05 05CF34AF F7D5F003 C4FB81FD 8D513100
  7623BF29 9B2F104F FC775697 FF51A935 B35F
  \tquit
crypto pki certificate chain SLA-TrustPoint
 certificate ca 01
  30820321 30820209 A0030201 02020101 300D0609 2A864886 F70D0101 0B050030
  32310E30 0C060355 040A1305 43697363 6F312030 1E060355 04031317 43697363
  6F204C69 63656E73 696E6720 526F6F74 20434130 1E170D31 33303533 30313934
  3834375A 170D3338 30353330 31393438 34375A30 32310E30 0C060355 040A1305
  43697363 6F312030 1E060355 04031317 43697363 6F204C69 63656E73 696E6720
  526F6F74 20434130 82012230 0D06092A 864886F7 0D010101 05000382 010F0030
  82010A02 82010100 A6BCBD96 131E05F7 145EA72C 2CD686E6 17222EA1 F1EFF64D
  CBB4C798 212AA147 C655D8D7 9471380D 8711441E 1AAF071A 9CAE6388 8A38E520
  1C394D78 462EF239 C659F715 B98C0A59 5BBB5CBD 0CFEBEA3 700A8BF7 D8F256EE
  4AA4E80D DB6FD1C9 60B1FD18 FFC69C96 6FA68957 A2617DE7 104FDC5F EA2956AC
  7390A3EB 2B5436AD C847A2C5 DAB553EB 69A9A535 58E9F3E3 C0BD23CF 58BD7188
  68E69491 20F320E7 948E71D7 AE3BCC84 F10684C7 4BC8E00F 539BA42B 42C68BB7
  C7479096 B4CB2D62 EA2F505D C7B062A4 6811D95B E8250FC4 5D5D5FB8 8F27D191
  C55F0D76 61F9A4CD 3D992327 A8BB03BD 4E6D7069 7CBADF8B DF5F4368 95135E44
  DFC7C6CF 04DD7FD1 02030100 01A34230 40300E06 03551D0F 0101FF04 04030201
  06300F06 03551D13 0101FF04 05300301 01FF301D 0603551D 0E041604 1449DC85
  4B3D31E5 1B3E6A17 606AF333 3D3B4C73 E8300D06 092A8648 86F70D01 010B0500
  03820101 00507F24 D3932A66 86025D9F E838AE5C 6D4DF6B0 49631C78 240DA905
  604EDCDE FF4FED2B 77FC460E CD636FDB DD44681E 3A5673AB 9093D3B1 6C9E3D8B
  D98987BF E40CBD9E 1AECA0C2 2189BB5C 8FA85686 CD98B646 5575B146 8DFC66A8
  467A3DF4 4D565700 6ADF0F0D CF835015 3C04FF7C 21E878AC 11BA9CD2 55A9232C
  7CA7B7E6 C1AF74F6 152E99B7 B1FCF9BB E973DE7F 5BDDEB86 C71E3B49 1765308B
  5FB0DA06 B92AFE7F 494E8A9E 07B85737 F3A58BE1 1A48A229 C37C1E69 39F08678
  80DDCD16 D6BACECA EEBC7CF9 8428787B 35202CDC 60E4616A B623CDBD 230E3AFB
  418616A9 4093E049 4D10AB75 27E86F73 932E35B5 8862FDAE 0275156F 719BB2F0
  D697DF7F 28
  \tquit
!
license udi pid CSR1000V sn 9UMWQBNX1KX
diagnostic bootup level minimal
archive
 log config
  logging enable
 path bootflash:
memory free low-watermark processor 72329
!
!
spanning-tree extend system-id
!
username vrnetlab privilege 15 password 0 VR-netlab9
!
redundancy
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet1
 ip address 10.0.0.15 255.255.255.0
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet2
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet3
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet4
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet5
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet6
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet7
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet8
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet9
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
interface GigabitEthernet10
 no ip address
 shutdown
 negotiation auto
 no mop enabled
 no mop sysid
!
!
virtual-service csr_mgmt
!
ip forward-protocol nd
no ip http server
no ip http secure-server
!
ip ssh pubkey-chain
  username vrnetlab
   key-hash ssh-rsa 5CC74A68B18B026A1709FB09D1F44E2F
ip scp server enable
!
!
!
!
!
!
!
control-plane
!
!
!
!
!
!
line con 0
 stopbits 1
line vty 0 4
 login local
 transport input all
line vty 5 15
 login local
 transport input all
!
netconf ssh
!
!
!
!
!
netconf-yang
end</cli-config-data-block></data></rpc-reply>"""

CONFIG_FILTER_SINGLE = """
<config-format-text-cmd>
    <text-filter-spec>
        interface GigabitEthernet1
    </text-filter-spec>
</config-format-text-cmd> 
"""

CONFIG_FILTER_SINGLE_GET_CONFIG_ELEMENTS = ["cli-config-data"]

CONFIG_FILTER_SINGLE_GET_CONFIG_RESULT = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"><data><cli-config-data><cmd>!</cmd>
<cmd>interface GigabitEthernet1</cmd>
<cmd> ip address 10.0.0.15 255.255.255.0</cmd>
<cmd> negotiation auto</cmd>
<cmd> no mop enabled</cmd>
<cmd> no mop sysid</cmd>
<cmd>end</cmd></cli-config-data></data></rpc-reply>"""

EDIT_CONFIG = """
<config>
<cli-config-data>
<cmd>interface GigabitEthernet2</cmd>
<cmd>description scrapli was here!</cmd>
</cli-config-data>
</config>"""

REMOVE_EDIT_CONFIG = """
<config>
<cli-config-data>
<cmd>interface GigabitEthernet2</cmd>
<cmd>no description</cmd>
</cli-config-data>
</config>"""

EDIT_CONFIG_VALIDATE_FILTER = """
<config-format-text-cmd>
 <text-filter-spec>
   interface GigabitEthernet2
 </text-filter-spec>
</config-format-text-cmd>"""

EDIT_CONFIG_VALIDATE_EXPECTED = """<rpc-reply message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <data>
        <cli-config-data>
            <cmd>!</cmd>
            <cmd>interface GigabitEthernet2</cmd>
            <cmd>description scrapli was here!</cmd>
            <cmd>no ip address</cmd>
            <cmd>shutdown</cmd>
            <cmd>negotiation auto</cmd>
            <cmd>no mop enabled</cmd>
            <cmd>no mop sysid</cmd>
            <cmd>end</cmd></cli-config-data>
    </data>
</rpc-reply>"""

RPC_FILTER = """<get><filter type="subtree"><config-format-text-cmd>
    <text-filter-spec> | include interface </text-filter-spec>
</config-format-text-cmd></filter></get>"""

RPC_ELEMENTS = ["cli-config-data"]

RPC_EXPECTED = """<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"><data><cli-config-data><cmd>interface GigabitEthernet1</cmd>
<cmd>interface GigabitEthernet2</cmd>
<cmd>interface GigabitEthernet3</cmd>
<cmd>interface GigabitEthernet4</cmd>
<cmd>interface GigabitEthernet5</cmd>
<cmd>interface GigabitEthernet6</cmd>
<cmd>interface GigabitEthernet7</cmd>
<cmd>interface GigabitEthernet8</cmd>
<cmd>interface GigabitEthernet9</cmd>
<cmd>interface GigabitEthernet10</cmd></cli-config-data></data></rpc-reply>"""
