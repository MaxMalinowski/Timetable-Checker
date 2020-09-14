import codecs
import json
import datetime


class Parser(Exception):

    table_file = "/.config/tmp.html"
    res_dict_one = dict()
    res_dict_two = dict()
    __dir = None

    def __init__(self, directory):
        self.__dir = directory
        pass

    def __print_dict(self, print_dict, name):
        with open(self.__dir + ".config/" + name + ".json", "w") as json_file:
            json.dump(print_dict, json_file, indent=4, sort_keys=True)

    def __construct_item(self):
        tmp = dict()
        tmp['start'] = None
        tmp['end'] = None
        tmp['title'] = str()
        tmp['desc'] = list()
        return tmp

    def extract_grob(self):
        with codecs.open(self.__dir + ".config/tmp.html", "r", encoding='utf-8') as file:
            html_line = file.readline()
            count = 1
            while html_line:
                if "dxscDateHeader dxsc-date-hr" in html_line:
                    self.res_dict_one[html_line[html_line.find("title=")+8:html_line.find(">")-1]] = list()
                if "dxsc-apt-content-layer" in html_line:
                    entry = self.__construct_item()
                    creation = True
                    count = count + 1
                    while creation:
                        html_line = file.readline()
                        if "lblStartTime" in html_line:
                            time_str = file.readline().strip()[:-2]
                            entry['start'] = datetime.datetime.strptime(time_str, '%I:%M %p')
                        elif "lblEndTime" in html_line:
                            time_str = file.readline().strip()
                            entry['end'] = datetime.datetime.strptime(time_str, '%I:%M %p')
                        elif "lblTitle" in html_line:
                            entry['title'] = file.readline().strip()
                        elif "lblDescription" in html_line:
                            while "</span>" not in html_line:
                                html_line = file.readline().strip()
                                entry['desc'].append(html_line)
                            creation = False
                            curr_key = min(self.res_dict_one.keys())
                            if len(self.res_dict_one[curr_key]) != 0:
                                if self.res_dict_one[curr_key][-1]['end'] < entry['start']:
                                    self.res_dict_one[curr_key].append(entry)
                                else:
                                    self.res_dict_two[curr_key] = list()
                                    self.res_dict_two[curr_key] = self.res_dict_one.pop(curr_key)
                                    for item in self.res_dict_two[curr_key]:
                                        item['start'] = item['start'].strftime("%H:%M")
                                        item['end'] = item['end'].strftime("%H:%M")
                            else:
                                self.res_dict_one[curr_key].append(entry)
                        else:
                            pass
                html_line = file.readline()
        self.res_dict_two[curr_key] = list()
        self.res_dict_two[curr_key] = self.res_dict_one.pop(curr_key)
        for item in self.res_dict_two[curr_key]:
            item['start'] = item['start'].strftime("%H:%M")
            item['end'] = item['end'].strftime("%H:%M")
        self.__print_dict(self.res_dict_one, "res_dict_one")
        self.__print_dict(self.res_dict_two, "res_dict_two")

    def extract_fein(self):
        pass
