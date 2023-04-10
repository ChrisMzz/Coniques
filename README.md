# Coniques

## Présentation 

Implémentation de certaines notions de géométrie, spécifiquement au programme de Géométrie 2 (L3 Mathématiques, AMU). Permet notamment d'obtenir des détails sur les aspects géométriques de certaines coniques en fonction des équations les définissant.
Utilise les modules `numpy` et `sympy`.

Utilise aussi le module [`algch_chris_mzz`](https://github.com/ChrisMzz/algch/releases) que j'ai écrit pour calculer certains espaces propres.
Ce module ne fonctionne pas très bien pour trouver les vecteurs propres des matrices associées aux parties quadratiques, mais semble fonctionner suffisamment bien pour trouver l'axe focal dans le cas où la conique est une parabole.

J'ai inclus des exemples de chaque type de conique que j'ai étudié en cours de géométrie, pour pouvoir vérifier chaque partie de mon code.

---

**DISCLAIMER**

Ce rep a pour unique but de m'aider à appliquer nos méthodes de résolutions vues en cours ; en écrivant et en relisant un programme qui peut résoudre des exercices, c'est parfois plus facile de comprendre ce qu'il faut faire à chaque étape de la résolution, mais en restant dans le cas général pour ne pas avoir la solution à un seul problème, ce qui est à mon sens le principal défaut de faire une liste d'exercices pour réviser.

---

## Structure

Le programme principal, qui contient les classes, est le fichier `conique.py`, qui contient la classe `Conique`, qui peut prendre les coefficients en argument, ou générer des coefficients aléatoires (pour tout de même pouvoir créer des exercices pour travailler dessus à la main).

Une initialisation de conique attendue est légèrement différente d'une initialisation standard :
```py
import conique

coeffs = {"x2":1, "xy":2, "y2":1, "x":3, "y":-2, "c":1}

f = conique.Conique(coeffs).compute()
```

`f = conique.Conique(coeffs)` crée un objet de type `conique.Conique`.

Le constructeur de `Conique` calcule certaines propriétés en fonction des coefficients donnés (ou générés), ce qui lui permet de déterminer de quelle type de conique il s'agit :
 - `est_propre = (det(Q) != 0)`, où $Q$ est la matrice homogénéisée de $f$ (représentant le cône de révolution dans $\mathbb{R}^3$). Si $Q$ est dégénérée, $f$ est impropre, donc on n'étudie pas ce cas.
 - `a_centre = (det(q) != 0)`, où $q$ est la matrice associée à la partie quadratique de $f$ ; si la conique étudiée n'est pas à centre, c'est une parabole.
 - `est_definie = ((q[0,0] > 0 and det(q) > 0) or (q[0,0] < 0 and det(q) < 0))`. Si $q$ est définie, alors $f$ décrit une ellipse ; sinon, $f$ décrit une hyperbole.
    * Si le déterminant de $q$ est positif, alors ses valeurs propres sont de même signe et $q$ est définie (positive) si et seulement si son mineur principal de dimension minimale est à déterminant positif. 
    * Réciproquement, si le déterminant de $q$ est négatif, alors ses valeurs propres sont de signes contraires et $q$ est définie (négative) si et seulement si son mineur principal de dimension minimale est à déterminant négatif.

`compute()` renvoie un objet d'une des classes `Parabole`, `Hyperbole` ou `Ellipse`, qui héritent toutes de `Conique`, en fonction de ces propriétés. La classification permet notamment de distinguer le comportement de certaines méthodes comme `find_center()`, définie de la manière suivante :
```py
    def find_centre(self):
        if type(self) == Parabole:
            self.centre = "n'a pas de centre"
            print(self.centre)
        else:
            df = self.gradient()
            self.centre = np.linalg.solve(df,np.array([-self.coeffs["x"],-self.coeffs["y"]]))
```
En effet, les paraboles n'ont pas de centre et le calcul nécessaire pour le trouver dans les deux autres cas n'aurait aucun sens dans le contexte d'un exercice sur une parabole.




### Ellipse

Le plus simple des trois cas, $q$ à centre, définie. 
Pour trouver des détails sur les aspects géométriques d'une ellipse, il faut trouver les vecteurs propres (et donc les valeurs propres) de la partie quadratique $q$, pour déterminer les axes (directeurs ?) de l'ellipse dans la base canonique. Avec un changement de base, on peut écrire l'équation réduite de l'ellipse : 
$$\lambda_1 x^2 + \lambda_2 y^2 = f(\Omega)$$
où $\lambda_1, \lambda_2$ sont les valeurs propres de $q$ et $\Omega$ est le centre de l'ellipse, trouvé en cherchant le vecteur qui annule le gradient de $f$, qu'on note $\nabla f$.

### Hyperbole

Le cas où $q$ est à centre, mais est indéfinie. 
Cette fois, on cherche aussi les vecteurs propres de $q$ (je suis fatigué donc j'ai oublié pourquoi mais je pense que c'est la base dans laquelle on se place pour l'étudier).
On cherche les vecteurs isotropes, c'est-à-dire les vecteurs qui annulent la partie quadratique $q$. Il faut bien sûr chercher des vecteurs qui engendrent deux espaces non confondus, donc non colinéaires (on cherche généralement en fixant $x = 0$ ou $x = 1$ et en essayant de résoudre).
Le centre se trouve, comme pour l'ellipse, en trouvant le vecteur qui annule le gradient de $f$.

### Parabole

Le plus dur des trois cas : $f$ n'est pas à centre.
Cette fois, on cherche l'axe focal, qui "dirige" la parabole, déterminé par $Ker(q)$, qu'on détermine dans le code en créant un vecteur à partir de la solution engendrée par le système associé à la valeur propre $0$ de $q$ (on sait que $0$ est valeur propre car $f$ est sans centre).
Ceci est déterminé par :
```py
v = q.make_vector_from_solution(q.get_eigenvectors(sp.Float(0)),[sp.Symbol("x1"),sp.Symbol("x2")])
```
On peut chercher un vecteur de $\nabla f$ colinéaire à ce vecteur de $Ker(q)$ :
$$\nabla f(x,y) = tv$$
et utiliser l'équation cartésienne obtenue pour trouver l'intersection avec $f$, et ainsi trouver son sommet.

