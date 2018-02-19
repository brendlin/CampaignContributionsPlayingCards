#!/usr/bin/env python
import subprocess
import os
from datetime import datetime
import csv
import Utils

#-------------------------------------------------------------------------
def main(options,args) :

    skipped = []

    for index,i in enumerate(open('OpenSecretsIDs.csv').readlines()) :
        i = i.replace('\n','')
        name = i.split(',')[1]
        print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
        print name

#         if index == 1 :
#             break

        if '#' in i :
            continue

        os.system('cp PoliticsTableTemplate.tex PoliticsTableTemplate_tmp.tex')

        data = dict()
        data['contributors'] = []
        data['industries'] = []

        filename_contributors = 'data/%s_%s_contributors.csv'%(name,options.cycle)
        filename_industries   = 'data/%s_%s_industries.csv'%(name,options.cycle)

        if not os.path.exists(filename_contributors) :
            print 'Warning:',filename_contributors,'does not exist. Skipping.'
            skipped.append(name)
            continue
        if not os.path.exists(filename_industries) :
            print 'Warning:',filename_industries,'does not exist. Skipping.'
            skipped.append(name)
            continue

        # Get info for "Data from DATE"
        the_date   = datetime.fromtimestamp(os.path.getmtime(filename_contributors))
        the_date_2 = datetime.fromtimestamp(os.path.getmtime(filename_industries  ))
        if (the_date_2 - the_date).total_seconds()/3600. > 5 :
            if the_date.strftime('%b %d, %Y') != the_date_2.strftime('%b %d, %Y') :
                print 'Error! Ambiguous date:'
                print '---',filename_contributors,the_date
                print '---',filename_industries,the_date_2
                print '%2.2f hours'%((the_date_2 - the_date).total_seconds()/3600.)
                return
        os.system('sed -i \'\' "s/DATE/%s/g" PoliticsTableTemplate_tmp.tex'%(the_date.strftime('%b %d, %Y')))

        # Sed in the name
        firstname = name.split('_')[0]
        lastname  = ' '.join(name.split('_')[1:]).upper()
        os.system('sed -i \'\' "s/Barbara/%s/g" PoliticsTableTemplate_tmp.tex'%(firstname))
        os.system('sed -i \'\' "s/BARABARA/%s/g" PoliticsTableTemplate_tmp.tex'%(lastname))

        for c_f,the_file in enumerate([filename_contributors,filename_industries]) :
            for jindex,j in enumerate(open(the_file).readlines()) :
                if jindex == 0 :
                    continue
                if jindex == 11 :
                    break

                # Returns a list. Basically to avoid commas inside names of things
                j = list(csv.reader([j]))[0]

                if c_f == 0 :
                    data_i,sed_item_0,sed_item_1 = 'contributors','CONTRIBUTOR','C'
                    data[data_i].append(dict())
                    data[data_i][-1]['name'] = j[4]
                    data[data_i][-1]['total'] = j[5]
                    data[data_i][-1]['pac'] = j[6]
                    data[data_i][-1]['indiv'] = j[7]

                else :
                    data_i,sed_item_0,sed_item_1 = 'industries','SECTOR','S'
                    data[data_i].append(dict())
                    data[data_i][-1]['name'] = j[5]
                    data[data_i][-1]['total'] = j[1]
                    data[data_i][-1]['pac'] = j[3]
                    data[data_i][-1]['indiv'] = j[2]

                cname = data[data_i][-1]['name']
                total = data[data_i][-1]['total']
                pac   = data[data_i][-1]['pac']
                indiv = data[data_i][-1]['indiv']

                cname = cname.replace('/','\/')
                cname = cname.replace('&','\\\\\\&')
                cname = cname.replace('\'','APOSTROPHE')

                if len(cname.replace('\\','')) > 30 :
                    cname = cname.replace('American','Am.')
                    cname = cname.replace('America','Am.')
                    cname = cname.replace('National','NatAPOSTROPHEl')

                print cname

                os.system("sed -i \'\' 's/%s%d/%s/g'           PoliticsTableTemplate_tmp.tex"%(sed_item_0,jindex-1,cname))
                os.system("sed -i \'\' 's/%sPAC%d/%s/g'        PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,pac))
                os.system("sed -i \'\' 's/%sINDIV%d/%s/g'      PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,indiv))
                os.system("sed -i \'\' 's/%sTOT%d/%s/g'        PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,total))
                os.system("sed -i \'\' \"s/APOSTROPHE/\'/g\"   PoliticsTableTemplate_tmp.tex")

        Utils.pdflatex('.','PoliticsTableTemplate_tmp.tex')
        Utils.pdflatex('.','PoliticsCombineLayers.tex')
        os.system('mv PoliticsCombineLayers.pdf output/%s.pdf'%(name))
        #subprocess.Popen(['pdflatex','PoliticsTableTemplate_tmp.tex'],stdout=subprocess.PIPE)

    print 'Skipped:'
    for sk in skipped :
        print ' -',sk

    print 'done'
    return

#-----------------------------------------------
if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--cycle',type='string',default='2018',dest='cycle',help='Election cycle')
    options,args = p.parse_args()

    main(options,args)
