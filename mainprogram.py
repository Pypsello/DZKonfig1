
import argparse
import tarfile
from io import BytesIO
#import shutil


def ls_com(archive_path, path):
    with tarfile.open(archive_path, 'r') as tar:
        for file in tar.getmembers():
            np = file.path.strip('/').split('/')
            last = np.pop()
            if path == np:
                print(last, end=" " * 2)
        print()

def cd_com(com, path):
    parts = com.split(' ')
    path = parts[1].split("/")
    path = [i for i in path if i != ""]
    return path



def cp_com(archive_path, com, path):
    with tarfile.open(archive_path, 'r') as tar:
        np = com.split(" ")[2]
        name = com.split(' ')[1]
        bytes = tar.extractfile(name).read()
    with tarfile.open(archive_path, 'a') as tar:
        io = BytesIO()
        io.write(bytes)
        io.seek(0)
        info = tarfile.TarInfo(name=np)
        info.size = len(bytes)
        tar.addfile(tarinfo=info, fileobj=io)




def main():
    parser = argparse.ArgumentParser(description="UNIX shell emulator")
    parser.add_argument("hostname", type=str, help="Hostname for prompt")
    parser.add_argument("fs_archive", type=str, help="Path to the virtual file system archive")
    parser.add_argument("start_script", type=str, help="Path to the start script")

    args = parser.parse_args()
    print(f'{args.hostname}:-----Welcome to the shell emulator!-------')
    archive_path = args.fs_archive


    path = []
    forhistory = []

    while True:
        com = input("$ ")
        forhistory.append(com)

        if com == "ls":
            ls_com(archive_path, path)

        elif com == "exit":
            break

        elif com.startswith("cd "):
            path = cd_com(com, path)

        elif com == "history":
            print(*forhistory[:-1], sep='\n')

        elif com.startswith('cp '):
            cp_com(archive_path, com, path)

    print("Exiting emulator.")


if __name__ == "__main__":
    main()