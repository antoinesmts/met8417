# Tableau de bord - Gestion de la qualité au sein de restaurants (WebHarvy, Python et Tableau)

Le projet a été mené dans le cadre du cours MET8417 (Gestion des opérations) de l'UQAM à l'hiver 2020. Il fût réalisé au sujet d'une chaîne de restaurants montréalaise. 

Le logiciel de récupération des données WebHarvy a été utilisé afin de récolter les commentaires laissés sur la plateforme Google Maps au sujet des restaurants analysés. Les données ont ensuite été traitées par un script codé en langage Python à l’aide de différentes librairies (principalement la librairie Vader NLTK pour la réalisation de l’analyse d’opinion):
- Nettoyage des données afin de retirer toute donnée superflue. 
- Réalisation d’une analyse d’opinion avec l’algorithme Vader. Chaque commentaire se voit attribuer un score sur une échelle de -1 à 1. Afin de faciliter l’analyse, ils ont été organisés en trois catégories : négatif (-1 ≤ score < -0.2), neutre (-0.2 ≤ score ≤ 0.2), positif (0.2 < score ≤ 1). 
- Enregistrement des données dans une base de données MySQL. 

Le tableau de bord a ensuite été créé en connectant le logiciel Tableau à la base de données.
