import numpy as np
import multiprocessing as mp
import time
import datetime

class Element:
    def get_name(self):
        return self._name

    def get_row(self):
        return self._row

    def get_data(self):
        return self._data

    def get_count(self):
        return self._count

    def get_mean(self):
        return self._mean

    def get_mp(self):
        return self._mp

    def get_array_valids(self):
        return self._array_valids

    def get_array_nones(self):
        return self._array_nones


class Variable(Element):
    def __init__(self, name, row, data):
        self._name = name
        self._row = row
        self._data = data
        self._count = None
        self._mean = None
        self._array_valids = None
        self._array_nones = None

    def compute(self):
        time.sleep(2)
        self._count = self.get_count()
        self._mean = self.get_mean()
        print("OK")
        return "OK"

    def get_name(self):
        return self._name

    def get_row(self):
        return self._row

    def get_data(self):
        return self._data

    def get_count(self):
        if self._count is None:
            # _count is None, it is not pre-cumputed, compute now!
            self._count = self._data.size
        return self._count

    def get_mean(self):
        if self._mean is None:
            # _mean is None, it is not pre-cumputed, compute now!
            self._mean = self._data.mean()
        return self._mean

    def get_array_valids(self):
        return self._array_valids

    def get_array_nones(self):
        return self._array_nones


class Split(Element):
    def __init__(self, name):
        self._name = name
        self._elements = []
        self._data = None
        self._count = None
        self._mean = None

    def compute(self, do_mp = False):
        if do_mp:
            fns = []
            for e in self._elements:
                fns.append(e.compute)
            '''
            inn = [self.get_count(), self.get_mean()]
            pool = mp.Pool()
            returns = pool.map(self, inn)
            print(returns)
            pool.close()
            for ret in returns:
                a = ret

            p1 = mp.Process(target=self.get_count)
            p1.start()
            p2 = mp.Process(target=self.get_mean)
            p2.start()
            p1.join()
            p2.join()
            '''

            proc = []
            for fn in fns:
                p = mp.Process(target=fn)
                p.start()
                proc.append(p)
            for p in proc:
                p.join()
        else:
            for e in self._elements:
                e.compute()
        self._data = self.get_data()
        self._count = self.get_count()
        self._mean = self.get_mean()
        return "OK"

    def get_name(self):
        return self._name

    def get_row(self):
        rows = []
        for e in self._elements:
            rows.append(e.get_row())
        return rows

    def get_data(self):
        data = np.array([])
        for e in self._elements:
            data = np.append(data, e.get_data())
        return data

    def get_count(self):
        if self._data is None:
            self._data = self.get_data()
        self._count = self._data.size
        return self._count

    def get_mean(self):
        if self._data is None:
            self._data = self.get_data()
        if self._mean is None:
            # _mean is None, it is not pre-cumputed, compute now!
            self._mean = self._data.mean()
        return self._mean

    def get_split_count(self):
        split_count = {}
        for e in self._elements:
            split_count[e.get_name()] = (e.get_row(), e.get_count())
        return split_count

    def add_element(self, element):
        self._elements.append(element)


def main():
    start = time.perf_counter()

    levels = {}
    levels[0] = []
    levels[0].append(Split('Table_0_0'))  # Total
    for i in range (1, 4):
        levels[i] = []
        levels[i].append(Split(f'Table_{i}_0'))  # SubTotal
        levels[0][0].add_element(levels[i][0])
        for j in range(1,4):
            levels[i].append(Split(f'Table_{i}_{j}'))
            levels[i][0].add_element(levels[i][j])

    rng = np.random.default_rng()
    levels[1][1].add_element(Variable('Stephan Fox', 3, rng.standard_normal(10000000)))
    levels[1][2].add_element(Variable('John Kowal', 4, rng.standard_normal(10000000)))
    levels[1][3].add_element(Variable('Joanna Denver', 5, rng.standard_normal(10000000)))
    levels[2][1].add_element(Variable('Marie Smith', 7, rng.standard_normal(10000000)))
    levels[2][2].add_element(Variable('Anna Brown', 8, rng.standard_normal(10000000)))
    levels[2][3].add_element(Variable('Mirka Wayne', 9, rng.standard_normal(10000000)))
    levels[3][1].add_element(Variable('Noname1', 7, rng.standard_normal(10000000)))
    levels[3][2].add_element(Variable('Noname2', 8, rng.standard_normal(10000000)))
    levels[3][3].add_element(Variable('Noname3', 9, rng.standard_normal(10000000)))


    levels[0][0].compute(True)

    '''
    print(f'Total: {levels[0][0].get_name()}, List: {levels[0][0].get_split_count()}, Total_count: {levels[0][0].get_count()}, Total_mean: {levels[0][0].get_mean()}, Total_data: {levels[0][0].get_data()}')
    print(f'Total1: {levels[1][0].get_name()}, List: {levels[1][0].get_split_count()}, Total_count: {levels[1][0].get_count()}, Total_mean: {levels[1][0].get_mean()}, Total_data: {levels[1][0].get_data()}')
    print(f'Total2: {levels[2][0].get_name()}, List: {levels[2][0].get_split_count()}, Total_count: {levels[2][0].get_count()}, Total_mean: {levels[2][0].get_mean()}, Total_data: {levels[2][0].get_data()}')
    '''

    print(f'Total: {levels[0][0].get_name()}, List: {levels[0][0].get_split_count()}, Total_count: {levels[0][0].get_count()}, Total_mean: {levels[0][0].get_mean()}')
    print(f'Total1: {levels[1][0].get_name()}, List: {levels[1][0].get_split_count()}, Total_count: {levels[1][0].get_count()}, Total_mean: {levels[1][0].get_mean()}')
    print(f'Total2: {levels[2][0].get_name()}, List: {levels[2][0].get_split_count()}, Total_count: {levels[2][0].get_count()}, Total_mean: {levels[2][0].get_mean()}')

    end = time.perf_counter()

    print("Elapsed time: " + str(datetime.timedelta(seconds=end-start)))

if __name__ == '__main__':
    main()
