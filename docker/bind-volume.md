bind mounts et volumes 

images docker ---> logs.txt
conteneur ----> les logs sont sauvegarder dans le fichier logs.txt

quand le conteneur tombe alors vous perdez le fichier logs.txt


on va creer une image de ce fichier dans le host ou la machine (bind) 

quand tu veux utilse le bind ( pour dev, tu dois entre le chemin absolu)

si je veux un fichier qui peux etre l'exterieur de host alors je vais use un  volume(productioin) s3, 


docker volume create nom-du-volume 
docker volume ls 
docker volume rm nom-du-volume 

docker run -it --rm -v test:/data alpine sh (volume)
docker run -it --rm -v $(pwd)/test:/data alpine sh (bind mount)
