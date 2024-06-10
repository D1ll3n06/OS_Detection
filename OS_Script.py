# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:52:16 2023

@author: dille
"""




def fileAdd(filename, data) -> bool:
    
    try:
        with open(filename, 'a') as file:
            file.write("\n")
            file.write(data)
            file.write("\n----------------------------------------------------------------------\n")
            return True
    except Exception as e:
            print("An error occurred while writing to the file: ", e)
            return False



import subprocess as sub

def stringGenerator (change) -> str:

    try:
        command = sub.run(["powershell.exe", change], text=True, 
                                 capture_output=True)
        commandStr = command.stdout
        return commandStr

    except Exception as e:
        print("Error executing PowerShell command: ", e)
        return ""



import re

def verifyUser(user, command) -> str:
    while True:
        exact = r'\b' + user + r'\b'
        match = re.search(exact, command)
        
        if match and user:
            try:
                command = sub.run(["powershell.exe", "net user", user], text=True, capture_output=True)
                return command.stdout
            except Exception as e:
                print("Error verifying user: ", e)

        user = input("\tThe user could not be found. Enter another: ")
        print()
        




import os

def eventLog(user) -> bool:
    
    os.putenv('USER', user)

    try:
        output = sub.check_output('detection_output.bat', text=True)
        file_name = user + " - Event Log"

        if output.strip():
            with open(file_name, 'a') as file:
                file.write(output)
            return True
        else:
            print("No successful or unsuccessful login attempts found.")
            return False
    except Exception as e:
        print("Error retrieving event log: ", e)
        return False






def main ():

    commandReturn = sub.check_output('intro_screen.bat', text=True)
    output = commandReturn[0:-36]

    hostName = stringGenerator ('hostname')
    print (" Users on ", hostName[:-1])

    print ("----------------------")
    print (output)
    print ()

    print ("  Access Control List")
    print ("-----------------------")
    print ()

    commandAcl = stringGenerator ('get-acl')
    print ( commandAcl[46:] )
    

    option = 0
    iterate = True
    while iterate:
        
        
        user = input ("Which user's information would you like to see? ")
        print()
        userDetail = verifyUser(user,output)
        userInfo  = userDetail[:-37]
        print (userInfo)
        print()
        
            
        
        more = True
        while more:
            
            
            
            fileCreation = input("Would you like to add this information to a file?(yes/no) ")
            if fileCreation.lower() == 'yes':
            
                token = True
                while token:
            
                    if option == 0:
                    
                        option +=1
                        fileName = input("What would you like to call this file? ")
                        print ("The name you gave the file was '%s'"% fileName)
                        fileAdd(fileName, userInfo)
                        eventLog(user)
                        token = False
                        more = False
                    
                    else:
                        fileCreation = input("Would you like to add this to '%s' file?(yes/no) " % fileName)    
                        if fileCreation.lower() == 'no':
                            option = 0
                        else:
                            fileAdd(fileName, userInfo)
                            eventLog(user)
                            token = False
                            more = False
            
            else:
                more = False
                            
        
        again = input("Would you like to see info on another user? ").lower()
        if again == 'yes':
            print ()
            iterate = True
        else: 
                iterate = False
            
            
    

if __name__ == "__main__":
    main()
