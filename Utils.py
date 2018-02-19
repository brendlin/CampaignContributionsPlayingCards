
# pdflatex
def pdflatex(directory,file) :
    import subprocess
    cmd = 'pdflatex -halt-on-error %s'%(file)
    print 'cd %s\n%s\ncd -'%(directory,cmd)
    p = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=directory)
    stdout, stderr = p.communicate()
    if 'Fatal error occurred' in stdout :
        print stdout
    return
