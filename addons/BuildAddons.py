import os
import md5
import glob
import zipfile
import shutil
from xml.etree import ElementTree
import Tkinter, tkFileDialog

def main():
    addons_repo = (r"D:\xbmc-korean\xbmc-korea-addons\addons\dharma" )
    addon_packager(addons_repo)
    generate_addons_xml(addons_repo)
    generate_md5_file(addons_repo)

def addon_packager(addons_repo):
    addon_path = addon_selector();
    add_version =addon_ver(addon_path)
    addon_id=os.path.basename(addon_path)
    if (not os.path.exists(os.path.join(addons_repo, addon_id))):
        os.mkdir(os.path.join(addons_repo, addon_id))
    for filename in glob.glob(os.path.join(addons_repo, addon_id, '*')) :
        os.remove( filename )

    zipper(addon_id, os.path.join(addons_repo, addon_id, addon_id + '-' + add_version + '.zip'))
    shutil.copyfile(os.path.join(addon_id, 'changelog.txt'), os.path.join(addons_repo, addon_id, 'changelog'+ '-' + add_version + '.txt'))
    shutil.copyfile(os.path.join(addon_id, 'icon.png'), os.path.join(addons_repo, addon_id, 'icon.png'))

def addon_selector():
    addons_path=os.getcwd()
    addons = os.listdir(addons_path)
    addon_num = 0
    for addon in addons:
        if ( os.path.isdir( addon ) and addon != ".svn" ):
            addon_num = addon_num +1
    addon_lists = ['']*(addon_num+1)
    print("0.Custom Addon Path")
    addon_num = 0
    for addon in addons:
        if ( os.path.isdir( addon ) and addon != ".svn" ):
            addon_num = addon_num +1
            print (str(addon_num) + '.' + addon)
            addon_lists[addon_num] = addon
    addon_selnum = raw_input("Choose an addon: ")
    if (int(addon_selnum)==0):
        root = Tkinter.Tk()
        addon_path=tkFileDialog.askdirectory(parent=root,title='Please select a directory')
        root.withdraw()
        addon_id=os.path.basename(addon_path)
    else:
        addon_id=addon_lists[int(addon_selnum)]
        addon_path=os.path.join(addons_path, addon_id)
    print "you select ", addon_id
    return addon_path

def addon_ver(addon_path):
    tree = ElementTree.parse(addon_path + "\\addon.xml")
    add_root = tree.getroot()
    add_version = add_root.attrib['version']
    return add_version

def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w')
    root_len = len(os.path.abspath(dir))+1
    for root, dirs, files in os.walk(dir):
        if ( not ".svn" in root):
            archive_root = os.path.join(dir, os.path.abspath(root)[root_len:])
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

def generate_addons_xml(addons_repo):
    addons = os.listdir(addons_repo)
    addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
    for addon in addons:
        try:
            # skip any file or .svn folder
            if ( not os.path.isdir( os.path.join(addons_repo, addon) ) or addon == ".svn" ): continue
            # create path
            addon_zfilename = glob.glob(os.path.join( addons_repo, addon, '*.zip' ))
            addon_zfile = zipfile.ZipFile(addon_zfilename[0], "r" )
            xml_lines = addon_zfile.open (addon + '/addon.xml').read().splitlines()
            # new addon
            addon_xml = ""
            # loop thru cleaning each line
            for line in xml_lines:
                # skip encoding format line
                if ( line.find( "<?xml" ) >= 0 ): continue
                # add line
                addon_xml += unicode( line.rstrip() + "\n", "utf-8" )
            # we succeeded so add to our final addons.xml text
            addons_xml += addon_xml.rstrip() + "\n\n"
        except:
            print ("skipping", addon)
    # clean and add closing tag
    addons_xml = addons_xml.strip() + u"\n</addons>\n"
    #print (addons_xml)
    open(os.path.join(addons_repo,'addons.xml'), "w" ).write(addons_xml.encode( "utf-8" ))

def generate_md5_file(addons_repo):
    # create a new md5 hash
    m = md5.new( open( "addons.xml" ).read() ).hexdigest()
    # save file
    open(os.path.join(addons_repo, 'addons.xml.md5'), "w" ).write(m)

if __name__ == '__main__':
    main()
