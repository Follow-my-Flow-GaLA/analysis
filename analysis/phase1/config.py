import re

class CONFIG:
    SCAN_REQUIRED_STR = "--------- s o u r c e   c o d e ---------"
    PARSE_LOG_REG = r"(?:RTO|RAP0|RAP1) KeyIs .*?<.*?: (\w*?)>\n" + \
    r"=== JS Info ===\n(?:Skip Non-JS;\n)+(.*?) \[(.*?):(\d+):(\d+)\]\n" + \
    r"--------- s o u r c e   c o d e ---------\n(.*?)\n" + \
    r"-----------------------------------------\n (?:RTOEnd|RAP0End|RAP1End)" # TODO: PARSE_LOG_REG incorrect!
    STARTING_KEYS = ["RTO", "RAP0", "RAP1", "JRGDP", "OGPWII", "GPWFAC"]
    SHOULD_EXCLUDE = "extensions::"
    EXTRACT_CODE_INFO_REG = r"==>\((\w*?), (.*?), (\d*?)\)"
    EXTRACT_MORE_INFO_REG = r"(?:AM|PM) (.*?)_log_file==>\((\w*?), (.*?), (.*?), (.*?), (\d*?), (\d*?)\)"
    EXTRACT_INFO_REG = r"(?:.*AM |.*PM )?(.*?)_log_file==>\((\w*?), (.*?), (.*?), (.*?), (\d*?), (\d*?)\)"

    
    BLACKFAN_JS_FINGERPRINT = {
        "adobedtm": ["_shouldRelease", "_buildScript", ".attrs.src||", ".attrs.SRC"], 
        "Backbone": ["if(!this.el)"], 
        "Scriptaculous": ["__parseStyleElement"], 
        "Knockout": ["with($context){with($data||{})"], 
        "Segment Analytics": ["\"string\"!=typeof", "'string'!=typeof"], 
        "google_tag_manager": ["\"IFRAME\",{title:\"reCAPTCHA\",src:", "'IFRAME',{title:'reCAPTCHA',src:"], 
        "jQuery $(x).off": [".preventDefault", ".handleObj"], 
        "pendo": ["=HOST+\"/data/\"", "=HOST+'/data/'"], 
        "jQuery $.get": [".url||location.href", "jQuery.event.trigger(\"ajaxStart\")", "jQuery.event.trigger('ajaxStart')"], 
        "embedly": [".extend({},", ".protocol=window.location.protocol,"]
    }
    
    SCAN_ROOT_PATH = "/media/datak/inactive/sanchecker/src/inactive_0to100k_phase1_logs"
    THIS_ROOT_PATH = "/media/datak/inactive/analysis/phase1"
