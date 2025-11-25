RBAC (WHY, WHAT , WHERE, HOW)

---> SIMPLE MAIS COMPLEXE 

RBAC = ROLE BASED ACCESS CONTROL (CONTROLE D'ACCES BASE SUR LES ROLE )

-> QUUI PEUT FAIRE QUOI DANS LE CLUSTER K8S
-> PRINCIPE DU MOINDRE PRIVILEGE ()
-> SEPARATION DES DROIT 


WHAT: 

4 --> RESOURCES 

USERS  --------------------------------------------- SERVICE ACCOUNT 

NAMESPACE 
    --> (ROLE) , --> CLUSTERROLE, ROLEBINDING, CLUSTERROLEBINDING


WHERE: 

ROLE: LOCAL(NAMESPACE: DEV, PROD, STAG, )
CLUSTERROLE: NODES


HOW: 
---> USER NE SONT PAS GERER DIRRECTEMENT DANS K8S
USERS: 

X.509()
OIDC(OPEN ID CONNECT) OAUTH2(SSO)(SIGLE SIGN ON)
LDAP(LIGHTWEWGHT DIRECTORY ACCESS PROTOCOL)
SSO
IAM(IDENTITY AND ACCESS MANAGEMENT)


SERVICE ACCOUNT 

ROLE : 
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: lecteur-pods
  namespace: dev
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]

ROLEBINDING:
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: liaison-lecteur
  namespace: dev
subjects:
- kind: User
  name: alice@example.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: lecteur-pods
  apiGroup: rbac.authorization.k8s.io



SERICEACCOUNT:
apiVersion: v1
kind: ServiceAccount
metadata:
  name: mon-service-account
  namespace: dev


BINDING:

kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: liaison-sa
  namespace: dev
subjects:
- kind: ServiceAccount
  name: mon-service-account
  namespace: dev
roleRef:
  kind: Role
  name: lecteur-pods
  apiGroup: rbac.authorization.k8s.io


# FOUNISSEUR D'IDENTITE ( IDENTITY PROVIDER )

GOOGLE, GITHUB, AZURE  (OIDC)
OKTA (IAM/OIDC/SSO) SSO, LDAP, OIDC
KEYCLOK(IAM/OIDC/SSO)
DEX
AWS IAM

# RELATION ENTRE USER, / SERCIEACCOUNT, ROLEBINDING, ROLE, RESOURCES

user/serviceaccount --- > rolebinding-----role----->resources



# tester les permission:

kubectl auth can-i get pods --as=alice@example.com --namespace=dev
kubectl auth can-i list secrets --as=system:serviceaccount:dev:mon-service-account


