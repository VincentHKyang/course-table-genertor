#!/usr/bin/python

import re
from config import *
from util import *
from course import Course
from coursetable import CourseTable
from reader import Reader


class Generator:
    def __init__(self, grades):
        self.grades = grades
        self.total_grade = len(grades)

    def pretty_print_all_grades(self):
        for g in self.grades:
            print g.pretty_grade_course_table()

    def set_next_course(self, which_grade, which_is_next, start_time=None):
        if start_time == None:
            for i in range(4):
                for j in range(5):
                    new_time = [i, j]
                    self.generate(which_grade, which_is_next, new_time)
        else:
            self.generate(which_grade, which_is_next, start_time)
        
    def set_next_grade(self, which_is_next, which_course=None, start_time=None):
        if start_time == None:
            for i in range(4):
                for j in range(5):
                    new_time = [i, j]
                    self.generate(which_is_next, 0, new_time)
        else:
            self.generate(which_is_next, which_course, start_time)

    # int * int * int * int => boolean
    def generate(self, which_grade, which_course, start_time): #return boolean
        grade = self.grades[which_grade]
        total_course = len(grade.courses)
        set_p = False

        # try to set couse at (i, j)
        print "[try] to set course %s to %s" % (grade.courses[which_course].name, start_time)
        if grade.courses[which_course].need_allocate_p(): # pre-allocatd
            print "pre allocated one!"
        else:
            set_p = grade.set_course(which_course, start_time)
            if not set_p:  #fail to set course in the table
                print "[failed] to set course %s to %s" % (grade.courses[which_course].name, start_time)
                return False
            else:
                print "[successed] to set course %s to %s" % (grade.courses[which_course].name, start_time)

        if which_course == total_course - 1 and which_grade == self.total_grade - 1: # successfully put all courses in all grades
            #get all course table, return True
            print "get final result: "
            self.pretty_print_all_grades()
            if set_p:
                print "[unset] course %s to %s" % (grade.courses[which_course].name, start_time)
                grade.unset_course(which_course, start_time) #before going back, unset
            return True
        # else: not all courses are allocated
        elif which_course == total_course -1: # successfully put all courses in one grade
            print "[try] to generate next grade: %s" % self.grades[which_grade + 1].name
            self.set_next_grade(which_grade + 1)
        else:
            print "[try] to generate next course: %s" % grade.courses[which_course+1].name
            self.set_next_course(which_grade, which_course + 1)

        if set_p:
            print "[unset] course %s to %s" % (grade.courses[which_course].name, start_time)
            grade.unset_course(which_course, start_time) #before going back, unset
        return False
        
    def start(self):

        for i in range(4):
            for j in range(5):
                start_time = [i, j]
                self.generate(0, 0, start_time)

if __name__ == '__main__':

    courses = Reader('test.csv').get_courses()
    grades = get_all_grades_info(courses)
    
#   for g in grades:
#       g.pretty_grade_course_table()
#       print g
#   exit(0)

    gen = Generator(grades)
    gen.start()
    for g in grades:
        g.pretty_grade_course_table()