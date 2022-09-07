class CellException(Exception):
    pass

class CellIntegerException(CellException):
    pass

class CellFloatException(CellException):
    pass

class CellStringException(CellException):
    pass


class Cell:
    def __init__(self, min_value, max_value):
        self._min_value = min_value
        self._max_value = max_value
        self._value = None
        self._ex_dict = {'CellInteger':CellIntegerException, 'CellFloat':CellFloatException, 'CellString':CellStringException}

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        if self.chek(new):
            self._value = new

    def chek(self, x):
        if self.__class__.__name__ != 'CellString' and self._max_value>=x>=self._min_value:
            return True
        elif self.__class__.__name__ == 'CellString' and self._max_value>=len(x)>=self._min_value:
            return True
        else:
            raise self._ex_dict[self.__class__.__name__]

class CellInteger(Cell):
    pass

class CellFloat(Cell):
    pass

class CellString(Cell):
    pass


class TupleData:
    def __init__(self, *args):
        self.lst = list(args)

    def __getitem__(self, item):
        self.cheker(item)
        return self.lst[item].value

    def __setitem__(self, key, value):
        if self.cheker(key)==True and self.lst[key].chek(value)==True:
            self.lst[key].value = value

    def cheker(self, x):
        if not (len(self.lst) - 1>=x>=0):
            raise IndexError
        else:
            return True

    def __len__(self):
        return len(self.lst)

    def __iter__(self):
        self.indx = 0
        return self

    def __next__(self):
        a = self.indx
        self.indx+=1
        if a > len(self.lst)-1:
            raise StopIteration
        else:
            return self.lst[a].value

# эти строчки в программе не менять!
ld = TupleData(CellInteger(0, 10), CellInteger(11, 20), CellFloat(-10, 10), CellString(1, 100))

try:
    ld[0] = 1
    ld[1] = 20
    ld[2] = -5.6
    ld[3] = "Python ООП"
except CellIntegerException as e:
    print(e)
except CellFloatException as e:
    print(e)
except CellStringException as e:
    print(e)
except CellException:
    print("Ошибка при обращении к ячейке")
except Exception:
    print("Общая ошибка при работе с объектом TupleData")
