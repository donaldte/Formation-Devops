

## **Installer EKS**

Veuillez suivre la documentation des **prérequis** avant cette étape.

---

### ✅ **Installation avec Fargate**

```bash
eksctl create cluster --name demo-cluster --region us-west-2 --fargate
```

> Cette commande crée un cluster EKS nommé `demo-cluster` dans la région `us-west-2`, en utilisant **Fargate** (mode sans gestion de nœuds EC2, les pods sont directement exécutés sur des ressources managées).

---

### ❌ **Supprimer le cluster**

```bash
eksctl delete cluster --name demo-cluster --region us-west-2
```

> Cette commande supprime le cluster EKS nommé `demo-cluster`.

