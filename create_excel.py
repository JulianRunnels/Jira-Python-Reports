#!/usr/bin/python
import xlsxwriter
import links
import sprints
import sys

def write_to_excel(modules):
    #Function to write search results to an excel sheet
    #usage: python create_excel "Sprints Links"

    #Create a workbook and add a worksheet
    workbook = xlsxwriter.Workbook("<LOCATION TO SAVE>")

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})
    
    #start from the first cell below the headers
    row = 0
    col = 0
    value = 0

    
    print("Attempting to create data tables for: {}".format(modules))
    modules = modules.split()
    
    #Create seperate worksheets for different types of data
    for x in modules:
        print("\nSearching: {}".format(x.upper()))
        #Creating specific formating for each of the 2 previous modules created
        if x.lower() == 'sprints':
            search_list = sprints.jira_search()
            value = 0
            row = 0
            col = 0
            worksheet = workbook.add_worksheet('Sprints')
            search_list_sprints = sprints.search_for_search_list()
            for x in range(len(search_list)):
                #Create a new table for each unique search
                search_amount_sprints = len(search_list_sprints[value])+2
                #Leave room for title and table headers
                worksheet.write(row,0, search_list[x],bold)
                #Note: if you changed what values you pulled in the info modules, must change the headers and the number 11 above must match the ending amount of headers
                worksheet.add_table(row+1,0,row+search_amount_sprints,11,{'data' : search_list_sprints[value],
                                                            'style': 'Table Style Medium 2',
                                                            'columns': [{'header': 'Issue'},
                                                                {'header': 'Created'},
                                                                {'header': 'Orginal Estimate'},
                                                                {'header': 'Time Spent'},
                                                                {'header': 'Issue Type'},
                                                                {'header': 'Summary'},
                                                                {'header': 'Status'},
                                                                {'header': 'Severity'},
                                                                {'header': 'Priority'},
                                                                {'header': 'Reporter'},
                                                                {'header': 'Assignee'},
                                                                {'header': 'URL'}]})
                format2 = workbook.add_format({'num_format': 'mm/dd/yy'})
                #Little column formatting
                worksheet.set_column('A:A',15)
                worksheet.set_column('B:B',10,format2)
                worksheet.set_column('C:C',5)
                worksheet.set_column('D:D',5)
                worksheet.set_column('E:E',12)
                worksheet.set_column('F:F',20)
                row += search_amount_sprints+1
                value +=1
        elif x.lower() == 'links':
            search_list = links.jira_search()
            #shows issues that are linked to the main issues in the Sprints
            value = 0
            row = 0
            col = 0
            worksheet = workbook.add_worksheet('Links')
            search_list_links = links.search_for_links()
            for x in range(len(search_list)):
                search_amount_links = len(search_list_links[value])+2
                #Leave room for title and table headeers
                worksheet.write(row,0, search_list[x],bold)
                worksheet.add_table(row+1,0,row+search_amount_links,10,{'data' : search_list_links[value],
                                                    'style': 'Table Style Medium 2',
						    #Note: if you changed what values you pulled in the info modules, must change the headers and the number 11 above must match the ending amount of headers
                                                    'columns': [{'header': 'Issue'},
                                                                {'header': 'Links'},
                                                                {'header': 'Created'},
                                                                {'header': 'Issue Type'},
                                                                {'header': 'Summary'},
                                                                {'header': 'Status'},
                                                                {'header': 'Severity'},
                                                                {'header': 'Priority'},
                                                                {'header': 'Reporter'},
                                                                {'header': 'Assignee'},
                                                                {'header': 'URL'}]})
                format2 = workbook.add_format({'num_format': 'mm/dd/yy'})
                #Little column formatting
                worksheet.set_column('A:A',20)
                worksheet.set_column('B:B',20)
                worksheet.set_column('C:C',10,format2)
                worksheet.set_column('D:D',10)
                worksheet.set_column('E:E',15)
                worksheet.set_column('F:F',12)
                row += search_amount_links+1
                value +=1
        else:
            print('There are no more values to add')
            break
    workbook.close()

if __name__ == '__main__':
    write_to_excel(sys.argv[1])
