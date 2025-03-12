### **Optimisation des coûts AWS Cloud - Identification des ressources obsolètes**  
#### **Identification des instantanés EBS obsolètes**  

Dans cet exercice, nous allons créer une **fonction Lambda** qui identifie les **instantanés EBS** qui ne sont plus associés à une **instance EC2 active** et les supprime afin de **réduire les coûts de stockage**.  

---

### **Description**  
La fonction Lambda effectuera les actions suivantes :  

1. **Récupération de tous les instantanés EBS** appartenant au compte AWS en cours (**'self'**).  
2. **Récupération de la liste des instances EC2 actives** (états **"running"** et **"stopped"**).  
3. **Vérification de chaque instantané** :  
   - Si l’instantané est **associé à un volume** et que ce volume **n'est plus attaché à aucune instance EC2 active**, alors il est considéré comme **obsolète**.  
4. **Suppression des instantanés obsolètes** pour **optimiser les coûts de stockage**.  

Ce processus garantit que l'espace utilisé par les instantanés inutilisés est libéré, évitant ainsi des **coûts supplémentaires** pour des ressources non exploitées. 🚀