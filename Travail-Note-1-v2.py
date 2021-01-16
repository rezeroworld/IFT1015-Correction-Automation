# The goal of this script is to provide an alternative solution to correction automation,
# the approach in the first py file forces the students to have a different script for each question
# whereas this one provides a ready template that just need to be filled by the students, the structure
# of the submissions is present in the sumbissions v2 folder

import os
import pandas as pd

def get_all_students(directory):
    # get all the students directories names
    return next(os.walk(directory))[1]

def arange_in_dataframe(marks, students_directories_names, questions):
    result = pd.DataFrame(marks, columns=questions)
    return result

def question_correction(student_directory_path, question, correct_answer):
    # import the solution of the student
    module = __import__(str(student_directory_path + '.solution'), fromlist=['solution'])
    
    # get the student answer
    if question == 'question_a':
        student_answer = getattr(module, 'question_a')()
    elif question == 'question_b':
        student_answer = getattr(module, 'question_b')()
    elif question == 'question_c':
        student_answer = getattr(module, 'question_c')()
    elif question == 'question_d':
        student_answer = getattr(module, 'question_d')()
    elif question == 'question_e':
        student_answer = getattr(module, 'question_e')()
    elif question == 'question_f':
        student_answer = getattr(module, 'question_f')()
    elif question == 'question_g':
        student_answer = getattr(module, 'question_g')()
    elif question == 'question_h':
        student_answer = getattr(module, 'question_h')()
            
    # See if the students answer is a correct answer
    mark = student_answer in correct_answer
    
    # return True is he has the correct answer and Fasle otherwise
    return mark

def student_correction(student_directory_path, questions, correct_answers):   
    marks = []
    
    # Iterate through all the questions and correct each question
    for i in range(len(questions)):
        # compute the mark of the student
        mark = question_correction(student_directory_path, questions[i], correct_answers[i])
        # append the mark to the list of marks
        marks.append(mark)
    return marks

def all_students_correction(directory, questions, correct_answers):
    # get all the students
    students_directories_names = get_all_students(directory)
    marks = []
    
    # add a column Student and a column Total grade, and for each student compute marks for all questions
    columns = questions.copy()
    columns.insert(0, 'Students')
    columns.append('Total grade')
    for student in students_directories_names:
        # prepare the student directory
        student_directory_path = str(directory + '.' + student)
        # compute the marks and append them
        student_mark = student_correction(student_directory_path, questions, correct_answers)
        student_grade = sum(student_mark)
        student_mark.append(student_grade)
        marks.append(student_mark)
    
    # add the names of the students to the list
    for i in range(len(marks)):
        marks[i].insert(0, students_directories_names[i])
        
    # Finally we put everything in a dataframe, question columns are booleans indicating if the student has done
    # the question right and the final column is the total grade (it considers the values True as ones and
    # add them together).
    marks = arange_in_dataframe(marks, students_directories_names, columns)
    return marks
        
##############################################################################

questions = ['question_a', 'question_b', 'question_c', 'question_d', 'question_e', 'question_f', 'question_g', 'question_h']
correct_answers = [['*-+'], ['+*-/'], [76], [100111], [11],['8-(5-3)-2*(1+2)'], ['(4-1)*9-5'], ['15*7-5-8','15*7-8-5']]

# Test the function all_students_correction()
marks = all_students_correction('submissionsV2', questions, correct_answers)

print(marks)