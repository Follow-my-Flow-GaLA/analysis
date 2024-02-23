import re
import requests

'''
    Data block example:

    utf8_func_hash is 50e13321b1057ed4dd921a48a515836c0d91cca8049247c89716691ce7a54059
    http_code is 0
    jsonData is 
    {
        "code_hash" : "50e13321b1057ed4dd921a48a515836c0d91cca8049247c89716691ce7a54059",
        "col" : "43",
        "func" : "function n(r){if(e[r])return e[r].exports;var i=e[r]={i:r,l:!1,exports:{}};return t[r].call(i.exports,i,i.exports,n),i.l=!0,i.exports}",
        "func_name" : "n",
        "js" : "https://inte.searchnode.io/kasa/searchnode.min.js?1701252262",
        "key" : "202",
        "phase" : "1",
        "row" : "6",
        "site" : "hej.sk",
        "start_key" : "RAP0"
    }
'''

SITE = "test_com"
LOG_PATH = '/home/zfk/temp/phase1_db_hej_sk_log_file'
API_URL = 'http://127.0.0.1:5000/api/phase1/'
    
def read_log_file(code_hash_dict):
    print('Reading log file...')
    with open(LOG_PATH) as f:
        # read the data block
        l = f.readline()
        while l:
            if l.startswith('\t"code_hash" : "'):
                code_hash = l.split('"')[3]
                l = f.readline()
                col = l.split('"')[3]
                for i in range(4):
                    l = f.readline()
                key = l.split('"')[3]
                for i in range(2):
                    l = f.readline()
                row = l.split('"')[3]
                check_data_exist(code_hash_dict, code_hash, col, key, row)
            l = f.readline()

def check_data_exist(code_hash_dict, code_hash, col, key, row):
    key = key.replace('.', '\\2E').replace('$', '\\24')
    # check if data exist in phase_info
    error_msg = ""
    if code_hash in code_hash_dict:
        if key in code_hash_dict[code_hash]:
            data_list = code_hash_dict[code_hash][key]
            if row + ', ' + col in data_list[0]:
                pass
            else:
                error_msg += 'Error: data does not exist in the phase_info (key: ' + key + '). \n'
                
        else:
            error_msg += 'Error: key does not exist in the phase_info (key: ' + key + '). \n'
    else:
        error_msg += 'Error: code_hash does not exist in the phase_info (code_hash: ' + code_hash + '). \n'
    # check if data exist in undef_prop_dataset
    response = requests.get(API_URL + 'undef_prop_dataset?code_hash=' + code_hash)
    if response.status_code == 200:
        if response.text != 'Code hash not found':
            data = response.json()["key_value_dict"]
            if key in data:
                row_col_list = data[key]
                if row + ', ' + col in row_col_list:
                    pass
                else:
                    error_msg += 'Error: data does not exist in the undef_prop_dataset (key: ' + key + '). \n'
            else:
                error_msg += 'Error: key does not exist in the undef_prop_dataset (key: ' + key + '). \n'
        else:
            error_msg += 'Error: code_hash does not exist in the undef_prop_dataset (code_hash: ' + code_hash + '). \n'
    else:
        error_msg += 'Error: error occurred when querying the database. \n'
    if error_msg:
        print("Failed. (code_hash: " + code_hash + ", key: " + key + ")")
        # print(error_msg)
    else:
        print('Data is consistent. (code_hash: ' + code_hash + ', key: ' + key + ')' )

if __name__ == '__main__':    
    # query site from db
    response = requests.get(API_URL + 'phase_info?site=' + SITE)
    if response.status_code == 200:
        if (response.text == 'Site not found'):
            print('Website does not exist in the database')
        else: 
            data = response.json()
            code_hash_dict = data['code_hash_dict']
            open("code_hash_dict.txt", "w").write(str(code_hash_dict))
            read_log_file(code_hash_dict)
    else:
        print('Website does not exist in the database')