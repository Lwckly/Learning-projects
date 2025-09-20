student_scores = {
    'Harry': 88,
    'Ron': 78,
    'Hermione': 95,
    'Draco': 75,
    'Neville': 60
}
student_grades=student_scores
list=[]
for i in student_scores:
    value= int(student_scores[i])
    if value in range(91,101):
        value= "Outstanding"
    elif value in range(81,91):
        value= "Exceeds Expectations"
    elif value in range(71,81):
        value= "Acceptable"
    elif value<70:
        value="Fail"


    list.append(value)

for key,list in zip(student_scores.keys(),list):
    student_grades[key]= list
