# INSTALLATION DES DEPENDENCES

## Installer docker

```sh 
sudo apt update && sudo apt upgrade -y
sudo apt install ca-certificates curl gnupg -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io -y
sudo usermod -aG docker $USER
```

## Installer Jenkins 

### documentation jenkins 
https://www.jenkins.io/doc/book/installing/linux/ 

### Obtenir ton mot de passe Jenkins

```sh
cat /var/lib/jenkins/secrets/initialAdminPassword
```

### accéder à jenkins

```sh
http://<ip-address-public>:8080
```

## Installer un cluster Kubernetes (k3s recommende pour faible cpu, ram)

```sh
curl -sfL https://get.k3s.io | sudo sh -
```

### verifier que le cluster est en marche

```sh
sudo kubectl get nodes
```

### Copier le kubeconfig 

```sh
sudo cat /etc/rancher/k3s/k3s.yaml
```

## Installer Helm

```sh
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

### ckecker le version de helm

```sh
helm version
```

## Installer argocd

### créer un namespace argocd

```sh
kubectl create namespace argocd
```

### installer argocd

```sh
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### vérifier que argocd est en marche

```sh
kubectl get svc -n argocd
```

### Exposer le service ArgoCD (NodePort)

```sh
kubectl patch svc argocd-server -n argocd -p \
'{"spec": {"type": "NodePort","ports": [{"port": 80,"nodePort": 30007,"protocol": "TCP","targetPort": 8080}]}}'
```

### reverfier le service argocd

```sh
kubectl get svc -n argocd
```

### Mot de passe ArgoCD 

```sh
kubectl get secret argocd-initial-admin-secret -n argocd \
-o jsonpath="{.data.password}" | base64 -d
```

### accéder à argocd

```sh
http://<ip-address-public>:30007
```

## Installer SonarQube

