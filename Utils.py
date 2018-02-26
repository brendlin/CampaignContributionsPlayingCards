
# pdflatex
def pdflatex(directory,file) :
    import subprocess
    cmd = 'pdflatex -halt-on-error %s'%(file)
    #print 'cd %s\n%s\ncd -'%(directory,cmd)
    p = subprocess.Popen(cmd.split(' '),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,cwd=directory)
    stdout, stderr = p.communicate()
    if 'Fatal error occurred' in stdout :
        print stdout
    return

# Get first name
def GetFirstName(name) :
    #print 'Getting firstname for \"%s\"'%(name)
    if '_' in name :
        firstname = name.split('_')[0]
    if ' ' in name :
        firstname = name.split(' ')[0]
    return firstname

def GetMiddleInit(name) :
    return name

def GetLastName(name) :
    tmp_name = name
    tmp_name = tmp_name.replace('_Jr','')
    #print 'Getting lastname for %s'%(name)
    if '_' in tmp_name :
        lastname = tmp_name.split('_')[-1]
    if ' ' in tmp_name :
        lastname = tmp_name.split(' ')[-1]
    return lastname

nicknames = {'Bernie':'Bernard' ,
             'Ben'   :'Benjamin',
             'Bill'  :'William' ,
             'Bobby' :'Robert'  ,
             'Bob'   :'Robert'  ,
             'Charlie':'Charles',
             'Chris' :'Christopher',
             'Dave'  :'David'   ,
             'Dan'   :'Daniel'  ,
             'Dick'  :'Richard' ,
             'Don'   :'Donald'  ,
             'Ed'    :'Edward'  ,
             'Hal'   :'Harold'  ,
             'Hank'  :'Henry'   ,
             'Pat'   :'Patrick' ,
             'Jan'   :'Janice'  ,
             'Jim'   :'James'   ,
             'Pete'  :'Peter'   ,
             'Rick'  :'Richard' ,
             'Rob'   :'Robert'  ,
             'Steven':'Steve'   ,
             'Steve' :['Stevan','Stephen'],
             'Mike'  :'Michael' ,
             'Ted'   :'Theodore',
             'Tim'   :'Timothy' ,
             'Tom'   :'Thomas'  ,
             'Brad'  :'Bradley' ,
             }

nicknames2 = {'Steve':'Stephen' ,
              }

# Connect the photo
def FindPhoto(name,dir) :
    firstname = GetFirstName(name)
    lastname  = GetLastName(name)
    import os
    for i in os.listdir(dir) :
        extension = i.split('.')[-1]
        i_name = '.'.join(i.split('.')[:-1])

        if not i_name :
            continue

        i_firstname = GetFirstName(i_name)
        i_lastname  = GetLastName(i_name)
        #print name,i_name

        if name == i_name :
            #print 'Found it!'
            return i_name

        if (i_firstname == firstname) and (i_lastname == lastname) :
            return i_name

        if firstname in nicknames.keys() :
            tmp_firstnames = nicknames[firstname]

            # convert to list
            if type(tmp_firstnames) == type('') :
                tmp_firstnames = [tmp_firstnames]

            # cycle through nicknames
            for tmp_firstname in tmp_firstnames :
                if (i_firstname == tmp_firstname) and (i_lastname == lastname) :
                    return i_name

    print 'could not find %s'%(name)
    return ''
