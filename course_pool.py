#!/usr/bin/env python
# encoding: utf-8

# �γ̳أ����ڴ��������йؿγ̵Ĳ���

import configure as cfg
from course_table import CourseTable
import debug

d = debug.Debug('course_pool')

class CoursePool:
    #------ ����ӿ� ------
    def id_to_course(self, courseid):
        return self._courseid_course_dict[courseid]

    def course_to_table(self, courseid):
        return self._courseid_table_dict[courseid]

    def find_max_course_num(self, tables):
        return max(tables, key=lambda x: x.get_course_num())

    def get_eachday_course(self, table):
        return table.eachday_course

    def get_teacher_courseids(self, t):
        return self._teacher_cid_dict[t]

    def get_sorted_undetermined(self):
        return self._sorted_undetermined

    def get_determined(self):
        return self._determined

    def get_detail_tables(self):
        result = []
        for table in self._tables:
            result.append('GRUOP: %s' % table.title)
            result.append(self._table_detail(table.table))
        return '\n'.join(result)

    #----��������
    def __init__(self, all_courses):
        # ���еĿγ�
        self._all_courses = all_courses
        # ÿ��courseid��Ӧ�Ŀγ�
        self._courseid_course_dict = self._get_courseid_course_dict()
        # ����group�Ŀγ̱�
        self._tables = self._get_all_tables()
        # group ��Ӧ�Ŀγ̱�
        self._group_table_dict = self._get_group_table_dict()
        # ÿ���γ̶�Ӧ�Ŀγ̱�
        self._courseid_table_dict = self._get_courseid_table_dict()
        # ÿ����ʦ�̵����пγ�id
        self._teacher_cid_dict = self._get_teacher_cid_dict()
        # Ԥ�õĿγ�
        self._determined = self._get_determined()
        # δԤ�õĿγ�����
        self._undetermined = self._get_undetermined()
        # ����Ŀγ�
        self._sorted_undetermined = self._sort_undetermined()

    def _get_determined(self):
        dc = []
        for c in self._all_courses:
            if not c.need_allocate_p():
                dc.append(c)
        return dc

    def _get_undetermined(self):
        udc = []
        for c in self._all_courses:
            if c.need_allocate_p():
                udc.append(c)
        return udc

    def _sort_undetermined(self):
        """�����еĿγ̽�������

        ������Ҫ��Ŀ�
        1. ��ͬһ�ſεİ༶Խ�࣬���ſ��ǰ����Ϊ�漰���˲�ͬ�Ŀα���
        2. һ�ſ���ʦҪ��Խ�ࣨ�������ÿ��ʱ������֮�⣬�������ڵ����ƣ���Խ��ǰ
        3. ��������ͬ��Ҫ��ģ�Ҫ��ΧԽխԽ��ǰ
        """
        # TODO
        return self._undetermined



    def _get_teacher_cid_dict(self):
        tcd = {}
        for c in self._all_courses:
            for t in c.teachers:
                try:
                    if c.cid not in tcd[t]:
                        tcd[t].append(c.cid)
                except KeyError:
                    tcd[t] = [c.cid]
        return tcd

    def _get_courseid_course_dict(self):
        ccd = {}
        for c in self._all_courses:
            ccd[c.cid] = c
        return ccd

    def _get_group_table_dict(self):
        "ÿ�� group ��Ӧһ�� table"
        gtd = {}
        for table in self._tables:
            gtd[table.title] = table
        return gtd

    def _get_all_groups(self):
        "�õ����е�group����"
        groups = []
        for c in self._all_courses:
            groups.extend(c.groups)
        return set(groups)

    def _get_courseid_table_dict(self):
        """���ؿγ���γ̶�Ӧ��group��table"""
        ctd = {}
        for c in self._all_courses:
            for g in c.groups:
                try:
                    # ȥ�أ���Ϊ�� _all_courses ������ܻ��������
                    # һ���Ŀγ̣�e.g.һ������������2��2ѧ�ֵ�X�Σ�
                    if self._group_table_dict[g] not in ctd[c.cid]:
                        ctd[c.cid].append(self._group_table_dict[g])
                except KeyError:
                    ctd[c.cid] = [self._group_table_dict[g]]
        return ctd

    def _get_all_tables(self):
        #�õ��꼶����Ӧ�γ̵�ӳ��
        groups = self._get_all_groups()

        # ��ʼ���γ̱�
        tables = []
        for k in groups:
            tables.append(CourseTable(k))
        return tables

    def _table_detail(self, num_table):
        "���ؿγ̱���������"
        s = ""
        for i in xrange(len(cfg.TIME)):
            s += cfg.TIME[i] + ' '
            for j in range(len(cfg.DAY)):
                cid = num_table[i][j]
                if cid == -1:
                    s += '_'*15
                else:
                    s += (self.id_to_course(cid).name+"_"*15)[:15]
                s += '  '
            s += '\n'
        return s



if __name__ == '__main__':
    import reader
    r = reader.Reader('test.csv')
    cp = CoursePool(r.courses)
    # ��ӡ���еĿγ�
    for c in cp._all_courses:
        print c.cid, c.name, c.credit, c.groups, c.teachers

    print 'ALL GROUPS: %s' % cp._get_all_groups()

    print '============='
    for i in cp._tables:
        print i
    print '-------------'
    for i in cp._group_table_dict:
        print 'GROUP: %s' % i
        print cp._group_table_dict[i]
    print 'ÿ���γ̶�Ӧ�Ŀγ̱���'
    for i in cp._courseid_table_dict:
        c = cp.id_to_course(i)
        print 'COURSE: %s %s %s' % (c.name, c.groups, c.teachers)
        for k in cp._courseid_table_dict[i]:
            print k
    print 'ÿ����ʦ��Ӧ�Ŀγ�'
    for t in cp._teacher_cid_dict:
        print 'TEACHER: %s' % t
        print cp._teacher_cid_dict[t]