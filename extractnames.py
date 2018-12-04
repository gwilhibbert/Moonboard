#this is a python file for extracting information from html
import os
import shutil

def open_file():
    count=1
    check=0
    problem_list=[]
    while check==0:
        filename=str(count)+".html"
        print("trying to open"+filename)
        try:
            filedata=open(filename,"r")
            problem_list=find_data(filedata)
            save_problems(problem_list)
            os.remove(filename)
            shutil.rmtree(str(count)+"_files")
        except:
            check=1
        count+=1

def find_data(filedata):
    line=filedata.readline()
    problem_line=""
    while line:
        test=line.find('<h3><a href="https://www.moonboard.com/Problems/View')
        if test==-1:
            line=filedata.readline()
        else:
            problem_line=line
            line=""
            filedata.close()
    if problem_line!="":
        extract=extract_data(problem_line)
        return(extract)
    filedata.close()

def extract_data(problem_line):
    check=0
    item_list=problem_line.split('"')
    problem_list=[]
    for i in item_list:
        position=i.find('https://www.moonboard.com/Problems')
        if position!=-1:
            problem_list.append(i)
    return(problem_list)

def saved_problems():
    save_file=open("problem_list.txt","r")
    saved_line=save_file.readline()
    saved_list=[]
    while saved_line:
        saved_list.append(saved_line)
        saved_line=save_file.readline()
    save_file.close()
    return(saved_list)

def save_problems(save_list):
    saved_list=saved_problems()
    save_file=open("problem_list.txt","a")
    new_probs=0
    for item in save_list:
        new_item=item+"\n"
        if new_item not in saved_list:
            save_file.write(item+"\r\n")
            new_probs+=1
    save_file.close()
    print(str(new_probs)+" new problems added from this file")

def main():
    open_file()

main()
