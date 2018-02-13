import os,sys

#-------------------------------------------------------------------------
def main(options,args) :

    if options.file :
        the_loop  = list(a.split(',')[0] for a in open(options.file).readlines())
        the_names = list(a.replace('\n','').split(',')[1] for a in open(options.file).readlines())
        print the_loop
        print the_names
    else :
        the_loop = range(0,100000)

    for index,entry in enumerate(the_loop) :

        if not options.file :
            cid = 'N%08d'%(entry)
        else :
            cid = entry

        url = 'https://www.opensecrets.org/members-of-congress/%s.csv?cid=%s&cycle=%s'%(options.type,cid,options.cycle)
        # print url
        cmd = "wget -O 'tmp.csv' -o 'wget_log.log' '%s'"%(url)
        print cmd
        os.system(cmd)

        if os.stat("tmp.csv").st_size < 10 :
            continue

        name = 'Unknown'
        for jindex,j in enumerate(open('tmp.csv').readlines()) :
            if jindex != 1 :
                continue
            if len(j.split(',')) > 3 :
                name = j.split(',')[3].split('(')[0].rstrip().replace(' ','_')

        if options.file and options.type == 'industries' :
            name = the_names[index]

        if name == 'Unknown' :
            print 'Error! Check the current tmp.csv file. Something went wrong.'
            break

        if options.cycle not in ','.join(open('tmp.csv').readlines()) :
            # print 'Skipping %s due to old data.'%(name)
            continue

        name = name.replace('.','')

        if not options.file :
            print 'N%08d'%(entry),name

        os.system('mv tmp.csv data/%s_%s_%s.csv'%(name,options.cycle,options.type))

    return

#-----------------------------------------------
if __name__ == '__main__':
    
    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--file' ,type='string',default=''    ,dest='file' ,help='Input file')
    p.add_option('--cycle',type='string',default='2018',dest='cycle',help='Election cycle')
    p.add_option('--type' ,type='string',default='contributors',dest='type',help='type (contributors or industries)')

    options,args = p.parse_args()

    if options.type != 'contributors' and options.type != 'industries' :
        print 'Error: please select --type as contributors or industries'
        sys.exit()

    if options.type == 'industries' and not options.file :
        print 'Error: when selecting --type industries one must use a previously-generated file with name-cid pairs'
        sys.exit()

    main(options,args)
