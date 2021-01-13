# 1) Load the files
# 2) Correct the files
# Let's try with an example

import sys
import io
import os
import pandas as pd

def get_all_students(directory):
    # get all the students directories names
    return next(os.walk(directory))[1]

def arange_in_dataframe(marks, students_directories_names, questions):
    result = pd.DataFrame(marks, columns=questions)
    return result

def question_correction(file_path, correct_answer):
    # We save the old stdout to switch back after saving the print value
    old_stdout = sys.stdout
    # We switch to the new stdout so we can save the print value
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    
    with open(file_path) as infile:
        exec(infile.read())
    # We save the print value without the last character because it is \n
    answer = new_stdout.getvalue()[:-1]
    # We switch back to the original stdout
    sys.stdout = old_stdout
    
    # Return True if the answer is correct and False otherwise
    mark = answer == correct_answer
    
    return mark

def all_questions_correction(directory_path, questions, correct_answers):
    marks = []
    
    # Iterate through all files of the student and correct each one
    for i in range(len(questions)):
        marks.append(question_correction(str(directory_path + '\\' + questions[i] + '.py'), correct_answers[i]))
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
        student_dir = str(directory + '\\' + student)
        # compute the marks and append them
        student_mark = all_questions_correction(student_dir, questions, correct_answers)
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
correct_answers = ['*-+', '*-+', '*-+', '*-+', '*-+', '*-+', '*-+', '*-+']

# Test the function question_correction()
#print(question_correction('student_1\\question_a.py', exercice_1_correct_answer))

# Test the function all_questions_correction()
#print(all_questions_correction('submissions\\student_1', questions, correct_answers))

# Test the function all_students_correction()
marks = all_students_correction('submissions', questions, correct_answers)