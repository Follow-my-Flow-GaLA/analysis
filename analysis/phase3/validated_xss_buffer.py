validated_xss_list=[each.replace('./', '').replace('_log_file', '').replace('_', '.') for each in '''
./myexternalip_com_log_file
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
./long_tv_log_file
'''.strip('\n').split('\n')]

manual_list = [each for each in '''
pavlovmedia.com
guru99.com
factroom.ru
bokee.com
myexternalip.com
igetget.com
dolby.com
domsporta.com
rosuchebnik.ru
viamichelin.co.uk
sodapdf.com
yuanshen.com
mountvernon.org
unimelb.edu.au
'''.strip('\n').split('\n')]

if __name__ == "__main__":
    getting_xss_exploit_info = False
    all_xss_domain = set(validated_xss_list + manual_list)
    print(len(all_xss_domain), all_xss_domain)
    if getting_xss_exploit_info:
        from result_buffer import js_ans, non_js_sink
        import json
        validated_xss_list = [each.replace('.', '_') for each in validated_xss_list]
        info = {}
        for each in [js_ans, non_js_sink]:
            for k,v in each.items():
                if k in validated_xss_list:
                    if k not in info.keys():
                        temp_list = []
                        for each_list_elem in v:
                            temp_dict = {}
                            for name, content in each_list_elem.items():
                                if name not in ['sink_string', 'code']:
                                    temp_dict[name] = content
                            temp_list.append(temp_dict)
                        info[k] = temp_list
                    else:
                        info[k] += v
        with open('xss_results.json', 'w') as fw:
            fw.write(json.dumps(info))
    