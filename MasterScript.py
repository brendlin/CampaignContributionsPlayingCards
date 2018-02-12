#!/usr/bin/env python
import subprocess
import os

for index,i in enumerate(open('OpenSecretsIDs.csv').readlines()) :
    i = i.replace('\n','')
    name = i.split(',')[1]

    if index == 1 :
        break

    os.system('cp PoliticsTableTemplate.tex PoliticsTableTemplate_tmp.tex')

    contributors = []

    for jindex,j in enumerate(open('data/%s.csv'%(name)).readlines()) :
        if jindex == 0 :
            continue
        if jindex == 11 :
            break

        j = j.replace('\n','')
        j = j.split(',')
        contributors.append(dict()) 
        contributors[-1]['name'] = j[4]
        contributors[-1]['total'] = j[5]
        contributors[-1]['pac'] = j[6]
        contributors[-1]['indiv'] = j[7]

        cname = contributors[-1]['name']
        total = contributors[-1]['total']
        pac   = contributors[-1]['pac']
        indiv = contributors[-1]['indiv']

        if len(cname) > 30 :
            cname = cname.replace('America','Am.')

        os.system('sed -i \'\' "s/CONTRIBUTOR%d/%s/g" PoliticsTableTemplate_tmp.tex'%(jindex-1,cname))
        os.system('sed -i \'\' "s/CPAC%d/%s/g"        PoliticsTableTemplate_tmp.tex'%(jindex-1,pac))
        os.system('sed -i \'\' "s/CINDIV%d/%s/g"      PoliticsTableTemplate_tmp.tex'%(jindex-1,indiv))
        os.system('sed -i \'\' "s/CTOT%d/%s/g"        PoliticsTableTemplate_tmp.tex'%(jindex-1,total))

    os.system('pdflatex PoliticsTableTemplate_tmp.tex')
    os.system('pdflatex PoliticsCombineLayers.tex')
    os.system('mv PoliticsCombineLayers.pdf output/%s.pdf'%(name))
    #subprocess.Popen(['pdflatex','PoliticsTableTemplate_tmp.tex'],stdout=subprocess.PIPE)

print 'done'
