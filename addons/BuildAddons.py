import os
import re
import sys
import md5
import glob
import zipfile
import shutil
from xml.etree import ElementTree
import Tkinter, tkFileDialog

addons_repo = (r"D:\xbmc-korean\xbmc-korea-addons\addons\dharma")
addons_path = (r"")

def main():
    addons_path = addons_path_check()
    print ("\
            ------------------------------------------------------\n \
            1. Update or generate an addon from custom path\n \
            2. Update all updated addons from current or specified path\n \
            3. Just update addons.xml\n \
           ------------------------------------------------------\n")
    menu_selnum = raw_input("Please select number : ")
    if menu_selnum == str(1):
        addon_path = addon_selector()
        addon_updater(addons_repo, addon_path)
        addons_xml_updater(addons_repo)
    elif menu_selnum == str(2):
        addons_updater(addons_repo, addons_path)
        addons_xml_updater(addons_repo)
    elif menu_selnum == str(3):
        addons_xml_updater(addons_repo)
    else:
        print ("Please select correct number !!")

def addons_path_check():
    if not os.path.exists(addons_repo):
        sys.exit("Please set Addons Repo path properly")
    try:
        if os.path.exists(addons_path):
            pass
    except:
        addons_path = os.getcwd()
        return addons_path

def addons_xml_updater(addons_repo):
    generate_addons_xml(addons_repo)
    generate_md5_file(addons_repo)
    
def addons_updater(addons_repo, addons_path):
    addons = addon_match(addons_path)
    for addon in addons:
        addon_updater(addons_repo, os.path.join(addons_path, addon))

def addon_match(addons_path):
    addons_candis = os.listdir(addons_path)
    addon_pattern = re.compile("^((metadata|skin|repository|plugin|script|screensaver|visualization|weather)(\.[\w-]+)+)")
    addon_ignore = ("repository")
    addons = []
    for addon in addons_candis:
        if os.path.isdir(os.path.join(addons_path, addon)) and not addon_ignore in addon:
            query = addon_pattern.search(addon)
            if query:
                matches = query.groups()
                if matches[0] == addon:
                    addons.append(addon)
    return addons

def addon_updater(addons_repo, addon_path):
    addon_id = os.path.basename(addon_path)
    addon_zip_num = len(glob.glob(os.path.join(addons_repo, addon_id, '*.zip')))
    if os.path.isfile(os.path.join(addon_path, 'addon.xml')):
        addon_version = addon_ver(addon_path)
        if os.path.exists(os.path.join(addons_repo, addon_id)) and addon_zip_num == 1:
            repo_addon_version = repo_add_ver(addons_repo, addon_id)
            if addon_version == repo_addon_version:
                print (addon_id + " is up to date.. version: " + addon_version)
            elif addon_version > repo_addon_version:
                print (addon_id + " is updated.. version: " + repo_addon_version + " to " + addon_version)
                print ("Updating addon package for " + addon_id + " to version: " + addon_version)
                addon_packer(addons_repo, addon_path)
            elif addon_version < repo_addon_version:
                print (addon_id + " is out dated.. version: " + addon_version)
        elif not os.path.exists(os.path.join(addons_repo, addon_id)):
            print ("\nFound new addon for " + addon_id)
            os.mkdir(os.path.join(addons_repo, addon_id))
            print ("Generating addon package for " + addon_id + " version: " + addon_version)
            addon_packer(addons_repo, addon_path)
        elif os.path.exists(os.path.join(addons_repo, addon_id)) and addon_zip_num == 0:
            print ("\nThe addon path exist, But no old package found for " + addon_id)
            print ("Copying addon package for " + addon_id + " version: " + addon_version)
            addon_packer(addons_repo, addon_path)

def repo_add_ver(addons_repo, addon):
    addon_zfilename = glob.glob(os.path.join(addons_repo, addon, '*.zip'))
    addon_zfile = zipfile.ZipFile(addon_zfilename[0], "r" )
    zip_addon_xml = addon_zfile.open(addon + '/addon.xml')
    addon_zfile.close()
    repo_addon_xml = ElementTree.parse(zip_addon_xml).getroot()
    repo_addon_version = repo_addon_xml.attrib['version']
    return repo_addon_version

