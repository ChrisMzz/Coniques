import numpy as np
import sympy as sp
import algch_chris_mzz as alg

det, trace = np.linalg.det, np.trace

class Conique :
    def __init__(self, coeffs={}):
        if coeffs != {}:
            self.coeffs = coeffs
        else:
            rnd_coeffs = np.random.randint(-4,4,size=6)
            self.coeffs = {"x2":rnd_coeffs[0], "xy":rnd_coeffs[1], "y2":rnd_coeffs[2], \
                            "x":rnd_coeffs[3], "y":rnd_coeffs[4], "c":rnd_coeffs[5], }
        Q = self.matrice_homogeneisee()
        q = Q[:2,:2]
        est_propre = (det(Q) != 0)
        if est_propre:
            print(f"Elle est propre car det(Q) = {det(Q)} != 0.")
            a_centre = (det(q) != 0)
            if not a_centre:
                print(f"Elle n'est pas à centre car det(q) = 0.")
                self.type = "parabole"
            else:
                print(f"Elle est à centre car det(q) = {det(q)} != 0.")
                est_definie = ((q[0,0] > 0 and det(q) > 0) or (q[0,0] < 0 and det(q) < 0))
                if est_definie:
                    self.type = "ellipse"
                else:
                    self.type = "hyperbole"
        else:
            print(f"Elle est impropre car det(Q) = 0.")
    
    
    def compute(self):
        if self.type == "parabole":
            return Parabole(self.coeffs)
        elif self.type == "ellipse":
            return Ellipse(self.coeffs)
        elif self.type == "hyperbole":
            return Hyperbole(self.coeffs)
        else:
            return
    
    def __str__(self):
        return str([(self.coeffs[key],key) for key in self.coeffs])
    
    def matrice_homogeneisee(self):
        return np.array([[self.coeffs["x2"],self.coeffs["xy"]/2,self.coeffs["x"]/2],\
                         [self.coeffs["xy"]/2,self.coeffs["y2"],self.coeffs["y"]/2],\
                         [self.coeffs["x"]/2, self.coeffs["y"]/2, self.coeffs["c"]]])
        
    def gradient(self):
        return np.array([[2*self.coeffs["x2"], self.coeffs["xy"]], \
                         [self.coeffs["xy"], 2*self.coeffs["y2"]]])
        
    def find_centre(self):
        if type(self) == Parabole:
            self.centre = "n'a pas de centre"
            print(self.centre)
        else:
            df = self.gradient()
            self.centre = np.linalg.solve(df,np.array([-self.coeffs["x"],-self.coeffs["y"]]))
    
    
    
    
    
class Parabole (Conique):
    def __init__(self,coeffs):
        self.coeffs = coeffs
        print("Parabole", coeffs)
        Q = self.matrice_homogeneisee()
        q = alg.SqMatrix(Q[:2,:2][0],Q[:2,:2][1])
        print("Son axe focal (axe directeur) est donné par Ker(q), où :")
        print(f"q = \n{q}")
        print("Cet axe est dirigé par un vecteur v :")
        v = q.make_vector_from_solution(q.get_eigenvectors(sp.Float(0)),[sp.Symbol("x1"),sp.Symbol("x2")])
        print(f"v : \n{v}")
        print()
        print("On trouve ensuite un vecteur de df colinéaire à un vecteur v de Ker(q) :")
        print("df(x,y) = tv")
        print("L'intersection du sous-espace dirigé par ce vecteur avec la parabole nous indique son sommet.")
        self.find_centre()
        
            
class Ellipse (Conique):
    def __init__(self,coeffs):
        self.coeffs = coeffs
        print("Ellipse", coeffs)
        Q = self.matrice_homogeneisee()
        q = alg.SqMatrix(Q[:2,:2][0],Q[:2,:2][1])
        print(q)
        print("On cherche les vecteurs propres de q, ici :")
        print(q.get_all_generalised_eigenvectors())
        print("On trouve le sommet en cherchant le point critique, df(x,y) = (0,0) :")
        self.find_centre()
            
class Hyperbole (Conique):
    def __init__(self,coeffs):
        self.coeffs = coeffs
        print("Hyperbole", coeffs)
        Q = self.matrice_homogeneisee()
        q = alg.SqMatrix(Q[:2,:2][0],Q[:2,:2][1])
        print(q)
        print("On cherche les vecteurs propres de q, ici :")
        print(q.get_all_generalised_eigenvectors())
        print("(peut ne pas marcher avec mon module, mais fonctionne à la main)")
        print("On trouve le sommet en cherchant le point critique, df(x,y) = (0,0) :")
        self.find_centre()
        print("On cherche ensuite les vecteurs isotropes, c'est-à-dire des vecteurs non colinéaires qui annulent la forme q")
        
            




