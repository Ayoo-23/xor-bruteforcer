# xor-bruteforcer
Bruteforcer en XOR!

# Outil de cryptanalyse à clé répétitive XOR

Ce projet a été créé dans le cadre d'un défi communautaire en cryptographie.  
L'objectif était de récupérer le texte en clair et la clé d'un message crypté à l'aide d'un chiffrement XOR à clé répétitive.
Au final, le ciphertext n'a pas été cripté en xor.. mais c'était bien tenté!

## 🔍 Fonctionnalités du programme
- Teste plusieurs longueurs de clé  
- Évalue les candidats au texte en clair à l'aide de la fréquence des caractères anglais (log-vraisemblance)  
- Utilise la **recherche par faisceau** pour explorer les candidats prometteurs  
- Utilise l'**escalade** avec des mutations aléatoires pour améliorer la meilleure clé  
- Récupère à la fois la clé et le message déchiffré  

## 🧠 Concepts utilisés
- Modélisation statistique du langage  
- Algorithmes de recherche heuristique  
- Cryptanalyse des chiffrements faibles  
- Optimisation et performances Python  

## ⚠️ Important
Ce projet est **strictement éducatif** et n'a été utilisé que sur des textes chiffrés fournis dans le cadre d'un événement communautaire.

