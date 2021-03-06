# -*- coding: utf-8 -*-

import httplib2
import urllib2
import json
import base64
import csv
import time


id = 'id'
pw = 'pw'

file_path = 'file_path'
korea_user_file_name = 'korea_user_file_name'
location_count_file_name = 'location_count_file_name'
date = time.strftime('%x', time.localtime(time.time())).replace('/', '')
korea_user_file_name = korea_user_file_name + date + '.csv'
location_count_file_name = location_count_file_name + date + '.csv'

start_date = '2007-10-01'
end_date = '2017-09-26'

line_point = '*'*150
double_line_point = line_point + '\n' + line_point



def Request(url):
    http = httplib2.Http()
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url, 'GET', headers={'Authorization': 'Basic ' + auth})


location_count_dict = {}
del_list = []
def total_search_location(location_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                    del_list=del_list, location_count_dict=location_count_dict):
    print double_line_point
    print '\t' + location_name
    f_open = open(file_path + location_user_data_file_name, 'a')
    f = csv.writer(f_open)
    page = 1
    while page <= 10:
        q_location_name = urllib2.quote(location_name)
        url = 'https://api.github.com/search/users?q=location:' + q_location_name + '&per_page=100&page=' + str(page)
        print line_point
        print location_name + ' / page = ' + str(page)
        while 1:
            print url
            respones, content = Request(url)
            j_data = json.loads(content)
            # print(j_data)
            try:
                if j_data['incomplete_results'] != 0:
                    print '\t!!!!....incomplete_results....!!!!'
                    continue
            except:
                pass
            try:
                if j_data['items'] == []:
                    print '\t!!!!....empty items....!!!!'
                    f_open.close()
                    return None
            except:
                pass
            try:
                if j_data['message'] == 'API rate limit exceeded for ' + id + '.':
                    print '\t!!!!....limit reached....!!!!'
                    time.sleep(4)
                    continue
            except:
                pass
            location_count_dict[location_name] = j_data['total_count']
            print '\t\t' + location_name + '_count : ', j_data['total_count']
            if j_data['total_count'] <= 1000:
                for j in range(len(j_data['items'])):
                    if j_data['items'][j]['id'] not in del_list:
                        print j_data['items'][j]['login'], j_data['items'][j]['id'], location_name
                        del_list.append(j_data['items'][j]['id'])
                        f.writerow([j_data['items'][j]['login'], j_data['items'][j]['id'], location_name])
                if len(j_data['items']) != 100:
                    f_open.close()
                    return None
                else:
                    page += 1
            else:
                f_open.close()
                return 'day_fn_start'
            break
    f_open.close()
    return None


def day_search_location(location_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                    del_list=del_list, start_date=start_date, end_date=end_date):
    print double_line_point
    print '\t' + location_name
    swtich_value = 0
    f_open = open(file_path + location_user_data_file_name, 'a')
    f = csv.writer(f_open)
    for year in range(2007, 2018):
        str_year = str(year)
        for month in range(1, 13):
            str_month = str(month)
            if len(str_month) == 1:
                str_month = '0' + str_month
            for day in range(1, 32):
                str_day = str(day)
                if len(str_day) == 1:
                    str_day = '0' + str_day
                str_date = str_year + '-' + str_month + '-' + str_day
                if str_date == start_date:
                    swtich_value = 1
                if str_date == end_date:
                    f_open.close()
                    return None

                if swtich_value == 1:
                    page = 1
                    while page <= 10:
                        q_location_name = urllib2.quote(location_name)
                        q_str_date = urllib2.quote(str_date)
                        url = 'https://api.github.com/search/users?q=location:' + q_location_name + '+created:' \
                              + q_str_date + '&per_page=100&page=' + str(page)
                        print line_point
                        print str_date + ' / page = ' + str(page)
                        while 1:
                            print url
                            respones, content = Request(url)
                            j_data = json.loads(content)
                            # print(j_data)
                            try:
                                if j_data['incomplete_results'] != 0:
                                    print '\t!!!!....incomplete_results....!!!!'
                                    continue
                            except:
                                pass
                            try:
                                if j_data['message'] == "Validation Failed":
                                    page = 11
                                    print '\t!!!!....Validation Failed....!!!!'
                                    break
                            except:
                                pass
                            try:
                                if j_data['items'] == []:
                                    page = 11
                                    print '\t!!!!....empty items....!!!!'
                                    break
                            except:
                                pass
                            try:
                                if j_data['message'] == 'API rate limit exceeded for ' + id + '.':
                                    print '\t!!!!....limit reached....!!!!'
                                    time.sleep(4)
                                    continue
                            except:
                                pass
                            for j in range(len(j_data['items'])):
                                if j_data['items'][j]['id'] not in del_list:
                                    print j_data['items'][j]['login'], j_data['items'][j]['id'], location_name
                                    del_list.append(j_data['items'][j]['id'])
                                    f.writerow([j_data['items'][j]['login'], j_data['items'][j]['id'], location_name])
                            if len(j_data['items']) != 100:
                                page = 11
                            else:
                                page += 1
                            break
    f_open.close()



start = time.time()
location_list = ['한국', '대한민국', '서울', 'seoul', 'korea']
with open(file_path + korea_user_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['user_name', 'user_id', 'search_location'])

with open(file_path + location_count_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['location_name', 'total_count'])
    
for l_name in location_list:
    day_val = total_search_location(location_name=l_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                          del_list=del_list, location_count_dict=location_count_dict)
    if day_val == 'day_fn_start':
        day_search_location(location_name=l_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                    del_list=del_list, start_date=start_date, end_date=end_date)

print double_line_point + '\n'

with open(file_path + location_count_file_name, 'a') as f_open:
    f = csv.writer(f_open)
    for l_name in location_list:
        print l_name +'_count : ', location_count_dict[l_name]
        f.writerow([l_name, location_count_dict[l_name]])

end = time.time()

print '\n\n' + double_line_point + '\n\nRunning_Time : %0.4f'%((end-start)/3600) + 'h\n\n' + double_line_point
