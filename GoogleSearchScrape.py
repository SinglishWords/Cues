from selenium import webdriver
import pandas as pd

def search(query):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get('http://www.google.com/')
    #agree = driver.find_element_by_id('L2AGLb')
    #agree.click()
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(query)
    search_box.submit()
    r = driver.find_element_by_id('result-stats').text
    if r.find('About') == -1:
        r = int(r[: r.find('result')].replace(',', ''))
    else:
        r = int(r[5: r.find('result')].replace(',', ''))
    driver.quit()
    return r

cues = pd.read_csv('ListOfWords.csv')
#results = pd.DataFrame(columns=['cues', 'result', 'compare'])
results = pd.read_csv('GoogleSearch.csv')
start = len(results)-1
for index, row in cues.iterrows():
    if index > start:
        result = search('Singapore "'+row['cues']+'"')
        compare = search('"'+row['cues']+'" Singapore')
        results.loc[index] = [row['cues'], result, compare]
        results.to_csv('results.csv', index=False)
        print(results.loc[index])
