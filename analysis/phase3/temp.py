def replace_no_quote(begin, whole):
    # Decide if str whole startswith str begin, ignoring ', " and `
    begin_idx = 0
    whole_idx = 0
    while begin_idx != len(begin):
        if whole[whole_idx] == begin[begin_idx]:
            begin_idx += 1
            whole_idx += 1
            continue
        elif begin[begin_idx] in ['"', "'", "`"]:
            begin_idx += 1
            continue
        elif whole[whole_idx] in ['"', "'", "`"]:
            whole_idx += 1
            continue
        else:
            # Not matched
            return None
    return whole[whole_idx:]

begin = 'with(this){return (tooltip)?_c(\'app\',{key:jet-mobile-menu__toggle,ref:"jet-mobile-menu__toggle",staticClass:".index-container",class:'
whole = 'with(this){return (tooltip)?_c(\'app\',{key:\'jet-mobile-menu__toggle\',ref:"jet-mobile-menu__toggle",staticClass:".index-container",class:{[console.log(67890)]:true}})};//'
a = replace_no_quote(begin, whole)
print(a)

target_list = [ each.strip('./').replace('_log_file', '').replace('.', '_') for each in '''./myexternalip_com_log_file
./iamcook_ru_log_file
./cargosmart_com_log_file
./pfizer_com_log_file
./loc_gov_log_file
./lanebryant_com_log_file
./commbank_com.au_log_file
./webmd_com_log_file
./federalreserve_gov_log_file
./micron_com_log_file
./gosexpod_com_log_file
./travelchannel_com_log_file
./reshak_ru_log_file
./econsultancy_com_log_file
./gls-group_eu_log_file
./discovery_com_log_file
./xumo_com_log_file
./circle_com_log_file
./honda_com_log_file
./mtvuutiset_fi_log_file
./elektra_mx_log_file
./trulia_com_log_file
./siemens_de_log_file
./skysports_com_log_file
./k12_com_log_file
./viamichelin_com_log_file
./odu_edu_log_file
./cc_com_log_file
./cnil_fr_log_file
./charitynavigator_org_log_file
./deutschepost_de_log_file
./siemens_com_log_file
./landsend_com_log_file
./oneamerica_com_log_file
./long_tv_log_file'''.split('\n')]

from result_buffer import js_ans, non_js_sink
return_dict = {}
for site in {**js_ans, **non_js_sink}.keys():
    if site not in target_list:
        continue
    return_dict[site] = set()
    if site in js_ans.keys():
        for each_js_ans_dict in js_ans[site]:
            if not each_js_ans_dict["exploit"] or each_js_ans_dict["exploit"] == 'MyString':
                continue
            # A rough filter to filter out known FPs
            if each_js_ans_dict['src_payload'] in ['c'] or each_js_ans_dict['sink_payload'] in ['c']:
                continue
            return_dict[site].add(each_js_ans_dict["exploit"])
    if site in non_js_sink.keys():
        for each_non_js_sink_dict in non_js_sink[site]:
            if not each_non_js_sink_dict["exploit"] or each_non_js_sink_dict["exploit"] == 'MyString':
                continue
            # A rough filter to filter out known FPs
            if each_non_js_sink_dict['src_payload'] in ['c'] or each_non_js_sink_dict['sink_payload'] in ['c']:
                continue
            return_dict[site].add(each_non_js_sink_dict["exploit"])
print(len(return_dict.keys()), return_dict)

gadget_count_dict = {}
for site, value_set in return_dict.items():
    for exploit in value_set:
        
        if exploit not in gadget_count_dict.keys():
            gadget_count_dict[exploit] = [site]
        else:
            gadget_count_dict[exploit].append(site)
print(len(gadget_count_dict.keys()), gadget_count_dict)
