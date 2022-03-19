from os import system
import pytest
from Professor import Professor
import System
import json


'''
#Tests if the program can handle a wrong username
def test_login(grading_system):
    username = 'thtrhg'
    password =  'fhjhjdhjdfh'
    grading_system.login(username,password)
'''

@pytest.fixture
def grading_system():
    gradingSystem = System.System()
    gradingSystem.load_data()
    return gradingSystem

@pytest.fixture
def grader(grading_system):
    grading_system.login('goggins', 'augurrox')

#1. Tests if user can login properly
def test_login(grading_system: System.System):
    username = 'akend3'
    password =  '123454321'
    grading_system.login(username,password)
    assert grading_system.usr.name == 'akend3'
    data = grading_system.load_user_db()
    assert data['akend3']['courses'] == grading_system.usr.courses
    assert data['akend3']['role'] == 'student'

#2. Checks that password is correct
def test_password(grading_system: System.System):
    assert grading_system.check_password('saab', 'boomr345')
    assert not grading_system.check_password('saab', 'BOOMR345')
    assert not grading_system.check_password('saab', ' boomr345')
    assert not grading_system.check_password('saab', 'boomr345 ')

#3. Tests if staff can change grades 
def test_grade_change(grading_system: System.System):
    grading_system.login('goggins', 'augurrox')
    data = grading_system.load_user_db()
    original_grade = data['hdjsr7']['courses']['software_engineering']['assignment1']['grade']
    if type(original_grade) is str:
        original_grade = 0
    new_grade = (original_grade + 17) % 100 #makes sure new_grade is different
    grading_system.usr.change_grade('hdjsr7', 'software_engineering', 'assignment1', new_grade)
    #grade should be updated now if it works
    data = grading_system.load_user_db()
    assert new_grade == data['hdjsr7']['courses']['software_engineering']['assignment1']['grade']
    
#4. Creating an assignment 
def test_assignment_create(grading_system: System.System):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.create_assignment('###test assignment', '4/5/20', 'software_engineering')
    data = grading_system.load_course_db()
    assert data['software_engineering']['assignments']['###test assignment']['due_date'] == '4/5/20'
    
#5. Professor adding a student to a course
def test_add_student(grading_system: System.System):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.add_student('akend3', 'software_engineering')
    data = grading_system.load_user_db()
    assert data["akend3"]["courses"]["software_engineering"] is not None

#6. Testing dropping a student from course
def test_drop_student(grading_system: System.System):
    grading_system.login('goggins', 'augurrox')
    grading_system.usr.drop_student('akend3', 'comp_sci')
    data = grading_system.load_user_db()
    assert "comp_sci" not in data['akend3']['courses']
    #making sure exceptions are handled when non-existent student is dropped
    grading_system.usr.drop_student('akend3', 'comp_sci')
    data = grading_system.load_user_db()
    assert "comp_sci" not in data['akend3']['courses']

#7. Verifying student submission for assignment
def test_submit_assignment(grading_system: System.System):
    grading_system.login('akend3', '123454321')
    grading_system.usr.submit_assignment('databases', 'assignment1', 'test test test', '3/19/22')
    data = grading_system.load_user_db()
    assert data['akend3']['courses']['databases']['assignment1']['submission'] == 'test test test'
    assert data['akend3']['courses']['databases']['assignment1']['submission_date'] == '3/19/22'

#8. Verifying that the due date check works
def test_check_ontime(grading_system: System.System):
    grading_system.login('akend3', '123454321')
    assert not grading_system.usr.check_ontime("5/20/22", '1/1/22') #should return false
    assert grading_system.usr.check_ontime('1/1/22', "5/20/22") #should return true

#9 Checks that the correct grades are returned for student
def test_check_grades(grading_system: System.System):
    grading_system.login('yted91', 'imoutofpasswordnames')
    assert grading_system.usr.check_grades('software_engineering') == [['assignment1', 43], ['assignment2', 22]]

#10 Verifies student can view all assignments and the due dates for the specified course
def test_view_assignments(grading_system: System.System):
    grading_system.login('yted91', 'imoutofpasswordnames')
    assert grading_system.usr.view_assignments('cloud_computing') == [['assignment1', '1/3/20'], ['assignment2', '2/3/20']]

# Custom Tests

#11 Verify ontime is correct after submitting assignment
def test_submit_assignment_ontime(grading_system: System.System):
    grading_system.login('akend3', '123454321')
    grading_system.usr.submit_assignment('databases', 'assignment1', 'test test test', '12/31/99')
    data = grading_system.load_user_db()
    assert data['akend3']['courses']['databases']['assignment1']['ontime'] == False
    grading_system.usr.submit_assignment('databases', 'assignment1', 'test test test', '1/1/01')
    data = grading_system.load_user_db()
    assert data['akend3']['courses']['databases']['assignment1']['ontime'] == True

#12 Verify that professor can't drop students from a class they do not teach
def test_drop_other_student(grading_system: System.System):
    grading_system.login('goggins', 'augurrox') # doesn't teach cloud_computing
    grading_system.usr.drop_student('hdjsr7', 'cloud_computing')
    data = grading_system.load_user_db()
    assert 'cloud_computing' in data['hdjsr7']['courses']

