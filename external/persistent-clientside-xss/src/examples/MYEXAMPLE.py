# Copyright (C) 2019 Ben Stock & Marius Steffens
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# flow from LocalStorage into eval
MYEXAMPLE = {u'd1': u'Function',
            u'd2': None,
            u'd3': u'https://d3.sina.com.cn/litong/zhitou/sinaads/release/sinaads.js:7:7613',
            u'finding_id': 3474,
            u'sink_id': 1,
            u'sources': [{u'end': 42,
                          u'finding_id': 3474,
                          u'hasEncodingURI': 0,
                          u'hasEncodingURIComponent': 0,
                          u'hasEscaping': 0,
                          u'id': 30553,
                          u'source': 13,
                          u'source_name': u'localStorage',
                          u'start': 37,
                          u'value_part': u'ad_id'}],
            u'storage': {u'cookies': [[u'UOR', u',www.sina.com.cn,', -1],
                                      [u'ULV', u'1552320680552:1:1:1::', -1],
                                      [u'SGUID', u'1552320685063_73970037', -1],
                                      [u'U_TRS1', u'00000035.9f63102e0.5c8688f3.8d8b7ae7', -1],
                                      [u'U_TRS2', u'00000035.9f6b102e0.5c8688f3.9dafd8d1', -1],
                                      [u'lxlrttp', u'1551747590', -1],
                                      [u'CNZZDATA1271230489',
                                       u'655136813-1552318791-https%253A%252F%252Fwww.sina.com.cn%252F%7C1552318791',
                                       -1]],
                         u'storage': [[u'adsData',
                                       u'ad_id', 
                                       1],
                                      [u'blkLike_logout', u'', 0],
                                      [u'brandListDataFromApiTime', u'1552320690299', 1],
                                      [u'eduTabNum', u'58', 1],
                                      [u'eduTabNum.expires', u'Tue Mar 12 2019 17:13:20 GMT+0100 (CET)', 1],
                                      [u'sinaads_2j6f', u'49;expires=1554912789169', 1],
                                      [u'sinaads_test_ls', u'support', 1],
                                      [u'u3173505_0',
                                       u'{"queryid":"6ff2fffbac896931","tuid":"u3173505_0","placement":{"basic":{"sspId":1,"userId":24904060,"flowType":1,"cname":"92073368_cpr","tuId":9223372032562982000,"sellType":2,"rspFormat":1,"conBackEnv":1,"publisherDomain":{"dup":"hda.watchtimes.com.cn","ubmc":"hdb.watchtimes.com.cn/oqw","pos":"hdb.watchtimes.com.cn","wn":"hdb.watchtimes.com.cn/twwg"}},"container":{"height":200,"width":240,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[5],"layout":[2],"txt":{"number":0},"lu":{},"video":{},"search":{},"styleType":2},"adslottype":0,"userdefine":"%7Ccpro%5Flayout%5Ffilter%3Drank%2Ctabcloud%7Ccpro%5Ftemplate%3DbaiduTlinkInlay%7Ccpro%5Fversion%3D2%2E0","encode_userdefine":"encoded","complement_type":1,"update":"1548410576_1515025426"},"extends":{"ssph":200,"sspw":240},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3173505"},"media_protect":"","adExpire":1552320814343}',
                                       1],
                                      [u'u3173511_0',
                                       u'{"queryid":"f2b320112e3e46b5","tuid":"u3173511_0","placement":{"basic":{"sspId":1,"userId":24904060,"flowType":1,"cname":"92073368_cpr","tuId":9223372032562982000,"sellType":2,"rspFormat":1,"conBackEnv":1,"publisherDomain":{"dup":"hda.watchtimes.com.cn","ubmc":"hdb.watchtimes.com.cn/oqw","pos":"hdb.watchtimes.com.cn","wn":"hdb.watchtimes.com.cn/twwg"}},"container":{"height":200,"width":240,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[5],"layout":[2],"txt":{"number":0},"lu":{},"video":{},"search":{},"styleType":2},"adslottype":0,"userdefine":"%7Ccpro%5Flayout%5Ffilter%3Drank%2Ctabcloud%7Ccpro%5Ftemplate%3DbaiduTlinkInlay%7Ccpro%5Fversion%3D2%2E0","encode_userdefine":"encoded","complement_type":1,"update":"1548410578_1515025426"},"extends":{"ssph":200,"sspw":240},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3173511"},"media_protect":"","adExpire":1552320694074}',
                                       1],
                                      [u'u3184293_0',
                                       u'{"queryid":"7b952f26ff80a0ad","tuid":"u3184293_0","placement":{"basic":{"sspId":1,"userId":6743724,"flowType":1,"cname":"48049029_cpr","tuId":9223372032562993000,"sellType":2,"rspFormat":1,"conBackEnv":1,"publisherDomain":{"dup":"mmjs.adutp.com","ubmc":"ymjs.adutp.com/hzkz","pos":"ymjs.adutp.com","wn":"ymjs.adutp.com/cg"}},"container":{"height":120,"width":1000,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[51],"layout":[1,2],"styleTemplateId":[60101],"txt":{"number":0},"styleType":3,"ignoreStyleMode":1},"adslottype":0,"userdefine":"%7Cadp%3D1%7Cat%3D3%7CconBW%3D0%7Ccpro%5Ftemplate%3DbaiduCustNativeAD%7Cpat%3D6%7Cpih%3D0%7Cpiw%3D0%7Cptp%3D0%7Cptt%3D0%7Crss1%3D%23ffffff%7Crss2%3D%23000000%7CtitFF%3D%E5%BE%AE%E8%BD%AF%E9%9B%85%E9%BB%91%7CtitFS%3D16%7CtitSU%3D0%7Ctn%3DbaiduCustNativeAD","encode_userdefine":"encoded","complement_type":2,"update":"1541994697_1541994697"},"extends":{"ssph":120,"sspw":1000},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3184293"},"media_protect":"","adExpire":1552320694109}',
                                       1],
                                      [u'u3484575_0',
                                       u'{"queryid":"dc35e584d75ff0f9","tuid":"u3484575_0","placement":{"basic":{"sspId":1,"userId":24904060,"flowType":1,"cname":"92073368_cpr","tuId":9223372032563293000,"sellType":2,"rspFormat":1,"conBackEnv":1},"container":{"height":200,"width":240,"sizeType":1,"anchoredType":1,"floated":{}},"fillstyle":{"elements":[5],"layout":[2],"txt":{"number":0},"lu":{},"video":{},"search":{},"styleType":2},"adslottype":0,"userdefine":"%7Ccpro%5Flayout%5Ffilter%3Drank%2Ctabcloud%7Ccpro%5Ftemplate%3DbaiduTlinkInlay%7Ccpro%5Fversion%3D2%2E0","encode_userdefine":"encoded","complement_type":1,"update":"1531797015_1532492600"},"extends":{"ssph":200,"sspw":240},"pdb_deliv":{"deliv_id":"0","deliv_des":{},"brandad":0},"order_deliv":{"deliv_id":"0","demand_id":"0"},"rtb_deliv":{"deliv_id":"0","demand_id":"3484575"},"media_protect":"","adExpire":1552320694093}',
                                       1],
                                      [u'_taxac_exp', u'1552322490688::1552407090031', 1],
                                      [u'_taxfp', u'1496507183,1129330842::1583856689853', 1],
                                      [u'_taxtax_vi',
                                       u'aae3d3750b38f4adeb028313421d71bd|1552320815978::1552925615974',
                                       1],
                                      [u'___ds_storage__isblock', u'0|1552320690358', 1],
                                      [u'___ds_storage__isblockone', u'1|1552320689832', 1]]},
            u'url': u'https://www.sina.com.cn/?from=kandian',
            u'value': u'(function() {\nreturn ({"content":[{"ad_id":"bottom_15e9abe0e323967c7f3115b932948174","link":[],"monitor":[],"pv":["//saxn.sina.com.cn/view?type=bottom&t=UERQUzAwMDAwMDA0NTk3Ng==","//sax.sina.com.cn/view?type=nonstd&t=TkEwMDAxMTI0NA%3D%3D"],"src":["//www.sina.com.cn/iframe/www/focuspic.html"],"type":["url"]}],"id":"PDPS000000045976","logo":"","size":"240*350","template":"","type":"embed"})\n})'}
