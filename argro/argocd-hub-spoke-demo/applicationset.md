 **2 apps en même temps**, chacune ciblant un cluster différent. Tu peux le coller tel quel.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook-multi-spokes
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - name: spoke1
            cluster: spoke-cluster-1     # doit correspondre au nom de contexte ajouté via `argocd cluster add`
            namespace: default
          - name: spoke2
            cluster: spoke-cluster-2
            namespace: default
          - name: spoke3
            cluster: spoke-cluster-3
            namespace: default
          - name: spoke4
            cluster: spoke-cluster-4
            namespace: default
          - name: spoke5
            cluster: spoke-cluster-5
            namespace: default
          - name: spoke6
            cluster: spoke-cluster-6
            namespace: default
  template:
    metadata:
      name: guestbook-{{name}}
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps
        path: guestbook
        targetRevision: HEAD
      destination:
        name: "{{cluster}}"              # utilise le nom du cluster enregistré dans Argo CD
        namespace: "{{namespace}}"
      syncPolicy:
        automated: {}                    # sync auto + self-heal (optionnel)
```

### Appliquer le manifeste

```bash
kubectl apply -n argocd -f applicationset-guestbook.yaml
```

Ça va créer automatiquement :

* `guestbook-spoke1` déployée sur `spoke-cluster-1`
* `guestbook-spoke2` déployée sur `spoke-cluster-2`

---

## Notes utiles

* Les valeurs `spoke-cluster-1` et `spoke-cluster-2` doivent **matcher les noms de contexte** que tu as ajoutés avec `argocd cluster add ...`.
* Tu peux voir ces noms dans :

  ```bash
  argocd cluster list
  ```
* Tu peux changer `repoURL`/`path` pour déployer **ton** repo.

---

## Variante (scalable) avec sélection de clusters par label

Si tu veux cibler **tous les clusters** labellisés `env=spoke` sans les lister un par un :

1. Ajoute un label sur les secrets de clusters dans `argocd` (un par cluster) :

```bash
kubectl label secret -n argocd $(kubectl get secret -n argocd -l "argocd.argoproj.io/secret-type=cluster" -o name | grep spoke-cluster-1 | cut -d'/' -f2) env=spoke
kubectl label secret -n argocd $(kubectl get secret -n argocd -l "argocd.argoproj.io/secret-type=cluster" -o name | grep spoke-cluster-2 | cut -d'/' -f2) env=spoke
```

2. Utilise ce manifest :

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook-all-spokes
  namespace: argocd
spec:
  generators:
    - clusters:
        selector:
          matchLabels:
            env: spoke
  template:
    metadata:
      name: guestbook-{{name}}
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps
        path: guestbook
        targetRevision: HEAD
      destination:
        name: "{{name}}"        # nom du cluster issu du generator
        namespace: default
      syncPolicy:
        automated: {}
```