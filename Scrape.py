import os

os.system("wget -O 'tmp_scrape_p1.txt' 'https://www.congress.gov/members?q={%22congress%22:%22115%22}&searchResultViewType=compact&pageSize=250'")
os.system("wget -O 'tmp_scrape_p2.txt' 'https://www.congress.gov/members?q=%7B%22congress%22%3A%22115%22%7D&searchResultViewType=compact&pageSize=250&page=2'")
os.system("wget -O 'tmp_scrape_p3.txt' 'https://www.congress.gov/members?q=%7B%22congress%22%3A%22115%22%7D&searchResultViewType=compact&pageSize=250&page=3'")

os.system('cat tmp_scrape_*.txt >& tmp_scrape.txt')

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

    member[name] = dict()
    member[name]['img'] = img
    member[name]['state'] = state
    
    print '%s %s %s %s' % (state,district,name,img)

    #os.system('mkdir -p %s'%(state.replace(' ','_')))
    os.system('mkdir -p figures')
    
    os.system("wget -O 'figures/%s' 'https://www.congress.gov%s'"%(img.replace('/img/member/',''),img))

    os.system('')
    
print 'done'
