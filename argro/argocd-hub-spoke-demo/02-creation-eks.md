
````markdown
# 🚀 Mise en place ArgoCD Hub & Spoke avec EKS (Région : us-west-2)

## 1. Création des clusters EKS
Crée un cluster **hub** et deux clusters **spoke** dans `us-west-2` :

```bash
eksctl create cluster --name hub-cluster --region us-west-2
eksctl create cluster --name spoke-cluster-1 --region us-west-2
eksctl create cluster --name spoke-cluster-2 --region us-west-2
````

---

## 2. Vérifier les contextes disponibles

Après création, liste les contextes enregistrés dans ton kubeconfig :

```bash
kubectl config get-contexts
```

👉 Tu dois voir au moins :

* `hub-cluster`
* `spoke-cluster-1`
* `spoke-cluster-2`

---

## 3. Installer Argo CD sur le cluster Hub

⚠️ Cette étape se fait sur **hub-cluster** (ton cluster principal).

# switcher sur le cluster hub

````bash
kubectl config use-context hub-cluster 
````


```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

## 4. Se connecter à Argo CD

Récupère le mot de passe admin :

```bash
kubectl get secret argocd-initial-admin-secret -n argocd \
  -o jsonpath="{.data.password}" | base64 -d; echo
```

Puis connecte-toi au serveur Argo CD depuis ton EC2 :

```bash
argocd login <ARGOCD_SERVER> --username admin --password <MOT_DE_PASSE>
```

👉 `<ARGOCD_SERVER>` est l’adresse IP ou DNS exposée (NodePort, LoadBalancer ou Ingress).

---

## 5. Ajouter les clusters Spoke dans Argo CD

Ajoute chaque cluster en utilisant son **contexte kubeconfig** :

```bash
argocd cluster add spoke-cluster-1
argocd cluster add spoke-cluster-2
```

> Cela crée automatiquement un `ServiceAccount` + `ClusterRoleBinding` pour donner accès à ArgoCD.

---

## 6. Vérifier les clusters ajoutés

```bash
argocd cluster list
```

Exemple de sortie attendue :

```
SERVER                          NAME              NAMESPACE  STATUS
https://<api-hub>               hub-cluster       default    Successful
https://<api-spoke-1>           spoke-cluster-1   default    Successful
https://<api-spoke-2>           spoke-cluster-2   default    Successful
```

---

## 7. Déployer une application sur un cluster Spoke
 voir le dossier `Formation-Devops/argro/argocd-hub-spoke-demo/manifests/guest-book`
## 8. Suppression des clusters EKS

Quand tu n’as plus besoin des clusters :

```bash
eksctl delete cluster --name hub-cluster --region us-west-2
eksctl delete cluster --name spoke-cluster-1 --region us-west-2
eksctl delete cluster --name spoke-cluster-2 --region us-west-2
```




