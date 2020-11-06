# -*- coding: utf-8 -*-
import time
import os
import multiprocessing as mp
data_lst = range(30)

def write_file():
    for data in data_lst:
        create_write_file(data)

def mp_write_file_callback():
    """
    多进程处理文件，不会丢失数据
    """
    process_pool = mp.Pool()
    for data in data_lst:
        # 当create_write_file函数执行完成之后就会调用write_all_to_file函数，并且把create_write_file函数的返回值传给write_all_to_file函数。
        process_pool.apply_async(create_write_file_callback, (data,), callback=write_all_to_file)
    process_pool.close()
    process_pool.join()

def mp_write_file():
    """
    多进程处理文件，会丢失数据
    """
    process_pool = mp.Pool()
    for data in data_lst:
        process_pool.apply_async(create_write_file, (data,))
    process_pool.close()
    process_pool.join()

def create_write_file_callback(data):
    """
    生成待写入文件数据
    """
    data_res_lst = list()
    """
    可自行添加对file的处理代码
    """
    # 做一些CPU密集型的任务时，才能体现出多进程的加速作用，否则可能效率低于单进程
    time.sleep(1)
    data_res_lst.append(data)
    return data_res_lst

def create_write_file(data):
    """
    生成待写入文件数据
    """
    # 做一些CPU密集型的任务时，才能体现出多进程的加速作用，否则可能效率低于单进程
    time.sleep(1)
    write_file_obj = open("res.txt", 'a+')
    write_file_obj.write(str(data) + "\n")
    write_file_obj.close()
    return


def write_all_to_file(data_lst):
    """
    回调函数，整合多进程返回的数据结果
    """
    write_file_obj = open("res.txt", 'a+')
    for line in data_lst:
        write_file_obj.write(str(line) + "\n")
    write_file_obj.close()


if __name__ == "__main__":
    if os.path.exists("res.txt"):
        os.remove("res.txt")

    start = time.time()
    write_file()
    end = time.time()
    print(end - start)

    start = time.time()
    mp_write_file()
    end = time.time()
    print(end - start)

    start = time.time()
    mp_write_file_callback()
    end = time.time()
    print(end - start)

