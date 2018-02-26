#!/usr/bin/env python
import subprocess
import os
from datetime import datetime
import csv
import Utils

#-------------------------------------------------------------------------
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#-------------------------------------------------------------------------
def main(options,args) :

    skipped = []
    too_long = []

    npoliticians = file_len('OpenSecretsIDs.csv')

    for index,i in enumerate(open('OpenSecretsIDs.csv').readlines()) :
        if index == options.n :
            break

        i = i.replace('\n','')
        name = i.split(',')[1]
#         print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#         if not index%1 :
#             print 'Processing %d of %d %2.2f%%'%(index,npoliticians,index/float(npoliticians))
#         print name

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

        # Sed in the picture
        photo = 'Bernard_Sanders.jpg'
        tmp_ph = Utils.FindPhoto(name,'figures')
        if not tmp_ph :
            return
        if tmp_ph :
            photo = tmp_ph
        os.system('sed -i \'\' "s/Bernard_Sanders.jpg/%s/g" PoliticsTableTemplate_tmp.tex'%(photo))

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
                    xtmp = j[5]
                    data[data_i][-1]['name'] = xtmp[0] + xtmp[1:].lower()
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

                def toobig(nm) :
                    return len(nm.replace('\\','').replace('APOSTROPHE','#')) > 31

                if toobig(cname) : cname = cname.replace('American','Am.')
                if toobig(cname) : cname = cname.replace('America','Am.')
                if toobig(cname) : cname = cname.replace('National','NatAPOSTROPHEl')
                if toobig(cname) : cname = cname.replace('International','IntAPOSTROPHEl')
                if toobig(cname) : cname = cname.replace('Government','GovAPOSTROPHEt')
                if toobig(cname) : cname = cname.replace('Federation','Fed.')
                if toobig(cname) : cname = cname.replace('Federal','Fed.')
                if toobig(cname) : cname = cname.replace('Workers','Wrkrs')
                if toobig(cname) : cname = cname.replace('Brotherhood','Bhood')
                if toobig(cname) : cname = cname.replace('United','Utd')
                if toobig(cname) : cname = cname.replace('Union','Un.')
                if toobig(cname) : cname = cname.replace('University','Univ.')
                if toobig(cname) : cname = cname.replace('Management','Mgmt.')
                if toobig(cname) : cname = cname.replace('Massachusetts','Mass.')
                if toobig(cname) : cname = cname.replace('Texas','TX')
                if toobig(cname) : cname = cname.replace('Cooperative','Coop.')
                if toobig(cname) : cname = cname.replace('Education','Ed.')
                if toobig(cname) : cname = cname.replace('Independent','Indep.')
                if toobig(cname) : cname = cname.replace('Council','Counc.')
                if toobig(cname) : cname = cname.replace('Mechanical','Mech.')
                if toobig(cname) : cname = cname.replace(' The ',' ')
                if toobig(cname) : cname = cname.replace(' the ',' ')
                if toobig(cname) : cname = cname.replace('Academy','Acad.')
                if toobig(cname) : cname = cname.replace('South','S.')
                if toobig(cname) : cname = cname.replace('Retired','Ret.')
                if toobig(cname) : cname = cname.replace('Community','Commun.')
                if toobig(cname) : cname = cname.replace('Pharmaceuticals','Pharma')
                if toobig(cname) : cname = cname.replace('Center','Ctr.')
                if toobig(cname) : cname = cname.replace('Investment Trusts','Invest...')
                if toobig(cname) : cname = cname.replace('Financial Advisors','Financ...')
                if toobig(cname) : cname = cname.replace('Fed. Employees Assn','Fed. Employ...')

                if toobig(cname) : cname = cname.replace('Support to Ensure Victory Everywhere PAC','S.T.E.V.E. PAC')
                if toobig(cname) : cname = cname.replace('Insurance Agents \\\\\& Brokers','Insurance Agents \\\\\& Br...')
                if toobig(cname) : cname = cname.replace('Crop production \\\\\& basic processing','Crop production, basic processing')
                if toobig(cname) : cname = cname.replace('Orthopaedic Surgeons','Orthopaedic Surg...')

                if toobig(cname) :
                    too_long.append(cname)

                os.system("sed -i \'\' 's/%s%d/%s/g'           PoliticsTableTemplate_tmp.tex"%(sed_item_0,jindex-1,cname))
                os.system("sed -i \'\' 's/%sPAC%d/%s/g'        PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,pac))
                os.system("sed -i \'\' 's/%sINDIV%d/%s/g'      PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,indiv))
                os.system("sed -i \'\' 's/%sTOT%d/%s/g'        PoliticsTableTemplate_tmp.tex"%(sed_item_1,jindex-1,total))
                os.system("sed -i \'\' \"s/APOSTROPHE/\'/g\"   PoliticsTableTemplate_tmp.tex")

        Utils.pdflatex('.','PoliticsTableTemplate_tmp.tex')
        Utils.pdflatex('.','PoliticsCombineLayers.tex')
        cmd = 'mv PoliticsCombineLayers.pdf output/%s.pdf'%(name)
        #print cmd
        os.system(cmd)
        #subprocess.Popen(['pdflatex','PoliticsTableTemplate_tmp.tex'],stdout=subprocess.PIPE)

    print 'Skipped:'
    for sk in skipped :
        print ' -',sk

    print 'Too long:'
    for tl in set(too_long) :
        print ' -',tl

    print 'done'
    return

#-----------------------------------------------
if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    p.add_option('--cycle',type='string',default='2018',dest='cycle',help='Election cycle')
    p.add_option('-n','--n',type='float',default=100000,dest='n',help='Process n entries')
    options,args = p.parse_args()

    main(options,args)
