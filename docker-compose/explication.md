fronted 
backend
db 
redis 

# communication via network

  frontend:
    networks:
      - front-tier
      - back-tier
    
  backend:
    networks:
      - back-tier
      
  db:
    networks:
      - back-tier

docker network create front-tier
docker network create back-tier


install nginx vps 
default.conf
etc/nginx/default.conf
etc/nginx/conf.d/
  -django.conf
  -appsandbox.conf 
