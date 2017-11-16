from selenium import webdriver
import re, time, jsonlines


def conv_str(sr):
    """Converting proxy strings"""
    r_l = []
    t_str = re.split(' ', sr)
    r_l.append(t_str[0])
    r_l.append(t_str[1][0:len(t_str[1]) - 1])
    if re.search('[A-Z]+4', sr):
        r_l.append(str(4))
    elif re.search('[A-Z]+5', sr):
        r_l.append(str(5))
    return r_l


def read_proxies(filepath):
    proxy_list = []
    with jsonlines.open(filepath) as reader:
        for i, state in enumerate(reader):
            proxy_list.append(state)
        reader.close()
    return proxy_list


def startCollectProxies():
    """Moving to site and collect proxies"""
    driver = webdriver.Firefox()
    driver.get("http://hideme.ru/proxy-list/?maxtime=250&type=45#list")

    with jsonlines.open('proxies/proxy.jsonl', 'w') as f:
        cont = driver.find_element_by_xpath('//tbody')
        for i, k in enumerate(cont.find_elements_by_xpath('//tr')):
            if i == 0:
                pass
            else:
                temp_dict = k.text
                f.write(conv_str(temp_dict))
        f.close()

    time.sleep(1)
    driver.quit()
    return 'proxies/proxy.jsonl'