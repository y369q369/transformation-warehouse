from flask import Blueprint, Response, make_response, send_file, send_from_directory

download = Blueprint('download', __name__)


@download.route('/download/<string:file>')
def file_download(file, filename):
    #     """
    #     单个小文件下载
    #     :param file: 待下载的文件(文件路径+文件名)
    #     :param filename: 下载的文件名称
    #     """
    # 写法一
    response = make_response(send_file(file, as_attachment=True))
    # 写法二
    # response = make_response(send_file(file))
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(
    #     filename.encode().decode('latin-1'))
    return response


@download.route('/download/<string:filepath>/<string:filename>')
def file_dir_download(filepath, filename):
    #     """
    #     基于文件夹路径和文件名下载，两种写法同 file_download
    #     :param filepath: 待下载的文件路径
    #     :param filename: 下载的文件名称
    #     """
    response = make_response(send_from_directory(filepath, filename, as_attachment=True))
    return response


@download.route('/download/<string:filepath>/<string:filename>')
def file_stream_download(filepath, filename):
    #     """
    #     文件流式下载
    #     :param filepath: 待下载的文件路径
    #     :param filename: 下载的文件名称
    #     """
    def send_chunk():
        # 流式读取
        store_path = filepath + filename
        with open(store_path, 'rb') as target_file:
            while True:
                chunk = target_file.read(10 * 1024)  # 每次读取10K
                if not chunk:
                    break
                yield chunk

    response = Response(send_chunk())
    response.headers['content_type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename.encode().decode('latin-1'))
    return response
