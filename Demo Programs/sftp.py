import pysftp as sftp


def example():
    try:
        s = sftp.Connection(host='192.168.111.172', username="rkrishi", password='reliancejio@7')
        remotePath = "/home/rkrishi/Desktop/Example.txt"
        localPath = ""
        s.put(localPath, remotePath)
        s.close()
    except Exception as e:
        print(str(e))
example()
