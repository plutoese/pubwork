# coding = UTF-8

# ------------------------------
# @topic：随机序列独裁机制
# @author：张晨峰
# @date：2017/10/24
# ------------------------------

from itertools import permutations
import numpy as np
import pandas as pd
import random


class Person:
    """ 个体类

    :param str name: 学生姓名
    :param list preference: 学生偏好
    :return: 无返回值
    """
    def __init__(self,name,preference):
        # 个体姓名
        self.name = name
        # 个体偏好
        self.preference = preference
        # 个体选择的物品，初始值为None
        self._choice = None

    def choose(self,items):
        """ 选择物品

        :return: 返回选择的物品
        """
        for preference in self.preference:
            if preference in items:
                self._choice = preference
                return preference
        return None

    @property
    def choice(self):
        """ 返回个体选择的物品

        :return: 返回个体选择的物品
        """
        return self._choice

    def is_choosed(self):
        """ 是否已经选择物品

        :return: 若已经选择物品，返回True，否则返回False
        """
        if self._choice is None:
            return False
        else:
            return True

    def __repr__(self):
        """ 输出

        :return: 无返回值
        """
        fmt = 'Person {}: {}, has choose item {}.'
        if self.is_choosed():
            return fmt.format(self.name, ','.join(self.preference), self.choice)
        else:
            return fmt.format(self.name, ','.join(self.preference), 'None')


class Item:
    """ 物品类

    :param str name: 物品名称
    :return: 无返回值
    """
    def __init__(self,name):
        # 学校名称
        self.name = name
        # 选择物品的个体名称，若无，则为None
        self._taken_by = None

    def is_taken(self):
        if self._taken_by is None:
            return False
        else:
            return True

    @property
    def taken_by(self):
        return self._taken_by

    def __repr__(self):
        """ 输出

        :return: 无返回值
        """
        fmt = 'Item {}: is taken by {}.'
        if self.is_taken():
            return fmt.format(self.name, 'None')
        else:
            return fmt.format(self.name, self.taken_by)


class Matcher:
    """ 匹配类

    :param list students: 学生对象列表
    :param list schools: 学校对象列表
    :return: 无返回值
    """
    def __init__(self, persons, items):
        # 设置个体列表
        self.persons = persons
        # 设置物品列表
        self.items = items
        self.items_dict = {item.name:item for item in items}

        # 生成个体选择顺序的排列
        self._ordered_person_permutations = list(permutations(self.persons,len(self.persons)))

        self.final_result = None

    def matching(self,info=True):
        matrix_list = []
        for ordered_person_list in self._ordered_person_permutations:
            items = list(self.items_dict.keys())
            for person in ordered_person_list:
                item_choosed = person.choose(items)
                self.items_dict[item_choosed] = person.name
                items.pop(items.index(item_choosed))
            
            matrix_result = pd.DataFrame(data=np.zeros([len(self.persons),len(self.items)],dtype=int),
                                         index=[person.name for person in self.persons],
                                         columns=[item.name for item in self.items])
            for person in self.persons:
                matrix_result.loc[person.name,person.choice] = 1
            matrix_list.append(matrix_result)
            if info:
                print('-'*50)
                print('Choose Order: {}'.format(','.join([mperson.name for mperson in ordered_person_list])))
                print('Choose Matrix')
                print(matrix_result)

        result = None
        for i in range(len(matrix_list)):
            if i < 1:
                result = matrix_list[i]
            else:
                result += matrix_list[i]

        self.final_result = (1/len(self._ordered_person_permutations))*result

    def result(self):
        fmt = '='*20
        fmt = ''.join([fmt,'Final Result',fmt,'\n'])

        fmt = ''.join([fmt,'Final Matrix:\n',self.final_result.__repr__(),'\n'])
        fmt = ''.join([fmt,'='*52])
        return fmt


if __name__ == '__main__':
    '''
    persons = [Person('p1', ['A', 'C', 'B']),
               Person('p2', ['A', 'B', 'C']),
               Person('p3', ['B', 'A', 'C'])]
    items = [Item('A'), Item('B'), Item('C')]
    matcher = Matcher(persons=persons, items=items)
    #print(persons)
    #print(items)

    matcher.matching()
    print(matcher.result())'''

    number = random.choice(range(4,8))

    item_names = []
    for m in range(number):
        if number > 9 and m < 10:
            item_names.append(''.join(['item0', str(m+1)]))
        else:
            item_names.append(''.join(['item', str(m+1)]))

    preference = []
    items = item_names[:]
    for k in range(number):
        random.shuffle(items)
        preference.append(items[:])

    persons = []
    for n in range(number):
        if number > 9 and n < 10:
            persons.append(Person(''.join(['p0', str(n+1)]), preference[n]))
        else:
            persons.append(Person(''.join(['p', str(n+1)]), preference[n]))

    items = [Item(item_name) for item_name in item_names]

    matcher = Matcher(persons=persons, items=items)
    print(persons)
    print(items)

    matcher.matching(info=True)
    print(matcher.result())

