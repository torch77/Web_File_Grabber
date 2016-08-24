# Script to automatically download all files of the same file extension from a website

import requests
import re
from bs4 import BeautifulSoup

# do something about http:// in url
# make chunk size a parameter

# function to retrieve all files of specified file extension
def get_files(url, file_ext):

    # get website content to find files
    bs_obj = get_soup(url)
    print("getting links")
    # get all links and iterate through them
    for link in bs_obj.find_all("a", href = True):
        # if file ends with correct extension
        if link['href'].endswith(file_ext):
            file_url = link.attrs['href']
            print(file_url)
            # http://stackoverflow.com/questions/29827479/beautifulsoup-download-all-zip-files-from-google-patent-search
            # set name to file name from url
            outfname = file_url.split('/')[-1]
            # open requests with path
            r = requests.get(file_url, stream=True)
            if (r.status_code == requests.codes.ok):
                fsize = int(r.headers['content-length'])
                print('Downloading %s (%sMb)' % (outfname, fsize / (1024*1024)))
                with open(outfname, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=(1024*1024*100)):  # chuck size can be larger
                        if chunk:  # ignore keep-alive requests
                            fd.write(chunk)
                    fd.close()
            break

# function to create bs4 object
def get_soup(url):
    # get website
    resp = requests.get("http://"+url)

    # check status and return if ok, else error
    if resp.status_code == 200:
        bs_obj = BeautifulSoup(resp.text, "xml")
        return bs_obj
    else:
        print("Website status not ok")
        resp.raise_for_status()

# function to get file name and website
def get_input():
    # take file extension as input
    print("This script will download all files with the file extension you enter from the website you specifiy.")
    file_ext = input("Please enter the file extension, a . followed by an alphanumeric string,"
                     " that you would like to download:")
    file_ext = file_ext.lower()
    file_ext = file_ext.strip()
    # check that file has a period followed by an alphanumeric string. This should handle all real cases, if something
    # weirder we want to reject any way
    ext_pattern = re.compile("^\.[a-z0-9]+$")
    # flag for input loop
    input_ok = False
    while input_ok == False:
        if ext_pattern.match(file_ext):
            print("File Extension " + file_ext + " Valid")
            input_ok = True
        else:
            file_ext = input("Please enter an extension which is only a . followed by an alphanumeric string:")
            file_ext = file_ext.lower()
            file_ext = file_ext.strip()

    print("Right now we are only allowed to access sites with a .com, .org, .edu., .net, .info, .gov TLD.")
    site_url = input('Please enter the website to download from starting with the "www":')
    site_url = site_url.lower()
    site_url = site_url.strip()
    site_pattern = re.compile("^www\.[\da-z\.-]+\.(com|org|edu|net|info|gov)([/\w \.-]*)*/?$") # \d = digit, \w = word char
    # flag for input loop
    input_ok = False
    while input_ok == False:
        if site_pattern.match(site_url):
            print("Website " + site_url + " Valid")
            input_ok = True
        else:
            site_url = input("Please enter a valid website starting with www. and ending with a valid TLD:")
            site_url = site_url.lower()
            site_url = site_url.strip()

    return site_url, file_ext

def main():

    url, file_ext = get_input()
    get_files(url, file_ext)

main()
