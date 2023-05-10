from canvasapi import Canvas
import yaml
import time
from concurrent.futures import ThreadPoolExecutor
import datetime
import os

# Get the current time
start_time = time.time()

# Load the config file
with open('config.yaml') as data:
    canvas_config = yaml.safe_load(data)['canvas']

# Set the base URL for the Canvas API
API_URL = canvas_config['url']

# Set the access token for the Canvas API
API_KEY = canvas_config['accesstoken']

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# Set the subaccount ID for the courses you want to update (FMG=36 SW=122 PSY=123 POW=124 CW=125)
account_id = "36"

# Get the subaccount object
account = canvas.get_account(account_id)

# Get a list of all courses in the subaccount
courses = account.get_courses()

# Initialize an empty list to store the courses that gave an error
error_list = []

# Initialize a counter for the number of courses changed
courses_changed_count = 0

list_of_settings = ['hide_distribution_graphs','hide_final_grades','hide_sections_on_course_users_page']

# print environment and subaccount 
print(f"Working on Canvas instance: {API_URL}")
print(f"Working on subaccount: {account_id}")

 

# Change the working directory to the log_files folder, this is where the log files will be stored.
# If the folder does not exist, it will be created but if the folder already exists, the log files will be stored there
# If you want to store the log files in a different location, change the path below
# Example: os.chdir("C:\\Users\\username\\Desktop\\log_files")
if not os.path.exists('log_files'):
    os.makedirs('log_files')  
os.chdir("log_files") 


# create a log file with the srcipt name and the current date and time as the file name
log_file = open(f"log_file_{os.path.basename(__file__)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w")
file_name = log_file.name
log_file.write(f"Working on Canvas instance: {API_URL} \n")
log_file.write(f"Working on subaccount: {account_id} \n")
log_file.close()



# Define a function to update the distribution graph setting for a course
def update_course_setting(course,setting):
    global courses_changed_count
    individual_course = canvas.get_course(course)
    course_settings = individual_course.get_settings()
    with open (file_name, "a") as log_file:
        try:
            if course_settings[setting] == False:
                individual_course.update_settings(setting= True)
                courses_changed_count = courses_changed_count+1
                print(f"In course {course} {setting} was changed to: True")
                # Write to log file
                log_file.write(f"In course {course} {setting} was changed to: True \n")
            elif course_settings[{setting}] == True:
                print(f"In course {course} {setting} was already set to: True ")
                # Write to log file
                log_file.write(f"In course {course} {setting} was already set to: True \n")
            else:
                print("Course settings had an unexpected value")
                # Write to log file
                log_file.write("Course settings had an unexpected value \n")
        except Exception as e:
            print(f"something went wrong for {course}",e)
            # Write to log file 
            log_file.write(f"something went wrong for {course}. Error:{e} \n")
            error_list.append(course)

# Set the number of threads to use in the ThreadPoolExecutor
NUM_THREADS = 1

# Use the ThreadPoolExecutor to update the distribution graph setting for each course concurrently
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    for course in courses:
        for setting in list_of_settings:
            executor.submit(update_course_setting, course.id,setting)


# Get the current time
end_time = time.time()
# Calculate the difference in seconds between the start and end times
time_difference_in_seconds = end_time - start_time

# Convert the time difference to a timedelta object
time_difference = datetime.timedelta(seconds=time_difference_in_seconds)

# Print the results
print(f"{courses_changed_count} courses were changed")
print(f"These courses gave an error: {error_list}")
print(f'Time to complete: {time_difference}')
