# -*- coding: utf-8 -*-
"""
    created by: @pdonaire1
    2. Un entero se considera redondo si termina con uno o más ceros. 
       Dada una lista de enteros encontrar el número redondo mas alto 
       en ella y devolver su posición en la lista, si no hay
       números redondos en la matriz devolver -1.
"""

class FindHigherInteger:
    def __init__(self, value):
        self.value = value
    def find_higher(self, i=0, value=[], higher_index=-1, higher_value=-1):
        # index_higher = -1
        if i == 0:
            value = self.value
        if len(value) > i:
            if int( str(value[i])[-1] ) == 0 and int(value[i]) > higher_value:
                higher_index = i
                higher_value = value[i]
            higher_index = self.find_higher(i+1, value, higher_index, higher_value)
        return higher_index
    def find_higher_by_for(self):
        value = self.value
        higher_value = -1
        higher_index = -1
        for (i, val) in enumerate(value):
            if (str(value[i])[-1] == '0' and val > higher_value):
                higher_value = val
                higher_index = i
        return higher_index

f = FindHigherInteger([0, 5, 10, 15])
print 'Para [0, 5, 10, 15], la salida debe ser 2:'
print 'resultado por recursividad: %s '%(f.find_higher())
print 'resultado por loop for: %s '%(f.find_higher_by_for())

f = FindHigherInteger([1, 2, 3, 4, 5])
print 'Para [1, 2, 3, 4, 5], la salida debe ser -1:'
print 'resultado por recursividad: %s'%(f.find_higher())
print 'resultado por loop for: %s'%(f.find_higher_by_for())

f = FindHigherInteger([10, 5, 30, 18])
print 'Para [10, 5, 30, 18], la salida debe ser 2'
print 'resultado por recursividad: %s'%(f.find_higher())
print 'resultado por loop for: %s'%(f.find_higher_by_for())

# f = FindHigherInteger([20, 5, 10, 15])
# print 'debe ser 0'
# print 'resultado por recursividad: %s'%(f.find_higher())
# print 'resultado por loop for: %s'%(f.find_higher_by_for())
