#!/usr/bin/python3
 
from jira import JIRA
from pprint import pprint
import csv
import base64
import xlsxwriter
from datetime import datetime
import sys
import sprints

search_list=[]
options = {'server': '<SERVER>'}
#Example: https://jira.atlassian.com
username = '<USERNAME>'
password = '<PASSWORD>'
#Enter your jira credentials above

def jira_search():
    jira_search = ["<LIST OF JQL JIRA SEARCHES SEPERATED BY COMMA>"]
    return jira_search

def search_for_links():
    #Connect to jira server and pull search results into a list
    jira = JIRA(options, basic_auth=(username, password))        
    value = 0
    
    for search in jira_search():
        #Create framework, list inside list (maybe think about dictonaries)
        search_list.append([])
        
        #Create JIRA query (create multiple queries that can be run from cli options)
        search_query = ('{}'.format(search))       
        search_results=jira.search_issues(search_query,maxResults=200)
        print('Searching: {}'.format(search))

        #Searching and formating results. Return list of results
        for issue in search_results:
            
            #Debugging types without severity field
            #print(issue.fields.issuetype)
            
            if issue.fields.issuelinks == []:
                normal_issue(issue,value)    
            else:

                linkedissue_value = 0
                linked_issue(issue,value)
                #Search for any issues linked to original search issues (Slow, as has to iterate over whole list and search each one)
                for link in issue.fields.issuelinks:
                    linktype = link.type
                    if hasattr(link, "outwardIssue"):
                        outwardissue = link.outwardIssue
                        outward_search = jira.search_issues('issueKey = {}'.format(outwardissue.key))
			#Add project if needed
						
                        for y in outward_search:
                            outward_linktype = (y.fields.issuelinks[0].type.outward)
                            get_outward_issue_values(y,value,outward_linktype,linkedissue_value)       
                            linkedissue_value += 1
							
                    elif hasattr(link, "inwardIssue"):
                        inwardIssue = link.inwardIssue
                        inward_search =  jira.search_issues('issueKey = {}'.format(inwardIssue.key))
			#Add Project if needed
                       
                        for t in inward_search:
                            inward_linktype = (t.fields.issuelinks[0].type.inward)
                            get_inward_issue_values(t,value,inward_linktype,linkedissue_value)
                            linkedissue_value += 1
        value+=1
    return search_list

def url(x):
    #Creating url string for each issue
    y = ("{}/browse/{}".format(options['server'],x)) 
    return str(y)

def updated_date(issue):
    #Changing created time to timevalue
    date = issue.fields.created
    date = date[:-18]
    up_date = datetime.strptime(date, '%Y-%m-%d')
    return up_date

def normal_issue(issue,value):
    #Formatting for issues with no links
    if str(issue.fields.issuetype) in ('Change','Action Item','Dev Task','New Feature', 'Sub-task','Task','Story'):  
        search_list[value].append([str(issue),"",updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),'None',str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])
    else:
        search_list[value].append([str(issue),"",updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),str(issue.fields.customfield_12304),str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])


def linked_issue(issue,value):
    #Formatting for issues with links
    if str(issue.fields.issuetype) in ('Change','Action Item','Dev Task','New Feature', 'Sub-task','Task','Story'):  
        search_list[value].append([str(issue),'Impacts Following',updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),'None',str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])
    else:
        search_list[value].append([str(issue),'Impacts Following',updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),str(issue.fields.customfield_12304),str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])

def get_inward_issue_values(issue,value,linktype,q):
    #search for issues with inward links and add to list
    if str(issue.fields.issuetype) in ('Change','Action Item','Dev Task','New Feature', 'Sub-task','Task','Story'):  
        search_list[value].append([str('    {}'.format(issue)),str(linktype),updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),'None',str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])
    else:
        search_list[value].append([str('    {}'.format(issue)),str(linktype),updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),str(issue.fields.customfield_12304),str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])

def get_outward_issue_values(issue,value,linktype,q):
    #search for issues with outward links and add to list
    if str(issue.fields.issuetype) in ('Change','Action Item','Dev Task','New Feature', 'Sub-task','Task','Story'):  
        search_list[value].append([str('    {}'.format(issue)),str(linktype),updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),'None',str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])                          
    else:
        search_list[value].append([str('    {}'.format(issue)),str(linktype),updated_date(issue),str(issue.fields.issuetype),issue.fields.summary,str(issue.fields.status),str(issue.fields.customfield_12304),str(issue.fields.priority),str(issue.fields.reporter.name),str(issue.fields.assignee),str(url(issue))])
        
    
if __name__== "__main__" :
    search_for_links()
