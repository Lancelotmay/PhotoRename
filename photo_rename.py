# -*- coding: utf-8 -*-
"""
Created on Sat May 18 21:22:05 2019

@author: Lancelot May

photo_rename
Copyright (C) 2018 Lancelot May lancelotmay@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import os, exifread
import sys
from datetime import datetime
from filehash import FileHash



def MD5_16_calc(f):
    md5hasher = FileHash('md5')
    hash_l = md5hasher.hash_file(f.name)
    return str(hash_l)[-4:]

def FileNameGen (fname):
    # Open image file for reading (binary mode)
    # Return Exif tags
    tags = exifread.process_file(f, details=False)
    try:
        date = str(tags['EXIF DateTimeOriginal'])
    except KeyError:
        return 'No EXIF info'
# Date format 
    date = date.replace(":","")
    date = date.replace(" ","_")
    try:
        model = str(tags['Image Model'])
    except KeyError:
        model = str('unknown')
    model = model.replace(" ","")
    model = model.replace("/","")
    model = model.replace("\\","")
    MD5_16_str = MD5_16_calc(f)
    NewName = date + '_'+model+'_'+MD5_16_str
    return NewName


## main function
# configurations
#CurrentDir = '.'
CurrentDir =sys.argv[1]
# Please change to the type you would like to have
PhotoFileType = set(['jpg','jpeg','arw'])
# name and patch of log file. Please change as needed
LogFileName = CurrentDir + 'log.txt'

#open log file
LogFile = open(LogFileName, 'at', encoding='utf-8')
LogFile.write('start changing name ')
LogFile.writelines(str(datetime.today()) + '\n')

for root, dirs, files in os.walk(CurrentDir, topdown=False):
    for name in files:
        fname = (os.path.join(root, name))
        fext = name.split('.')[-1].lower()
        if fext in PhotoFileType:
            f = open(fname, 'rb')
            NameGen= FileNameGen (f)
            NameFull = NameGen + '.'+fext
            NewName = (os.path.join(root, NameFull))
            f.close()
            if NameGen == 'No EXIF info':
                LogFile.writelines("ERROR " + fname + ' : ' + NameGen + '\n')
            elif os.path.isfile(NewName):
                LogFile.writelines("ERROR " + fname +" to " + NewName +':  file exist'  + '\n')
            else:
                os.rename(f.name,NewName)
                LogFile.writelines("rename " + fname +" to " + NewName + '\n')
          
              

LogFile.close()
  
      
         
