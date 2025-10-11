Docker Networks -> Communiquer, Information
 
Insolation: 1 - 1
Type de reseaux: bridge, host, overlay

Bridge: Personalise

docker network create my_network

Host(  bridge(container(gateway))  ) <- api -request

Host: (3000, XXXX - > 5000)

None:

Overlay: Kubernetes(plusieurs hotes)

1  - (1000 docker comtainer)
2  - (1000 docker comtainer)
3  - (1000 docker comtainer)

Macvlan: -Address MAc Container.. 


docker network create --driver bridge --subnet 178.28.10.0/24 --gateway 178.20.10.1 my-custom-net

00000000 00000000 00000000 00000000

Range - (178.28.10.1 - 178.28.10.255)

1 Nerwork - 2^8 (256 - 3 ) = 253 (178.28.10.0, 178.20.10.1, 178.20.10.255) 
1 Nertwork - 2^16 ()
