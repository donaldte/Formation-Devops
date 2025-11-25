
````markdown
# Installer Argo CD

## 1. Créer l’espace de noms (namespace) Argo CD
```bash
kubectl create namespace argocd
````

## 2. Appliquer le manifeste d’installation officiel

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

---

# Exécuter Argo CD en mode HTTP (Insecure)

Pour exécuter Argo CD en mode **HTTP non sécurisé**, consultez la documentation officielle :
[Configuration Argo CD en HTTP Mode](https://github.com/argoproj/argo-cd/blob/54f1572d46d8d611018f4854cf2f24a24a3ac088/docs/operator-manual/argocd-cmd-params-cm.yaml#L82)

---

# Exposer le service Argo CD Server en mode NodePort

Éditez le service `argocd-server` :

```bash
kubectl edit svc argocd-server -n argocd
```

Puis changez la valeur du champ **type** de :

```yaml
type: ClusterIP
```

à :

```yaml
type: NodePort
```
