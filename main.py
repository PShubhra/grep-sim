import termcolor
import re
import pathlib
import os


def check_command_validity(command_string):
    '''It checks if command string have grep as starting word'''
    if(command_string[0:4]=="grep"):
        return True

def doPrinting(content,i,f,lineNo):
    '''Input: content to print, initial index, final index, line_number of that
    Output: loop through content letters and color the colors if letter index is between i and f.
    '''
    print(f"{lineNo+1}: ",end="")
    for idx in range(len(content)):
        if(idx>=i and idx<f):
            print(termcolor.colored(content[idx],'red'),end="")
        else:
            print(content[idx],end="")
    print()

#Resolving the input command
    

def get_requested_pattern(command_string):
    '''This will split the input command and get the 2 last
        element as the manual'''
    commands_list = command_string.split()
    pattern = commands_list[len(commands_list)-2]
    return pattern


def get_requested_flags(command_string):
    '''This will remove any other inputs after
        and return the left list as flags list'''
    commands_list = command_string.split()
    commands_list.pop(0)
    commands_list.pop(len(commands_list)-1)
    commands_list.pop(len(commands_list)-1)
    return commands_list


def get_requested_path(command_string):
    '''Get the last item after splitting as path'''
    commands_list = command_string.split()
    return commands_list[len(commands_list)-1]
#========================================================================================================

def perform_case_sensitive_search(requested_pattern, path,options):
    '''Inputs: requested_pattern string, path of the file, flags on how you want to search
        Work: Based on options it got it will search for requested_pattern with case senstivity
        Options: 
            -w for word Only
            -n only give the count of the
            -i gives the lines that don't have the requested pattern
    '''
    with open(path,'r') as file:
        lines = file.readlines()

    print(termcolor.colored("==========================================================",'light_red'))
    print(termcolor.colored(f"Searching in file: {path}",'light_red'))
    print(termcolor.colored("==========================================================",'light_red'))
    resultsFound=0
    for line in lines:
        initialPos = line.find(requested_pattern)
        if(initialPos>=0 and "-i" not in options):
            finalPos = initialPos+len(requested_pattern)
            if("-w" in options):
                if(line[initialPos-1]==" " and (line[finalPos]==" " or line[finalPos]==".")):
                    if("-n" in options): resultsFound+=1
                    else: doPrinting(line,initialPos,finalPos,lines.index(line))
            else:
                if("-n" in options): resultsFound+=1
                else: doPrinting(line,initialPos,finalPos,lines.index(line))
        elif("-i" in options):
            if("-n" in options):
                resultsFound+=1
            else:
                doPrinting(line,-1,-1,lines.index(line))
    if("-n" in options):print(f"{resultsFound} matches found.")

#Finding the requested_pattern case insensitive

def perform_insensitive_search(requested_pattern, path,options):
    '''
    Inputs: requested_pattern string, path of the file, flags on how you want to search
    Work: Based on options it got it will search for requested_pattern with case insensitive
        It uses regex module to find match while ignoring case and get the index
        provided by span atribute of search object.
    Options: 
        -w for word Only
        -n only give the count of the
        -i gives the lines that don't have the requested pattern
'''
    with open(path,'r') as file:
        lines = file.readlines()
    
    print(termcolor.colored("==========================================================",'light_red'))
    print(termcolor.colored(f"Searching in file: {path}",'light_red'))
    print(termcolor.colored("==========================================================",'light_red'))
    resultsFound=0
    for line in lines:
        try:
            pos = re.search(requested_pattern,line,re.IGNORECASE).span()
        except AttributeError:
            pos=(-1,-1)

        if(pos[0]>=0 and "-i" not in options):
            if("-w" in options):
                if(line[pos[0]-1]==" " and (line[pos[1]]==" " or line[pos[1]]==".")):
                    if("-n" in options): resultsFound+=1
                    else: doPrinting(line,pos[0],pos[1],lines.index(line))
            else:
                if("-n" in options): resultsFound+=1
                else: doPrinting(line,pos[0],pos[1],lines.index(line))
        elif(pos[0]==-1 and "-i" in options):
            if("-n" in options):
                resultsFound+=1
            else:
                doPrinting(line,-1,-1,lines.index(line))
    if("-n" in options): print(f"{resultsFound} matches found")


def perform_deep_search(requested_pattern,flags,DIR):
    '''
    Input: requested pattern, requested flalgs, root dir to search
    Task: Create a list of all the files in the directory and sub directory and get the 
    Output: Give the output by calling respective search option according to the flags
    '''
    file_names = []
    for root,d_names,file_names in os.walk(DIR):
        for f in file_names:
            file_names.append(os.path.join(root,f))
    for file_name in file_names:
        trigger_search(requested_pattern,file_name,flags)

def trigger_search(requested_pattern, path, flags):
    if("-c" in flags):
        perform_case_sensitive_search(requested_pattern,path,tuple(flags))
    else:
        perform_insensitive_search(requested_pattern,path,tuple(flags))
#========================================================================================================
#Main Function

'''
Defaults:
1> Case Insensitive by Default( -c to make it sensitive)
2> Deep search gets the priority than multiple files search
    If any one is specified other flags will be ignored
'''
#Take command input
exit_check = False

while(exit_check!=True):

    command_string = input(": ")

    if(check_command_validity(command_string)==True):

        requested_pattern = get_requested_pattern(command_string)
        forced_options = get_requested_flags(command_string)
        destination_path = get_requested_path(command_string)

        if("-d" in forced_options):
            perform_deep_search(requested_pattern,forced_options,destination_path)
        elif("*" in destination_path and '-m' in forced_options):

            destination_path = destination_path.replace('/*',"")

            files_path_list = pathlib.Path(destination_path).glob("*")
            for file_path in files_path_list:
                try:
                    trigger_search(requested_pattern,file_path,forced_options)
                except IsADirectoryError:
                    pass
        else:
            try:
                trigger_search(requested_pattern,destination_path,forced_options)

            except IsADirectoryError:
                print("Provide path to a file")

            except FileNotFoundError:
                if('*' in destination_path):
                    print("Provide file name instead of wildcard(*)")
                else:
                    print("File not Found")

    elif(command_string=="exit"):
        exit_check = True

    else:
        print("Command not valid!")