# Jira-Python-Reports
Creation of automated Jira reports using (very basic) python. Feel free to suggest improvements, this was all done through self-teaching and the current code is not very robust.

These files are used to create automatic excel reports of jira searches that can be additionally automatically emailed out.

The two information modules I have created so far are Sprints.py and Links.py

Sprints.py was used to search for all issues in a provided list of sprint seaches. However, it will work to provide results for any list of valid JQL searches. However, the resulting information that is pulled will need to be adjusted, as some of the fields pulled will not be in all JIRA setups.

Links.py takes this a step further by looking for all issues in a search and then returning those issues + any linked issues as well.

Create_excel.py is the main module that will be run to pull the information from the other modules. You run this module in cmd line with the information modules you want as arguements: python create_excel.py "Sprints Links", or python create_excel.py "Sprints".

The last module, send_mail.py is an add-on that you can implement to create automatic emails of this report. Using all 4 of these, you can set up a .bat file or .sh with task scheduler/crontab to automatically create daily reports with no input needed.
