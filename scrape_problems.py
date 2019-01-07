import urllib.request
import os

def get_line(problem_file,data_points):
    line=problem_file.readline()
    if line=="":
        return(line)
    line_items=line.split(".,.")
    if len(line_items)!=data_points or line_items[0]=="\n" or line[0]=="#":
        line=get_line(problem_file,data_points)
    return(line)

def get_existing(problem_file,problem_list=[]):
    line=get_line(problem_file,11)
    while line:
        problem_list.append(line.split(".,.")[0])
        line=get_line(problem_file,11)
    return(problem_list)

def get_addresses():
    address_file=open("problem_list.txt","r")
    line=get_line(address_file,1)
    address_list=[]
    while line:
        if len(line[:-1])!=47:
            address_list.append(line[:-1])
        line=get_line(address_file,1)
    return(address_list)

def scrape(url):#downloads webpage passed to it and saves to temp location
    scrape_file=open("temp.txt","w")
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    f = urllib.request.urlopen(req)
    scrape_file.write(f.read().decode('utf-8'))
    scrape_file.close()
    print("Just scraped "+url)

def get_scrape_line():#find the line with all the useful data in
    scrape_file=open("temp.txt","r")
    scrape_line=scrape_file.readline()
    check=-1
    while scrape_line and check==-1:
        scrape_line=scrape_file.readline()
        check=scrape_line.find('"Method')
    return(scrape_line)

def extract_data(name,line):#takes the item to be found and extracts it
    length=len(name)
    position=line.find(name)+length+3
    search_area=line[position:(position+30)]
    search_list=search_area.split('"')
    item=search_list[0]
    return(item)

def get_hold(line):#gets hold and sorts them in start midlle and end categories
    hold_list=line.split("},{")
    middle_hold=""
    end_hold=""
    start_hold=""
    for item in hold_list:
        data_list=item.split(",")
        is_start=data_list[2].split(":")
        if is_start[1]=="true":
            start_hold+=(data_list[1].split(":"))[1][1:-1]+","
        elif (data_list[3].split(":"))[1]=="true":
            end_hold+=(data_list[1].split(":"))[1][1:-1]+","
        else:
            middle_hold+=(data_list[1].split(":"))[1][1:-1]+","
    return(start_hold+".,."+middle_hold+".,."+end_hold)
    

def extract_holds(line):#removes everything from the string except holds info and calls get_hold
    position=line.find("Moves")
    line=line[(position+9):]
    position=line.find("]")
    line=line[0:(position-1)]
    holds=get_hold(line)
    return(holds)

def get_items(line,address):#repeatedly calls extract_data for each item
    factor_list=["Method","Name",'"Grade','"Id":1,"Description','Nickname','"Holdsetup":{"Id":15,"Description',"IsBenchmar"]
    save_string=""
    for item in factor_list:
        extracted=extract_data(item,line)
        save_string+=extracted+".,."
    holds=extract_holds(line)
    #print(holds)
    save_string+=holds+"\r\n"
    save_string=address+".,."+save_string
    save_file=open("problems.txt","a")
    save_file.write(save_string)
    save_file.close()


def main():
    problem_file=open("problems.txt","r")
    existing=get_existing(problem_file)
    problem_file.close()
    #print(existing)
    addresses=get_addresses()
    #print(addresses)
    existing_number=0
    new_number=0
    for address in addresses:
        if address not in existing:
            new_number+=1
            data=scrape(address)
            line=get_scrape_line()
            get_items(line,address)
            os.remove("temp.txt")
        else:
            existing_number+=1
    print(str(existing_number)+" existing problems, "+str(new_number)+" new problems and "+str(existing_number+new_number)+" total problems")
            
main()