def addon_packer(addons_repo, addon_path):
    addon_id = os.path.basename(addon_path)
    add_version = addon_ver(addon_path)
    for filename in glob.glob(os.path.join(addons_repo, addon_id, '*')) :
        os.remove(filename)
    addon_zipper(addon_id, os.path.join(addons_repo, addon_id, addon_id + '-' + add_version + '.zip'))
    try:
        shutil.copyfile(os.path.join(addon_id, 'changelog.txt'), os.path.join(addons_repo, addon_id, 'changelog'+ '-' + add_version + '.txt'))
    except:
        print ("Skipping changelog.txt for " + addon_id)
    try:
        shutil.copyfile(os.path.join(addon_id, 'icon.png'), os.path.join(addons_repo, addon_id, 'icon.png'))
    except:
        print ("Skipping icon.png for " + addon_id)
    try:
        shutil.copyfile(os.path.join(addon_id, 'fanart.jpg'), os.path.join(addons_repo, addon_id, 'fanart.jpg'))
    except:
        print ("Skipping fanart.jpg for " + addon_id)
    print ("Packaged " + addon_id + " is placed in the repository\n")
                       

def addon_selector():
    root = Tkinter.Tk()
    root.withdraw()
    addon_path = tkFileDialog.askdirectory(parent=root,title='Please select a directory')
    addon_id = os.path.basename(addon_path)
    print ("you select " + addon_id + "\n")
    return addon_path

def addon_ver(addon_path):
    if os.path.isfile(os.path.join(addon_path, 'addon.xml')):
        addon_tree = ElementTree.parse(os.path.join(addon_path, 'addon.xml'))
    else:
        print("addon.xml is not exist")
        return
    addon_id = os.path.basename(addon_path)
    add_root = addon_tree.getroot()
    add_version = add_root.attrib['version']
    add_id = add_root.attrib['id']
    if not add_id == addon_id:
        print ("Addon ID is not matched with addon directory name, please check !")
        return
    return add_version

def addon_zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w')
    root_len = len(os.path.abspath(dir))+1
    for root, dirs, files in os.walk(dir):
        if (not ".svn" in root):
            archive_root = os.path.join(dir, os.path.abspath(root)[root_len:])
            for f in files:
                if f != "Thumbs.db":
                    fullpath = os.path.join(root, f)
                    archive_name = os.path.join(archive_root, f)
                    zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def generate_addons_xml(addons_repo):
    addons = addon_match(addons_repo)
    addons_root = ElementTree.Element("addons")
    for addon in addons:
        try:
            addon_zfilename = glob.glob(os.path.join( addons_repo, addon, '*.zip' ))
            addon_zfile = zipfile.ZipFile(addon_zfilename[0], "r" )
            zip_addon_xml = addon_zfile.open(addon + '/addon.xml')
            addon_zfile.close()
            addon_xml = ElementTree.parse(zip_addon_xml).getroot()
            addons_root.append(addon_xml)
        except:
            print ("Problems Found. skipping", addon)
    indent(addons_root)
    addons_xml = ElementTree.ElementTree(addons_root)
    addons_xml.write(os.path.join(addons_repo,'addons.xml'), encoding="UTF-8")
    print ("\nSucessfuly generate addons.xml from current repository addons")

def generate_md5_file(addons_repo):
    try:
        # create a new md5 hash
        m = md5.new(open(os.path.join(addons_repo, "addons.xml")).read()).hexdigest()
        # save file
        open(os.path.join(addons_repo, 'addons.xml.md5'), "w" ).write(m)
        print ("Sucessfuly generate addons.xml.md5 for addons.xml")
    except:
        print ("An error occurred creating addons.xml.md5 file!\n")

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

if __name__ == '__main__':
    main()
