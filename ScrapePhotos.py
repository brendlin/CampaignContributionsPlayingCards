import os

#-------------------------------------------------------------------------
def main(options,args) :

    outfile = open('tmp_ImageData.csv','w')

    os.system("wget -O 'tmp_scrape_p1.txt' 'https://www.congress.gov/members?q={%22congress%22:%22115%22}&searchResultViewType=compact&pageSize=250'")
    os.system("wget -O 'tmp_scrape_p2.txt' 'https://www.congress.gov/members?q=%7B%22congress%22%3A%22115%22%7D&searchResultViewType=compact&pageSize=250&page=2'")
    os.system("wget -O 'tmp_scrape_p3.txt' 'https://www.congress.gov/members?q=%7B%22congress%22%3A%22115%22%7D&searchResultViewType=compact&pageSize=250&page=3'")

    os.system('cat tmp_scrape_*.txt >& tmp_scrape.txt && rm tmp_scrape_p1.txt tmp_scrape_p2.txt tmp_scrape_p3.txt')

    member = dict()

    lines = open('tmp_scrape.txt').readlines()

    for index,i in enumerate(lines) :

        if index > 3000 : continue

        i = i.replace('\n','')
        if '.jpg' not in i :
            continue

        alt_i = i.find('alt=')
        if alt_i < 0 :
            continue

        img_i = i.find('img src=')
        if img_i < 0 :
            continue

        name = i[alt_i:].split('"')[1]
        firstname = name.split(',')[1].lstrip().split(' ')[0]
        lastname = name.split(',')[0]
        name = '%s_%s'%(firstname,lastname)
        name = name.replace(' ','')

        img = i[img_i:].split('"')[1]

        if name in member.keys() :
            continue

        state = 'Unknown'
        for jindex,j in enumerate(lines[index:index+30]) :
            if 'State:' in j :
                state = lines[index+jindex+1].split('<span>')[1].split('</span>')[0]
                break

        district = '---'
        for jindex,j in enumerate(lines[index:index+30]) :
            if 'District:' in j :
                district = lines[index+jindex+1].split('<span>')[1].split('</span>')[0]
                break

        img = img.replace('_200','')
        #img_local = img.replace('/img/member/','')
        img_local = 'figures/%s.jpg'%(name)

        member[name] = dict()
        member[name]['img'] = img_local
        member[name]['state'] = state

        outfile.write('%s,%s,%s,%s\n' % (name,state,district,img_local))

        os.system('mkdir -p figures')
        os.system("wget -O '%s' 'https://www.congress.gov%s'"%(img_local,img))

    outfile.close()

    print 'done'

#-----------------------------------------------
if __name__ == '__main__':

    from optparse import OptionParser
    p = OptionParser()
    options,args = p.parse_args()

    main(options,args)
