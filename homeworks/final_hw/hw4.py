import os, shutil, threading
from time import perf_counter_ns


possible_types = ['jpg', 'mp3', 'png', 'txt']

#Creating directories for types in the possible_types array
def environment():
    for i in possible_types:
        if os.path.exists(i):
            shutil.rmtree(i)
        os.mkdir(i)

#Finding the type of each file with respect to their magic numbers 
def matcher(magic_number):
    filetypes = {"FF D8 FF E0" : "jpg",
                 "49 44 33 03" : "mp3",
                 "89 50 4E 47" : "png",
                 "78 79 7A" : "txt"}
    return filetypes.get(magic_number, None)

#Copying using just single thread
def single_thread_copying():
    for i in range(1, 150):
        try:
            file = open("files/file{0}".format(i), 'rb').read(4)
            hex_bytes = " ".join(['{:02X}'.format(byte) for byte in file])
            shutil.copy("files/file{0}".format(i), matcher(hex_bytes))
        except:
            pass


jpg_list = []
mp3_list = []
png_list = []
txt_list = []

#A dispatcher to split all files into related arrays
def split():
    for i in range(1, 150):
        try:
            file = open("files/file{0}".format(i), 'rb').read(4)
            hex_bytes = " ".join(['{:02X}'.format(byte) for byte in file])
            if matcher(hex_bytes) == "jpg":
                jpg_list.append("files/file{0}".format(i))
            elif matcher(hex_bytes) == "mp3":
                mp3_list.append("files/file{0}".format(i))
            elif matcher(hex_bytes) == "png":
                png_list.append("files/file{0}".format(i))
            elif matcher(hex_bytes) == "txt":
                txt_list.append("files/file{0}".format(i))
        except:
            pass

#Copying files in every array to associated directories
def jpg_copy():
    for i in jpg_list:
        shutil.copy(i, "jpg")
def mp3_copy():
    for i in mp3_list:
        shutil.copy(i, "mp3")
def png_copy():
    for i in png_list:
        shutil.copy(i, "png")
def txt_copy():
    for i in txt_list:
        shutil.copy(i, "txt")


#Copying using four threads (one thread for each type)
def multi_thread_copying():
    t1 = threading.Thread(target=jpg_copy)
    t2 = threading.Thread(target=mp3_copy)
    t3 = threading.Thread(target=png_copy)
    t4 = threading.Thread(target=txt_copy)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()


### Application for single-threading ###
environment()
print("The elapsed time with single-threading: ", end=' ')
start_time1 = perf_counter_ns()
single_thread_copying()
end_time1 = perf_counter_ns()
elapsed_time1 = end_time1 - start_time1
print(elapsed_time1, "ns")

### Application for multi-threading ###
environment()
split()
print("The elapsed time with multi-threading: ", end=' ')
start_time2 = perf_counter_ns()
multi_thread_copying()
end_time2 = perf_counter_ns()
elapsed_time2 = end_time2 - start_time2
print(elapsed_time2, "ns\n")

#Difference between single-threading and multi-threading
print("Using multi-threading is" , round(elapsed_time1/elapsed_time2, 3), "times faster than using single-threading!")
