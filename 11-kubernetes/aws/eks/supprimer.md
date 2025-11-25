

## 🧨 Étape 1 – Supprimer l’application déployée (Deployment, Service, Ingress)

```bash
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/examples/2048/2048_full.yaml
```

---

## 🧨 Étape 2 – Supprimer le Fargate Profile

Tu dois supprimer **chaque Fargate profile** attaché au cluster :

```bash
eksctl delete fargateprofile --cluster demo-cluster --name alb-sample-app --region us-west-2
```

*Adapte `alb-sample-app` au nom réel de ton Fargate profile si besoin.*

---

## 🧨 Étape 3 – Supprimer le contrôleur ALB

Si tu l’as installé avec Helm :

```bash
helm uninstall aws-load-balancer-controller -n kube-system
```

---

## 🧨 Étape 4 – Supprimer le Service Account IAM

```bash
eksctl delete iamserviceaccount \
  --cluster demo-cluster \
  --name aws-load-balancer-controller \
  --namespace kube-system
```

---

## 🧨 Étape 5 – Supprimer la IAM Policy manuellement (facultatif mais propre)

Liste les policies :

```bash
aws iam list-policies | grep AWSLoadBalancerControllerIAMPolicy
```

Supprime la policy si elle n’est plus utilisée :

```bash
aws iam delete-policy --policy-arn arn:aws:iam::<votre-id>:policy/AWSLoadBalancerControllerIAMPolicy
```

---

## 🧨 Étape 6 – Supprimer le cluster EKS

```bash
eksctl delete cluster --name demo-cluster --region us-west-2
```

---

## 🧨 Étape 7 – Vérifie que tout est bien supprimé

Tu peux aller dans la **console AWS** (EC2, IAM, EKS, VPC) pour confirmer qu'il ne reste :

* Aucun ALB
* Aucun VPC ou Security Group créé par EKS (optionnel)
* Aucune IAM Policy résiduelle


