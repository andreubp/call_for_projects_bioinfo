import os
import pandas as pd
import pdfkit
import shutil
import re

def generate_pdf(project, options):
    """
    To geneerate the PDF for eachg project. Create an html and generate the pdf
    """

    subti_comments = "Comments:"
    subti_ref = "References:"

    # For a nan's line we correct it.
    for i in project:
        if pd.isna(project[i]):
            project[i] = ' '
            if(i == "References"):
                subti_ref = " "
            if(i == "Additional comments"):
                subti_comments = " "
    #we pick up the template
    template = open("template/template2.html", "r")
    text_template = template.read().format(get_Adreça_electrònica=project.get("Adreça electrònica.1"),
                                           get_Supervisores_name=project.get("Supervisor's name"),
                                           get_Group=project.get("Group"),
                                           get_Institution=project.get("Institution"),
                                           get_Website=project.get("Website"),
                                           get_Field_of_Study=project.get("Field of Study"),
                                           get_Project_Title=project.get("Project's Title"),
                                           get_Summary=project.get("Summary"),
                                           get_References=project.get("References"),
                                           get_Skills_required=project.get("Skills required"),
                                           get_Keywords=project.get("Keywords"),
                                           get_Funding=project.get("Funding"),
                                           get_Continuity_with_PhD=project.get("Continuity with PhD"),
                                           get_Additional_comments=project.get("Additional comments"),
                                           subtitle_Additional_comments = subti_comments,
                                           subtitle_References = subti_ref)
    identifier = project.get("Marca de temps")
    identifier = re.sub(r"[\/:\s]", "", identifier)

    namePdf = project.get("Supervisor's name").replace(" ", "")+"-"+str(identifier)+".pdf"
    pathSave = ("projects/"+project.get("Field of Study")+"/"+namePdf)
    print (pathSave)
    pdfkit.from_string(text_template, pathSave, options=options)
    print("DONE")



    return text_template

def generate_tables_html(dates, datesHTML):
    """
    Function that helps with the HTML table generation to be copied in the bioinformatic's Website

    """
    #we created the folder of the tables to save
    os.mkdir("projects/tables-html")
    #This is the id of the main folder that is taken from the page to access the projects NEED TO BE CHANGED
    idFileProtect2021 = "244861252/"
    #Once created the folders in the page they have an id (unique, may need to be changed
    idFilesWeb ={'Computational genomics':'257014152/' ,
                 'Computational systems biology': '257014987/',
                 'Pharmacoinformatics & systems pharmacology':'257015135/',
                 'Structural bioinformatics': "257015191/",
                  'Web development & bioinformatic tools': "257015195/"}

    for project in dates.to_dict('record'):
        identifier = project.get("Marca de temps")
        identifier = re.sub(r"[\/:\s]", "", identifier)
        namePdf = project.get("Supervisor's name").replace(" ", "")+"-"+str(identifier)+".pdf"
        #we build the row for the table with its respective variables so that when we make the copy and paste in the page we can visualize the pdf
        row_table = '<tr><th align="left" height="20" scope="row">'+project.get("Supervisor's name")+'</th><td align="left">'+project.get("Institution")+'</td><td align="left">'+project.get("Group")+'</td><td align="left"><a href="https://www.upf.edu/documents/4177293/'+idFilesWeb.get(project.get("Field of Study"))+namePdf+'" target="_blank">'+project.get("Project's Title")+'</a></td></tr>'
        #we add the row in its respective table
        datesHTML[project.get("Field of Study")] += row_table

    for i in datesHTML:
        name = i+"_projects.pdf"
        #we reconstruct the end of the table with their respective variables
        end = '</tbody></table><p>&nbsp;</p><p>&nbsp;</p><p style="color: rgb(53, 52, 48); font-family: Verdana, Geneva, sans-serif;"><span style="font-weight: 700;"><span style="font-size: 18px;">Find all '+i+' projects in&nbsp;<a href="https://www.upf.edu/documents/4177293/'+idFileProtect2021+name+'" style="color: rgb(200, 16, 46); text-decoration-line: underline !important; word-break: normal !important;" target="_blank">PDF</a></span></span></p><div>&nbsp;</div>'
        datesHTML[i] += end
        path = "projects/tables-html/"+i+'.html'
        f = open(path,'wb')
        dat = str(datesHTML[i])
        dat = dat.encode(encoding='UTF-8')

        f.write(dat)
        f.close()



def main(file_csv):

    form_csv = pd.read_csv(file_csv, header=0)
    ordered_form = form_csv.sort_values(by=["Field of Study"])
    dates = pd.DataFrame(ordered_form)
    fields_folders = {}
    general = ""

    #Checking existing files, and deleating them if exist.
    if os.path.isdir('projects'):
        shutil.rmtree('projects')
    if(os.path.isfile("all_proyects.pdf")):
        os.remove('all_proyects.pdf')
    os.mkdir("projects")

    datesHTML = {}

    #These are some of the settings that allow pdfkit
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    start = """<table align="center" border="0" cellspacing="0"><colgroup>
    </colgroup><colgroup></colgroup><colgroup></colgroup><colgroup></colgroup>
    <thead><tr><th align="center" height="20" scope="row"><strong>Supervisor's
    name</strong></th><th align="center" scope="col"><strong>Institution</strong></th>
    <th align="center" scope="col"><strong>Group</strong></th><th align="center"
    scope="col"><strong>Project's Title</strong></th></tr></thead><tbody>"""


    for information in dates.to_dict('record'):
        field_ofStudy = information.get("Field of Study")
        if(field_ofStudy not in fields_folders):
            #Adding the field to have it as already existing and not to create a new folder
            fields_folders.setdefault(field_ofStudy)
            datesHTML.setdefault(field_ofStudy)
            #Initializing it empty to be able to fill it later
            fields_folders[field_ofStudy] = ""
            datesHTML[field_ofStudy] = start
            os.mkdir("projects/"+field_ofStudy)
        proyect_HTML = generate_pdf(information, options)
        fields_folders[field_ofStudy] += proyect_HTML
        general +=  proyect_HTML

    #Passing the initial file (form_csv) to be able to computerize it alphabetically by the supervisor
    generate_tables_html(form_csv.sort_values(by=["Supervisor's name"]), datesHTML)

    pdfkit.from_string(general, "projects/all_proyects.pdf", options=options)

    #Creating the pdfs by field study
    for i in fields_folders:
        path = "projects/"+i+"_projects.pdf"
        pdfkit.from_string(fields_folders[i], path, options=options)
