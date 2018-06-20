from jira import JIRA
from pprint import pprint
import csv
import base64
import xlsxwriter
from datetime import datetime

search_list = []
options = {'server': '<SERVER>'}
#Example: https://jira.atlassian.com
username = '<USERNAME>'
password = '<PASSWORD>'
#Enter your jira credentials above

def jira_search():
    jira_search = ["<LIST OF JQL JIRA SEARCHES SEPERATED BY COMMA>"]
    return jira_search

def search_for_search_list():
    #Connect to jira server and pull search results into a list    
    jira = JIRA(options, basic_auth=(username, password)) 
    value = 0
    
    for search in jira_search():
        #Create framework, list inside list (maybe think about dictonaries)
        search_list.append([])
        
	#Create JIRA query
        search_query = ('{}'.format(search))       
        search_results=jira.search_issues(search_query,maxResults=200)
        print('Searching: {}'.format(search))
        
		#Searching and formating results. return list of results
        for issue in search_results:
            url =(options['server']+'/browse/'+str(issue)) 

            #Changing created time to timevalue
            date = issue.fields.created
            date = date[:-18]
            updated_date = datetime.strptime(date, '%Y-%m-%d')
            
			#Grabbing estimate time and time spent 
            if issue.fields.timeoriginalestimate != None:
                original_seconds = issue.fields.timeoriginalestimate
                m, s = divmod(original_seconds, 60)
                original_time, m = divmod(m, 60)
                if original_time == 0:
                    original_time = ""   
            else:
                original_time = ""
            if issue.fields.timespent != None:
                spent_seconds= issue.fields.timespent
                m, s = divmod(spent_seconds, 60)
                spent_time, m = divmod(m, 60)
                if spent_time == 0:
                    spent_time = ""
            else:
                spent_time = ""
                
           #Taking resulting information and storing in list. Currently this list includes the issue key, date created, original estimate of time, spent time, summary fields, status,priority(custom field), reporters name, assignees name, and url to ticket
            if str(issue.fields.issuetype) in ('Change','Action Item','Dev Task','New Feature', 'Sub-task','Task','Story'):  
                search_list[value].append([str(issue),updated_date,original_time,spent_time,str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),'None',str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),url])
            else:
                search_list[value].append([str(issue),updated_date,original_time,spent_time,str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),str(issue.fields.customfield_12304),str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),url])
        value +=1
    
    return search_list
              

if __name__== "__main__":
    search_for_search_list()
