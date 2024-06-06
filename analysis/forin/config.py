import re

class CONFIG:    
    PHASE1_JS_INFO_JSON_PATH = "/media/datak/from_aws_2022/inactive/output/phase1_info.json"
    
    # This dir contains defined value (in the format of taint strings detected in sink functions)
    # PHASE2_RECORD_PATH = "/home/zfk/Documents/sanchecker/record_inactive_notemplate_phase2_crawl" 
    PHASE2_RECORD_PATH = "/media/datak/inactive/sanchecker/record_inactive_notemplate_phase2_partial_crawl"
    # Example file: os.path.join(CONFIG.PHASE2_RECORD_PATH + "record_westhost_com_9270_1690585137839_0")
    
    # regex for record
    RECORD_START_REG = re.compile("start = (\d+),")
    RECORD_END_REG = re.compile("end = (\d+),")
    RECORD_CONTENT_REG = re.compile('content = \"((?:\n|.)*?)\",\s*?isOneByte = (true|false)') #re.compile("content = \"((\n|.)*)\",")
    RECORD_SINKTYPE_REG = re.compile("sinkType = (\w+),")
    SHOULD_EXCLUDE_SINKTYPE = ['sinkType = prototypePollution', 'sinkType = xmlhttprequest', 'sinkType = logical']
    
    
    
    # This dir contains all information but defined values: 
    PHASE2_LOG_PATH = "/media/datak/inactive/sanchecker/src/inactive_notemplate_phase2_partial_logs/"
    # Example file: os.path.join(CONFIG.PHASE2_LOG_PATH + "westhost_com_log_file")
    
    # regex for log
    LOG_KEY_VALUE_REG = re.compile("<String\[\d+].?: (.*?)>(.|\n)*?<String\[\d+].?: (.*?)>")
    LOG_LN_REG = re.compile("Line:(\d+,\d+)|Line:(\d+)")
    LOG_CODEHASH_REG = re.compile("code_hash is:(.*?) ")
     
        
        
    SCAN_ROOT_PATH = "/media/data1/zfk/Documents/sanchecker/src/inactive_0to100k_phase1_logs"
    THIS_ROOT_PATH = "/media/datak/inactive/sanchecker/" #"/home/zfk/Documents/sanchecker/src/Inactive"
    
    
    
    
    
    
    