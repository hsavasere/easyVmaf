import concurrent.futures
import csv
import getopt
import sys

import requests


def download(link):
    file_name = link.split('/')[-1]
    r = requests.get(link, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=2048 * 2048):
            if chunk:
                f.write(chunk)
    return f'Download complete from the link : {link}'


def read_to_list(file_name):
    files = []
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

        for i in data:
            files.append(i[1])

    return files


def list_file_download(file_name):
    file_list = read_to_list(file_name)

    print("-------------- Downloading the videos from list --------------")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in file_list:
            futures.append(executor.submit(download, link=url))

        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    try:
        arguments, values = getopt.getopt(sys.argv[1:], "l:f:", ["Link", "File"])

        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-f", "--File"):
                list_file_download(currentValue)

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

