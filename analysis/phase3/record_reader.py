import os, re, codecs, glob, difflib

from phase3_config import CONFIG

# Function to generate a set of payload values from record
# output: sink_val_list = [{payload, sink_type, start_pos, end_pos, sink_string, message_id}]
def get_sink_val_list(site, fpath):
    sink_val_list = []
    
    inactive_flag = False
    start_pos = end_pos = -1
    var_val = sink_type = ""
    message_id = -1
    pos_list = []
    content_list = []
    
    with codecs.open(fpath, mode='r') as ff:
        lines = ff.readlines()
        pos_list = []
        for num, line in enumerate(lines, 0):
            if 'type = inactive' in line: # get start_pos & end_pos
                if 'start' in line: 
                    start_pos = int(re.search(CONFIG.RECORD_START_REG, line).group(1))
                else:
                    start_pos = int(re.search(CONFIG.RECORD_START_REG, lines[num-2]).group(1))
                search_end_pos_str = "".join(lines[num+1:num+6])
                # next start_pos is the end_pos for last entree
                search_end_pos_result = re.search(CONFIG.RECORD_START_REG, search_end_pos_str)
                if search_end_pos_result:
                    end_pos = int(search_end_pos_result.group(1))
                else:
                    end_pos = 4294967295 # the last var is inactive
                inactive_flag = True
                pos_list.append((start_pos, end_pos))
                continue
            
            if inactive_flag and 'targetString = (' in line: # extract var_val from content
                content_list = []
                # Find sink_type line first
                for sink_line_num, temp_line in enumerate(lines[ num+2 : ]):
                    search_sink_type_result = re.search(CONFIG.RECORD_SINKTYPE_REG, temp_line)
                    if (search_sink_type_result):
                        sink_type = search_sink_type_result.group(1)
                        break
                else:
                    # No sink_type provided. Abort
                    print(f"Warning: Website {site} in {fpath} finds no sink_type from line {num}")
                    continue
                
                if sink_type in ["prototypePollution", "xmlhttprequest", "logical"]:
                    continue
                
                # Search for contents within that block: lines[ num+2 : sink_line_num ]
                sink_line_num += num + 2
                content_matches = re.findall(CONFIG.RECORD_CONTENT_REG, ''.join(lines[ num+2 : sink_line_num ]))
                if not content_matches:
                    print(f"Warning: Website {site} in {fpath} finds no contents in line {num+2} to {sink_line_num}")
                    continue
                
                for each_content, is_one_byte in content_matches:
                    if is_one_byte == 'false':
                        # Two-byte string. needs encoding
                        each_content = each_content.replace('\\x00','')
                        if False and "\\x" in each_content:
                            try:
                                bytes(each_content, encoding='latin-1').decode('utf-16le')
                            except (UnicodeDecodeError, ValueError) as e:
                                print(f"Skipped due to Error {e}: Website {site} in {fpath} cannot handle two-byte {each_content} in line {num+2}")
                    if "\\" in each_content:
                        try: 
                            each_content = eval(f'"{each_content}"') 
                        except Exception as e:
                            print(f"Skipped due to Error {e}: Website {site} in {fpath} failed to eval {content_list} in line {num+2}")
                    content_list.append(each_content) 
                content_list = ''.join(content_list)
                continue
    
            if inactive_flag and 'messageId =' in line: # extract message_id
                try:
                    message_id = line.split("messageId = ")[1][:-1]
                except Exception as e:
                    print(f"Error: Website {site} in {fpath} failed to get messageId in line {num}")
                    continue
                
                var_val_pos_set = set() # when payloads are the same, choose the one with smallest start&end pos
                for start_pos, end_pos in pos_list:
                    try:
                        var_val = content_list[int(start_pos): int(end_pos)]
                        if str(var_val) in var_val_pos_set:
                            continue
                        sink_val_list.append({
                            "sink_payload": str(var_val),
                            "sink_type": sink_type,
                            "start_pos": start_pos,
                            "end_pos": end_pos,
                            "sink_string": content_list, 
                            "message_id": message_id
                        }) 
                        var_val_pos_set.add(str(var_val))
                    except ValueError:
                        print(f"ValueError: {start_pos} or {end_pos} failed to str->int! Website {site} in {fpath} in line {num+2}. ")
                        continue                  
                inactive_flag = False
                content_list = []
                pos_list = []
                continue
    return sink_val_list
