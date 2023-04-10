import conique




coeffs = {"x2":1, "xy":2, "y2":1, "x":3, "y":-2, "c":1} # parabole

#coeffs = {"x2":2, "xy":6, "y2":5, "x":4, "y":6, "c":1} # ellipse

#coeffs = {"x2":2, "xy":-4, "y2":0, "x":-3, "y":3, "c":1} # hyperbole



f = conique.Conique(coeffs).compute()


#print(f.centre)


