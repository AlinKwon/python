from bs4 import BeautifulSoup
from re import sub
import requests

def main():
    # python 3에서는 print() 으로 사용합니다.
    with open('Menu1.html', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        html = ''.join(lines)
        soup = BeautifulSoup(html, 'html.parser')
        
        roots = soup.find_all('li', attrs={'class':'c-menu__item'})
        
        for itemRoot in roots:
            writeLine = []
            
            writeLine.append('(')
            
            writeLine.append('"')
            link = itemRoot.find('a', attrs={'class':'c-menu__item-inr'})
            if (link != None) :
                writeLine.append(link['href'].replace('https://www.hottomotto.com/menu_list/view/13/',''))
            writeLine.append('",')             
            
            writeLine.append('"')
            name = itemRoot.find('p', attrs={'class':'c-menu__title'})
            if (name != None) :
                writeLine.append(name.get_text().strip())
            writeLine.append('",')             
            
            writeLine.append(' ')
            price = itemRoot.find('span', attrs={'class':'c-menu__price'})
            if (price != None) :
                writeLine.append(sub(r'[^\d.]', '', price.get_text().strip()))
            writeLine.append(', ')             
            
                            
            writeLine.append('"')
            imgsrc = itemRoot.find('img', attrs={'class':'c-menu__pict'})
            if (imgsrc != None) :
                writeLine.append(imgsrc['src'].replace('./Menu1_files/',''))
            writeLine.append('",')             
            
            writeLine.append('"')
            annotaion = itemRoot.find('p', attrs={'class':'c-annotaion'})
            if (annotaion != None) :
                writeLine.append(annotaion.get_text().strip().replace('\n', ' '))
            writeLine.append('"')   
                            
            writeLine.append(')')
            print(''.join(writeLine))
            
            with open('item_info.txt','a',encoding='utf-8') as wInfo:
                wInfo.write(''.join(writeLine))
                wInfo.write('\n')
                
            with open('item_link.txt','a',encoding='utf-8') as wlink:
                link = itemRoot.find('a', attrs={'class':'c-menu__item-inr'})
                if (link != None) :
                    wlink.write(link['href'])
                    wlink.write('\n')
        
  
        
        #name
        # names = soup.find_all('p', attrs={'class':'c-menu__title'})
        # for name in names:
        #     with open('names.txt', 'a', encoding='UTF-8') as wfile:
        #         pname = name.get_text().strip()
        #         print(pname)
        #         wfile.write(pname)
        #         wfile.write('\n')
        
        #price
        # pricexs = soup.find_all('span', attrs={'class':'c-menu__price'})
        # for price in pricexs:
        #     with open('pricexs.txt', 'a', encoding='UTF-8') as wfile:
        #         tprice = price.get_text().strip()
        #         print(tprice)
        #         wfile.write(
        #             sub(r'[^\d.]', '', tprice)
        #             )
        #         wfile.write('\n')
        
        # annotaions = soup.find_all('div', attrs={'class':'c-menu__txt'})
        # for annotaion in annotaions:
        #     with open('annotaions.txt', 'a', encoding='UTF-8') as wfile:
        #         tannotaion = annotaion.get_text().strip()
        #         print(tannotaion)
        #         wfile.write(
        #             tannotaion
        #             )
        #         wfile.write('\n')
        
        
def main2():
    with open('item_link.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        with open('item_subinfo.txt','a',encoding='utf-8') as sInfo:
            for line in lines:
                writeLine = []
                req = requests.get(line.replace('\n', ''))
                print(line)
                writeLine.append('(')
                writeLine.append('"')
                writeLine.append(line.replace('https://www.hottomotto.com/menu_list/view/13/','').replace('\n', ''))
                writeLine.append('",')
                
                if(req.ok):
                    soup = BeautifulSoup(req.text, 'html.parser')
                
                    infos = soup.find(True, {'class':['c-tab__cont-item','js-tab__cont', 'is_show']})
                    if (infos != None) :
                        for info in infos.findAll('dd', attrs={'class':'c-table__body'}):
                            writeLine.append('"')
                            writeLine.append(info.get_text().strip())
                            writeLine.append('",')
                            
                    writeLine.append('"')
                    desc = soup.find('p', attrs={'class':'c-menu-detail__txt--desc'})
                    if (desc != None) :
                        writeLine.append(desc.get_text().strip().replace('\n', ' '))
                    writeLine.append('"')                
                    
                else:
                    writeLine.append('"",""')
                writeLine.append(')')
                sInfo.write(''.join(writeLine))
                sInfo.write('\n')

if __name__ == "__main__":
	# main()
    main2()