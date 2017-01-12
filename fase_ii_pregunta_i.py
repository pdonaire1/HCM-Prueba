# -*- coding: utf-8 -*-
"""
    Created by: @pdonaire1
    
    1. Crear un método que reciba un string y quite los caracteres 
       duplicados consecutivos, tener en cuenta que el string contiene 
       solo letras latinas minúsculas.
"""

class CleanString:
    def __init__(self, value):
        self.value = list(value.decode('utf-8'))
    def validate_string(self, i=0, value=[]):
        if value == []:
            value = self.value
        # remover caracteres duplicados consecutivos
        if len(value) > i+1:
            if value[i] == value[i+1]:
                del value[i+1]
                self.validate_string(i, value)
            else:
                self.validate_string(i+1, value)
        return ''.join(value)
    def validate_by_for(self):
        value = self.value
        i = 0
        while len(value) > i+1:
            if (value[i+1] == value[i]):
                del value[i+1]
            else:
                i+=1
        return ''.join(value)
 

c = CleanString('aaaa')
print 'aaaa validado con sentencia for: ',c.validate_by_for()
print 'aaaa validado con recursividad: ', c.validate_string()
c = CleanString('abccaaab')
print 'abccaaab validado con sentencia for: ',c.validate_by_for()
print 'abccaaab validado con recursividad: ', c.validate_string()
