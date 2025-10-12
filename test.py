# Algorithme de tri 
# tri par bulle ou propagation 
# def tri_bubble(liste):
#     permut = True 
#     passage = 0
#     while not permut:
#         permut = False
#         passage += 1
#         for i in range(len(liste)-passage): 
#             if liste[i] > liste[i+1]: 
#                 liste[i], liste[i+1] = liste[i+1], liste[i] 
#                 permut = True  
#     return liste
# range(1, 5) => 1, 2, 3, 4
# range(1) => 1
# range de 0 done  0 => 0
liste = [6, 3, 2, 1, 4, 5, 56, 0, -1]
def tri_selection(liste): 
    for i in range(1, len(liste)):
        en_cours = liste[i]
        j = i 
        while j>0 and en_cours < liste[j-1]:
            liste[j] = liste[j-1]
            j -= 1
        liste[j] = en_cours
    return liste

print(tri_selection(liste))