from Person import Person

class Student(Person):

    def __init__(self, name):
        super().__init__(name)
    
    def setDNI(self, DNI):
        self.DNI = DNI

    def getDNI(self):
        return self.DNI
        


s = Student("John Constantine")
s.setDNI("40248013")
print("DNI = {}".format(s.getDNI()))