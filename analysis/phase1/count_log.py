LOG_PATH = '/home/zfk/temp/phase1_db_hej_sk_log_file'

def read_log_file():
    count = 0
    with open(LOG_PATH) as f:
        # read the data block
        l = f.readline()
        while l:
            data_block_str = ""
            if "utf8_func_hash" in l:
                count += 1
                while l:
                    data_block_str += l
                    if l =='}\n':
                        break
                    l = f.readline()
            l = f.readline()
    print(count)


if __name__ == '__main__':
    read_log_file()