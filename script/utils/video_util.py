import os
import requests
from multiprocessing import Process
from moviepy.editor import concatenate_videoclips, VideoFileClip


def split_process_download(headers, direction, process_num, url_list, file_list, out_file):
    """
        多线程下载视频，并合并为一个视频

        Parameters
        -----------
        headers
            请求头
        direction
            下载目录
        process_num
            线程数量
        url_list
          下载url列表
        file_list
          文件名称列表
      out_file
          输出文件名称
    """
    if not os.path.exists(direction):
        os.makedirs(direction)
    if len(url_list) == len(file_list):
        process_list = []
        piece_size = len(url_list) // process_num
        if len(url_list) % process_num > 0:
            piece_size = piece_size + 1
        for i in range(process_num):
            if i == process_num - 1:
                temp_url_list = url_list[i * piece_size:]
                temp_file_list = file_list[i * piece_size:]
            else:
                temp_url_list = url_list[i * piece_size:(i + 1) * piece_size]
                temp_file_list = file_list[i * piece_size:(i + 1) * piece_size]
            temp_process = Process(target=batch_download, args=(headers, direction, temp_url_list, temp_file_list))
            temp_process.start()
            process_list.append(temp_process)
        for item in process_list:
            if item.is_alive():
                item.join()
        concat_video(direction, file_list, out_file)
    else:
        print("\033[31;48m 文件数量与url数量不一致 \033[0m")


def batch_download(headers, direction, url_list, file_list):
    """
        多个文件批量下载

        Parameters
        -----------

        headers
            请求头

        direction
            下载目录

        url_list
          下载url列表

        file_list
          文件名称列表
    """
    number = len(url_list)
    for i in range(number):
        response = requests.get(url_list[i], headers=headers)
        f = open(direction + "/" + file_list[i], "wb")
        f.write(response.content)
        f.close()


def concat_video(direction, file_list, out_file):
    """
        本地合并多个视频为一个（m3u8或其他需要被合并的视频）

        Parameters
        -----------

        direction
          合并文件的目录

        file_list
          需要合并文件的文件名（包含文件格式）列表

        out_file
          输出文件名称
    """
    concat_file_list = []
    for item in file_list:
        concat_file_list.append(VideoFileClip(direction + "/" + item))
    final_clip = concatenate_videoclips(concat_file_list, method='compose')
    final_clip.write_videofile(direction + "/" + out_file)
