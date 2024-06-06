import re

class CONFIG:
    # for gen_payload_val_dict
    PHASE3_RECORD_PATH = "/media/datak/inactive/sanchecker/record_detector_1M_phase3_db_crawl/"
    RECORD_START_REG = re.compile("start = (\d+),")
    RECORD_END_REG = re.compile("end = (\d+),")
    RECORD_CONTENT_REG = re.compile('content = \"((?:\n|.)*?)\",\s*?isOneByte = (true|false)')
    RECORD_SINKTYPE_REG = re.compile("sinkType = (\w+),")
    # RECORD_SOURCE_CODE_REG = re.compile("\\n.*?\[.*?:(\d+):(\d+)\]\\n--------- s o u r c e   c o d e ---------\\n((?:\n|.)*?)\\n")
    RECORD_SOURCE_CODE_REG = re.compile(".*?\[.*?:(\d+):(\d+)\]--------- s o u r c e   c o d e ---------((?:\n|.)*?)(?:------------|...\" \) \),\n)")
    
    STR_MATCH_THRESHOLD = 0.78
    
    # for gen_payload_dict
    #PHASE3_VALUE_DATA_JS_PATH = "/home/zfk/Documents/inject_pp_extension/value_data.js"
    SHOULD_EXCLUDE = "extensions::"
    SHOULD_EXCLUDE_SINKTYPE = ['sinkType = prototypePollution', 'sinkType = xmlhttprequest', 'sinkType = logical']
    
    # for process
    PHASE3_LOG_PATH = "/media/datak/inactive/sanchecker/src/detector_1M_phase3_db_logs/"
    STARTING_KEYS = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC"]
    PARSE_LOG_REG = r"(?:RTO|RAP0|RAP1|JRGDP|OGPWII|GPWFAC) KeyIs .*?<.*?: (\w*?)>\n" + \
    r"=== JS Info ===\n(?:Skip Non-JS;\n)+(.*?) \[(.*?):(\d+):(\d+)\]\n" + \
    r"--------- s o u r c e   c o d e ---------\n(.*?)\n" + \
    r"-----------------------------------------\n (?:RTOEnd|RAP0End|RAP1End|JRGDPEnd|OGPWIIEnd|GPWFACEnd)"
    
    # for gen_json
    THIS_ROOT_PATH = "/media/datak/inactive/analysis/phase3"
    
    # for new_undef 
    #PHASE1_INFO_JSON = "/media/datak/inactive/analysis/phase1/output/phase1_info.json"
    #PHASE3_INFO_JSON = "/media/datak/inactive/analysis/phase3/output/phase3_info.json"
    
    # for check_def_flows
    STORE_ROOT_PATH = "/media/datak/inactive/sanchecker/"
