#!/usr/bin/env python
import subprocess
import os

#-------------------------------------------------------------------------
def main(options,args) :

    for index,i in enumerate(open('OpenSecretsIDs.csv').readlines()) :
        i = i.replace('\n','')
        name = i.split(',')[1]

        if index == 1 :
            break

        os.system('cp PoliticsTableTemplate.tex PoliticsTableTemplate_tmp.tex')

        data = dict()
        data['contributors'] = []
        data['industries'] = []

        filename_contributors = 'data/%s_%s_contributors.csv'%(name,options.cycle)
        filename_industries   = 'data/%s_%s_industries.csv'%(name,options.cycle)

        for the_file in [filename_contributors,filename_industries] :
            if not os.path.exists(the_file) :
                print 'Warning:',the_file,'does not exist. Skipping.'
                continue

        for c_f,the_file in enumerate([filename_contributors,filename_industries]) :
            for jindex,j in enumerate(open(the_file).readlines()) :
                if jindex == 0 :
                    continue
                if jindex == 11 :
                    break

                j = j.replace('\n','')
                j = j.split(',')

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
                cname = cname.replace('&','and')

                if len(cname) > 30 :
                    cname = cname.replace('America','Am.')

                os.system('sed -i \'\' "s/%s%d/%s/g" PoliticsTableTemplate_tmp.tex'%(sed_item_0,jindex-1,cname))
                os.system('sed -i \'\' "s/%sPAC%d/%s/g"        PoliticsTableTemplate_tmp.tex'%(sed_item_1,jindex-1,pac))
                os.system('sed -i \'\' "s/%sINDIV%d/%s/g"      PoliticsTableTemplate_tmp.tex'%(sed_item_1,jindex-1,indiv))
                os.system('sed -i \'\' "s/%sTOT%d/%s/g"        PoliticsTableTemplate_tmp.tex'%(sed_item_1,jindex-1,total))

        os.system('pdflatex PoliticsTableTemplate_tmp.tex')
        os.system('pdflatex PoliticsCombineLayers.tex')
        os.system('mv PoliticsCombineLayers.pdf output/%s.pdf'%(name))
        #subprocess.Popen(['pdflatex','PoliticsTableTemplate_tmp.tex'],stdout=subprocess.PIPE)

    print 'done'
    return

#-----------------------------------------------
if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--cycle',type='string',default='2018',dest='cycle',help='Election cycle')
    options,args = p.parse_args()

    main(options,args)
