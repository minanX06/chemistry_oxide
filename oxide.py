from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def e_big(a, b):
    if atom_info[a] > atom_info[b]:
        return a
    elif atom_info[a] < atom_info[b]:
        return b
    
def e_small(a, b):
    if atom_info[a] < atom_info[b]:
        return a
    elif atom_info[a] > atom_info[b]:
        return b

def absolute(x):
    if x < 0:
        return int(x*-1)
    else:
        return int(x)
    
def plus_minus(x):
    if x > 0:
        return '+' + str(int(x))
    else:
        return str(int(x))

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

url = 'https://ko.wikipedia.org/wiki/%EC%A0%84%EA%B8%B0_%EC%9D%8C%EC%84%B1%EB%8F%84'

service = Service(executable_path='cd/chromedriver.exe')

driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

element = {}
lst = []
for atom in soup.find_all('a'):
    lst.append(atom.string)
lst2 = []
for atom2 in range(170, 297):
    lst2.append(lst[atom2])
for i in range(1, 8):
    lst2.remove(str(i))
lst2.remove('악티늄족')
lst2.remove('란타넘족')

for atom in soup.find_all('td'):
    try:
        e = round(float(int(str(atom.get_text()).split(".")[0][-1]) + float("0." + str(int(str(atom.get_text()).split(".")[1])))), 2)
        element[str(atom.get_text()).split(".")[0][0:-1]] = e
    except:
        pass

atom_info = {}
for atoms in lst2:
    try:
        atom_info[atoms] = float(element[atoms])
    except:
        atom_info[atoms] = 0
while True:
    oxide = input('산화수 구하기: ')
    oxide = oxide.strip()
    oxide_analyze = []
    for k in range(len(oxide)):
        oxide_analyze.append(oxide[k])

    lst3 = []
    for w in oxide_analyze:
        if w.isupper():
            lst3.append(oxide_analyze.index(w))

    element_sort = []
    for i in range(len(lst3)):
        try:
            element_sort.append(oxide[int(lst3[i]):int(lst3[i+1])])
        except:
            element_sort.append(oxide[int(lst3[i]):])

    dic = {}
    for element in element_sort:
        try:
            dic[element[:-1]] = int(element[-1])
        except:
            dic[element] = 1
    ion_dic = {'Li':1, 'Be':2, 'F':-1, 'Na':1, 'Mg':2, 'K':1, 'Ca':2, 'O':-2, 'S':-2, 'Ba':2, 'Cl':-1, 'I':-1, 'S':-2, 'Br':-1}

    #산화수 구하기
    atom_lst = list(dic.keys())
    if len(atom_lst) == 1:
        print(atom_lst[0] + ':' + str(0))
    elif len(atom_lst) == 2:
        try:
            H = atom_lst.index('H')
            if absolute(ion_dic[atom_lst[int(1 - H)]]) <= dic[atom_lst[int(H)]]/dic[atom_lst[int(1 - H)]]:
                print(str(atom_lst[int(1 - H)]) + ": " + plus_minus(ion_dic[atom_lst[int(1 - H)]]))
            else:
                print(str(atom_lst[int(1 - H)]) + ": " + plus_minus(dic[atom_lst[int(H)]]/dic[atom_lst[int(1 - H)]]))
            if ion_dic[atom_lst[int(1 - H)]] > 0:
                print(str(atom_lst[H]) + ": " + '-1')
            else:
                print(str(atom_lst[H]) + ": " + '+1')
        except:
            print(str(e_big(atom_lst[0], atom_lst[1])) + ": " + plus_minus(ion_dic[e_big(atom_lst[0], atom_lst[1])]))
            print(str(e_small(atom_lst[0], atom_lst[1])) + ": " + plus_minus(int(dic[e_big(atom_lst[0], atom_lst[1])]*ion_dic[e_big(atom_lst[0], atom_lst[1])]/dic[e_small(atom_lst[0], atom_lst[1])]*-1)))
    print('--------------------------')