import os, time

#Go into home directory of user
os.chdir(os.path.expanduser('~'))

#Create a new folder
os.mkdir('os_lab_0')

#Change the current working directory to created folder
os.chdir('os_lab_0')

#Create new two .txt files and one .py file
open('a.txt', 'x').close()
open('b.txt', 'x').close()
open('c.py', 'x').close()

#Print last modified date of each file in the directory
for i in os.listdir():
    print("Last modified date of", i, ":", time.ctime(os.path.getmtime(i)))

#Print only .txt files
for f in os.listdir():
    if f.endswith('.txt'):
        print(os.path.join('', f))