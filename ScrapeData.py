import os

for i in range(0,100000) :
    url = 'https://www.opensecrets.org/members-of-congress/contributors.csv?cid=N%08d&cycle=2018'%(i)
    # print url
    os.system("wget -O 'tmp.csv' -o 'wget_log.log' '%s'"%(url))

    if os.stat("tmp.csv").st_size < 10 :
        continue

    name = 'Unknown'

    for jindex,j in enumerate(open('tmp.csv').readlines()) :
        if jindex != 1 :
            continue
        if len(j.split(',')) > 3 :
            name = j.split(',')[3].split('(')[0].rstrip().replace(' ','_')
    
    if name == 'Unknown' :
        print 'Error! Check the current tmp.csv file. Something when wrong.'
        break

    if '2017' not in ','.join(open('tmp.csv').readlines()) :
        # print 'Skipping %s due to old data.'%(name)
        continue

    name = name.replace('.','')

    print 'N%08d'%(i),name

    os.system('mv tmp.csv data/%s.csv'%(name))
