'''Search through the project folders, and convert .ui to .py'''
import os
import sys
import gflags
import subprocess

if __name__ == '__main__':
    
    project_folder = None
    
    # Parse command line arguments
    try:
        argv = gflags.FLAGS(sys.argv)
        if len(argv) != 2:
            raise gflags.FlagsError("Must specify project folder")
        project_folder = argv[1]
    except gflags.FlagsError, e:
        print 'USAGE ERROR: %s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], gflags.FLAGS)
        sys.exit(1)
    flags = gflags.FLAGS

    # Look for files to parse
    print "Checking for changed .ui files"
    print "Scanning", project_folder
    for dirpath, dirnames, filenames in os.walk(project_folder):
        for filename in filenames:
            if filename.lower().endswith('.ui'):
                ui_path = os.path.join(dirpath, filename)
                py_path = os.path.join(dirpath, filename[:-3]) + '.py'
                
                print ui_path,
                build = False
                if not os.path.exists(py_path):
                    build = True
                elif os.stat(ui_path).st_mtime > os.stat(py_path).st_mtime:
                    build = True
                    
                if not build:
                    print "(up to date)"
                    continue
                else:
                    print "(BUILDING)"
                    
                rtncode = subprocess.call(
                    [r"C:\Python27\Scripts\pyside-uic.exe",
                     ui_path,
                     '-o', py_path,
                     ],
                    stdout = sys.stdout,
                    stderr = sys.stdout)
                if rtncode != 0:
                    print "ERROR: Build of %s failed" % (ui_path)
                    sys.exit(rtncode)
                    
    print "Finished"