# coding = UTF-8

# ------------------------------
# @topic：波士顿学校选择机制
# @author：张晨峰
# @date：2017/10/18
# ------------------------------

from collections import defaultdict


class Student:
    """ 学生类

    :param str name: 学生姓名
    :param list preference: 学生偏好
    :return: 无返回值
    """
    def __init__(self,name,preference):
        # 学生姓名
        self.name = name
        # 学生偏好
        self.preference = preference
        # 学生被哪个学校接受，初始值为None
        self._be_accepted = None

    def pop_reference(self):
        """ 弹出偏好

        :return: 返回排名最靠前的偏好，如果偏好集为空，那么返回None
        """
        if len(self.preference) > 0:
            return self.preference.pop(0)
        else:
            return None

    def be_accepted_by(self, school_name):
        """ 接受的信息

        :param str school_name: 设置被哪所学校接受
        :return:
        """
        self._be_accepted = school_name

    def is_be_accepted(self):
        """ 是否被录取

        :return: 若被学校录取，返回True，否则返回False
        """
        if self._be_accepted is None:
            return False
        else:
            return True

    def __repr__(self):
        """ 输出

        :return: 无返回值
        """
        fmt = 'Student {}: {}, be accepted by {}.'
        if self._be_accepted is None:
            return fmt.format(self.name, ','.join(self.preference), 'None')
        else:
            return fmt.format(self.name, ','.join(self.preference), self._be_accepted)


class School:
    """ 学校类

    :param str name: 学校名称
    :param list preference: 学校对学生的偏好
    :param int quantity: 学校招生的配额
    :return: 无返回值
    """
    def __init__(self,name,preference,quantity):
        # 学校名称
        self.name = name
        # 学校对学生的偏好
        self.preference = preference
        # 学校招生的配额
        self.quantity = quantity
        # 学校接受学校的名单，是一个Student对象的列表，初始值为None
        self._accept = None

    def accept(self, apply_students):
        """ 学校选择学生的算法（波士顿机制）

        :param list apply_students: 学生的列表
        :return: 无返回值
        """
        # 设置初始值为空列表
        if self._accept is None:
            self._accept = []
        # 如果申请的学生数量小于等于学校现有的配额，那么接受所有申请的学生；
        # 如果申请的学生数量大于学校现有的配额，那么就招生配额允许的排名靠前的学生
        if len(apply_students) <= self.quantity:
            # 把所申请的所有学生都放进录取名单
            self._accept.extend(apply_students)
            for student in apply_students:
                # 修改每个学生对象的录取信息，被当前学校所录取
                student.be_accepted_by(self.name)
            # 当前的配额为原有配额减去招收的学生数量
            self.quantity -= len(apply_students)
        else:
            # 对申请的学生按照当前学校的偏好进行排序，student_order是个字典，{序号：学生对象}
            student_order = {self.preference.index(student.name):student for student in apply_students}
            # 按照配额，接受排名靠前的学生
            accepted_students = [student_order[key] for key in sorted(student_order)[0:self.quantity]]
            for accepted_student in accepted_students:
                # 修改每个学生对象的录取信息，被当前学校所录取
                accepted_student.be_accepted_by(self.name)
            # 把录取的学生添加到学校的录取名单中
            self._accept.extend(accepted_students)
            # 学校剩余的名额为原有的名额减去录取的名额
            self.quantity -= len(accepted_students)

    def __repr__(self):
        """ 输出

        :return: 无返回值
        """
        fmt = 'School {}({}): {}, accepted {}.'
        if self._accept is None:
            return fmt.format(self.name, str(self.quantity), ','.join(self.preference), 'None')
        else:
            return fmt.format(self.name, str(self.quantity), ','.join(self.preference), self._accept)


class Matcher:
    """ 匹配类

    :param list students: 学生对象列表
    :param list schools: 学校对象列表
    :return: 无返回值
    """
    def __init__(self, students, schools):
        # 设置学生列表
        self.students = students
        # 设置学校列表
        self.schools = schools
        # 设置学校这字典，{学校名称：学校}
        self._schools_dict = {school.name:school for school in self.schools}

    def matching(self,info=True):
        # 每次读取学生最靠前的偏好，如有N所学校，则循环为N次
        for round in range(len(self.schools)):
            # 控制打印标志
            print_signal = False
            # 设置一个字典，用来储存每所学校申请的学生列表，{学校名称：学生}
            apply_dict = defaultdict(list)
            for student in self.students:
                if student.is_be_accepted():
                    continue
                apply_dict[student.pop_reference()].append(student)
            # 对于所有被申请的学校，调用学校选择学生的算法程序
            for key in apply_dict:
                if self._schools_dict[key].quantity > 0:
                    print_signal = True
                    self._schools_dict[key].accept(apply_dict[key])
            if info:
                if print_signal:
                    # 打印每一轮选择后学校和学生的基本状态
                    print('*'*20)
                    print('round ', round + 1)
                    for school in self.schools:
                        print(school)
                    for student in self.students:
                        print(student)
                    print('='*20)

    def result(self):
        fmt = '='*20
        fmt = ''.join([fmt,'Final Result',fmt,'\n'])
        for school in self.schools:
            if school._accept is not None:
                fmt = ''.join([fmt,'School ',school.name,': ',','.join(sorted([student.name for student in school._accept])),'\n'])
            else:
                fmt = ''.join([fmt,'School ',school.name,': ','None','\n'])

        fmt = ''.join([fmt,'-'*52,'\n'])
        for student in self.students:
            if student._be_accepted is not None:
                fmt = ''.join([fmt,'Student ',student.name,': ',student._be_accepted,'\n'])
            else:
                fmt = ''.join([fmt, 'Student ', student.name, ': ', 'None\n'])
        return fmt

if __name__ == '__main__':
    students = [Student('i1', ['c1', 'c2', 'c3']),
                Student('i2', ['c1', 'c3', 'c2']),
                Student('i3', ['c3', 'c2', 'c1']),
                Student('i4', ['c3', 'c1', 'c2'])]
    schools = [School('c1', ['i1', 'i2', 'i3', 'i4'], 1),
               School('c2', ['i2', 'i3', 'i1', 'i4'], 1),
               School('c3', ['i1', 'i2', 'i4', 'i3'], 1)]
    matcher = Matcher(students=students,schools=schools)
    print(students)
    print(schools)

    matcher.matching(info=False)
    print(matcher.result())



