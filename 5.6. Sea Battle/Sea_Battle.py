"""в данной сборке для расстановки кораблей на поле используется RND без словаря уже ранее сгенерированных значений, 
также при уменьшении поля во избежании зависания при поиске места для установки нового корабля при переборе n-нного количества операций расстановка новых кораблей прекращается"""

from random import randint, choice

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._x = x
        self._y = y
        self._length  = length
        self._tp = tp
        self._is_move = True
        self._cells = [1 for _ in range(self._length)]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        x, y = self.get_start_coords()
        self.check_move_possibity()
        if self._is_move:
            if self._tp == 1:
                self.set_start_coords(x + go, y)

            if self._tp == 2:
                self.set_start_coords(x, y + go)
        return self.get_start_coords()

    def is_collide(self, ship):
        coords_lst_a = self.collide_calculater(self)
        coords_lst_b = self.collide_calculater(ship)
        map_zero_zone = [(-1,-1), (-1,0),(-1,+1), (0,+1), (+1,+1),(+1, 0), (+1,-1), (0,-1)]
        res = [(a + x, b + y) for a,b in coords_lst_a for x,y in map_zero_zone if x+a>=0 and y+b>=0]
        coords_lst_a.extend(res)
        if len(set(coords_lst_a).intersection(coords_lst_b))>0:
            return True
        else:
            return False

    @staticmethod
    def collide_calculater(ship):
        temp = []
        if ship._tp == 1:
            for i in range(ship._length):
                x, y = ship.get_start_coords()
                temp.append((x + i, y))
        if ship._tp == 2:
            for i in range(ship._length):
                x, y = ship.get_start_coords()
                temp.append((x, y + i))
        return temp

    def check_move_possibity(self):
        for i in self._cells:
            if i==2:
                self._is_move = False

    def is_out_pole(self, size):
        x, y = self.get_start_coords()
        if self._tp == 1:
            if size - 1>=y>=0 and size - self._length >= x >= 0:
                return False
            else:
                return True
        if self._tp == 2:
            if size - 1>=x>=0 and size - self._length >= y >= 0:
                return False
            else:
                return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __repr__(self):
        return f'<{self._cells}>'


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self.pole = [[0 for i in range(self._size)] for j in range(self._size)]

    def init(self):
        ships_on_pole = []
        list_of_ships = [(i, randint(1,2)) for i in [1,1,1,2,2,2,3,3,4,]]
        counter = 0
        for ship in list_of_ships:
            l, t = ship
            while True:
                if counter>=1000:   #  лимит операций для выхода из цикла при невозможности найти новое место для корабля
                    
                    break
                counter+=1
                x = randint(0, self._size)
                y = randint(0, self._size)
                if not Ship(l, t, x, y).is_out_pole(self._size):
                    res = []
                    if len(ships_on_pole)>0:
                        for i in ships_on_pole:
                            res.append(Ship(l, t, x, y).is_collide(i))
                        if len(set(res))==1 and res[0]==False:
                            ships_on_pole.append(Ship(l, t, x, y))
                            break
                    else:
                        ships_on_pole.append(Ship(l, t, x, y))
        for ship in ships_on_pole:
            self._ships.append(ship)

    def list_of_ships_collider_checker(self, ship, ship_w_new_coord):
        temp_lst = self._ships[:]
        temp_lst.pop(temp_lst.index(ship))
        res = []
        for i in temp_lst:
            res.append(ship_w_new_coord.is_collide(i))
        if len(set(res))==1 and res[0]==False:
            return True
        else:
            return False

    def get_ships(self):
        return self._ships

    def move_ships(self):
        for ship in self._ships:
            go = choice([1,-1])
            x, y = ship.get_start_coords()
            l, t = ship._length, ship._tp
            temp = [go]
            while True:
                if len(temp)==3:
                    go = 0
                    break
                else:
                    if Ship(l, t, *Ship(l, t, x, y).move(go)).is_out_pole(self._size) or self.list_of_ships_collider_checker(ship, Ship(l,t,x,y)):
                        go = -go
                        temp.append(go)
                    else:
                        break
            ship.move(go)

    def show(self):
        self.pole = [[0 for i in range(self._size)] for j in range(self._size)]
        for ship in self._ships:
            x, y = ship.get_start_coords()
            for i in range(len(ship._cells)):
                if ship._tp == 1:
                    self.pole[x + i][y] = ship._cells[i]
                if ship._tp == 2:
                    self.pole[x][y + i] = ship._cells[i]
        for i in self.pole:
            print(*i)

    def get_pole(self):
        self.pole = [[0 for i in range(self._size)] for j in range(self._size)]
        for ship in self._ships:
            x, y = ship.get_start_coords()
            for i in range(len(ship._cells)):
                if ship._tp == 1:
                    self.pole[x + i][y] = ship._cells[i]
                if ship._tp == 2:
                    self.pole[x][y + i] = ship._cells[i]
        for k, v in enumerate(self.pole):
            self.pole[k] = tuple(v)

        return tuple(self.pole)
