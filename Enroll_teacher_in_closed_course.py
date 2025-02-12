# Import the Canvas class
from canvasapi import Canvas
import yaml

# Load the config file
with open('config.yaml') as data:
    canvas_config = yaml.safe_load(data)['canvas']

# Set the base URL for the Canvas API
API_URL = canvas_config['url']

# Set the access token for the Canvas API
API_KEY = canvas_config['accesstoken']

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# a list of users sis-login-id`s to be enrolled in the course. Use the format: user_list = ['uvanetid1','uvanetid2','uvanetid3']
user_list= ['']

# the course id to enroll the users in. Use the format: course_id = 12345
course_id = 12345

# print the canvas instance being worked on to check if you are working in beta/test/production
print(f"Working on Canvas instance: {API_URL}")
# get the course object
course = canvas.get_course(course_id)
# store the original course term to revert back to after the users have been enrolled
original_course_term = course.enrollment_term_id


course_updated = False
for i in user_list:
    try:
        userobj = canvas.get_user(i,'sis_login_id')
        # the {"enrollment_state": "active"} disables the invitation email to the user and enrolls the user directly, allowing the script to close the course immediately after enrolling the user
        course.enroll_user(user = userobj,enrollment = {"type": "TeacherEnrollment","enrollment_state": "active"})
        print(f'{userobj} has been added to {course}')
    except Exception as e:
        print(f'Error: {e}. Updating term and trying to add {userobj} to {course} again')  
        # update the course term to the default term
        course.update(course={'enrollment_term_id': 1})
        course_updated = True
        userobj = canvas.get_user(i,'sis_login_id')
        course.enroll_user(user = userobj,enrollment = {"type": "TeacherEnrollment","enrollment_state": "active"})
        print(f'{userobj} has been added to {course}. ')
    else:
        print(f'unexpected error: {e}')

# revert the course back to the original term if the course term was updated
if course_updated:  
    print(f'Reverting the course back to the original term')
    course.update(course={'enrollment_term_id': original_course_term})
    print(f'Course term has been reverted back to original term: {original_course_term}')