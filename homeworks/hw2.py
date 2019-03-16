#FATİH SARAÇOĞLU (160709001)

import os, shutil, subprocess

#Preparing of the jail environment
home_dir = os.path.expanduser('~')
os.chdir(home_dir)
os.mkdir('jail')
os.chdir('jail')

#Base directory of the chroot
chroot_path = home_dir + '/jail'

#Binaries we can use in the jail
bins = ['/bin/bash', '/bin/chmod', '/usr/bin/stat']


#Finding all dependencies of binaries
def libraries(olist):
    ldd_output = subprocess.check_output(['/usr/bin/ldd', olist]).decode().split('\n')     
    libs = []
    for eachLib in ldd_output:
        if not eachLib:
            continue
        lib = eachLib.split()
        if os.path.splitext(lib[0])[0] == 'linux-vdso.so':
            continue
        if lib[1] == '=>':
            libs.append(lib[2])
        else:
            libs.append(lib[0])
    return libs

#Making a copy of dependencies to the jail
def copy_libs(path):
    for eachApp in bins:
        for eachLib in libraries(eachApp):
            lib_dir  = os.path.dirname(eachLib)
            lib_name = os.path.basename(eachLib)
            if lib_dir.startswith('/'):
                lib_chroot_dir = os.path.join(path, lib_dir[1:])
            else:
                lib_chroot_dir = os.path.join(path, lib_dir)
            lib_chroot_location = os.path.join(lib_chroot_dir, lib_name)   
            if not os.path.exists(lib_chroot_dir):
                os.makedirs(lib_chroot_dir)
            if not os.path.exists(lib_chroot_location) or \
                    (os.path.exists(lib_chroot_location)):
                shutil.copy2(eachLib, lib_chroot_location)


#Making a copy of binaries to the jail
def copy_bins(path):
    for eachApp in bins:
        app_dir  = os.path.dirname(eachApp)
        app_name = os.path.basename(eachApp)
        if app_dir.startswith('/'):
            app_chroot_dir = os.path.join(path, app_dir[1:])
        else:
            app_chroot_dir = os.path.join(path, app_dir)
        app_chroot_location = os.path.join(app_chroot_dir, app_name)
        if not os.path.exists(app_chroot_dir):
            os.makedirs(app_chroot_dir)
        if not os.path.exists(app_chroot_location) or \
                (os.path.exists(app_chroot_location)):
            shutil.copy2(eachApp, app_chroot_location)

#Creating a script to determine whether we are in the jail or not
def test_script():
	f = open("test_script.sh", "w+")
	f.write("#!/bin/bash\n" +
	"root_inode=$(stat -c %i /);\n" +
	"if [ $root_inode -ne 2 -a $root_inode -ne 128 ]; then\n" +
	"\techo You are in the jail!\n\techo Type exit to leave the jail!\n" +
	"else\n" +
	"\techo 'You are not in the jail!'\n" +
	"fi\n" +
	"bash")
	f.close()

#Calling the functions
copy_bins(chroot_path)
copy_libs(chroot_path)
test_script()

#Creating a chroot jail
os.chroot(chroot_path)

#Giving permission to test script in order to execute
subprocess.Popen(['/bin/chmod', '+x', 'test_script.sh'], stdout=subprocess.PIPE)

#Executing the test script
subprocess.run(['./test_script.sh'])

