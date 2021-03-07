import codecs
import json
import datetime


class Parser(Exception):

    table_file = "/.config/tmp.html"
    res_dict_one = dict()
    res_entry_list = list()
    data_dict = dict()
    __dir = None

    def __init__(self, directory):
        self.__dir = directory
        pass

    def __print_dict(self, print_dict, name):
        with open(self.__dir + ".config/" + name + ".json", "w") as json_file:
            json.dump(print_dict, json_file, indent=4, sort_keys=True)

    def __construct_item_grob(self):
        tmp = dict()
        tmp['start'] = None
        tmp['end'] = None
        tmp['title'] = str()
        tmp['desc'] = list()
        return tmp
    
    def __construct_item_fein(self, item_grob):
        tmp = dict()
        tmp['subject'] = str()
        tmp['topic'] = str()
        tmp['room'] = str()
        tmp['teacher'] = str()
        tmp['start'] = item_grob["start"]
        tmp['end'] = item_grob["end"]
        return tmp

    def extract_grob(self):
        # read html file
        with codecs.open(self.__dir + ".config/tmp.html", "r", encoding='utf-8') as file:
            html_line = file.readline()
            # for every line
            while html_line:
                # if section contains date
                if "dxscDateHeader dxsc-date-hr" in html_line:
                    self.res_dict_one[html_line[html_line.find("title=")+7:html_line.find(">")-1]] = list()
                # if section contains subject info
                elif "dxsc-apt-content-layer" in html_line:
                    # construct empty item
                    entry = self.__construct_item_grob()
                    # while item is not created
                    creation = True
                    while creation:
                        html_line = file.readline()
                        # if line contains start time
                        if "lblStartTime" in html_line:
                            time_str = file.readline().strip()[:-2]
                            entry['start'] = datetime.datetime.strptime(time_str, '%I:%M %p')
                        # if line contains end time
                        elif "lblEndTime" in html_line:
                            time_str = file.readline().strip()
                            entry['end'] = datetime.datetime.strptime(time_str, '%I:%M %p')
                        # if line contains subject title 
                        elif "lblTitle" in html_line:
                            entry['title'] = file.readline().strip()
                        # if line contains add info
                        elif "lblDescription" in html_line:
                            # append all lines
                            while "</span>" not in html_line:
                                html_line = file.readline().strip()
                                if "</span>" not in html_line and "<br/>" not in html_line:
                                    entry['desc'].append(html_line)
                            # item created
                            creation = False
                    # append final entry to list
                    self.res_entry_list.append(entry)
                # read next line
                html_line = file.readline()
        
        # key number
        key_no = 0
        # get current key
        key = list(self.res_dict_one.keys())[key_no]
        # for every item in linst
        for item in self.res_entry_list:
            # format datetime to string
            item['start'] = item['start'].strftime("%H:%M")
            item['end'] = item['end'].strftime("%H:%M")
            # if start time of item smaller than last, next day
            if len(self.res_dict_one[key]) != 0:
                if self.res_dict_one[key][-1]['end'] > item['start']:
                    key_no += 1
                    key = list(self.res_dict_one.keys())[key_no]
            # append item to dict
            self.res_dict_one[key].append(item)
        # safe dict 
        self.__print_dict(self.res_dict_one, "res_dict_one")


    def extract_fein(self):
        # fine grained extraction for every entry
        for key in self.res_dict_one:
            self.data_dict[key] = list()
            for entry in self.res_dict_one[key]:
                # get a fine entry prefilled
                data_entry = self.__construct_item_fein(entry)

                if len(entry['desc']) == 3:
                    data_entry['subject'] = ' '.join(entry['desc'][0].split(" ")[1:])
                    data_entry['topic'] = ' '.join(entry['desc'][1].split(" ")[1:])
                    data_entry['teacher'] = ' '.join(entry['desc'][2].split(" ")[1:])
                elif len(entry['desc']) == 1:
                    data_entry['subject'] = ' '.join(entry['desc'][0].split(" ")[1:])
                    data_entry['topic'] = None
                    data_entry['teacher'] = None
                else: 
                    data_entry['subject'] = None
                    data_entry['topic'] = None
                    data_entry['teacher'] = None

                # extract room
                data_entry['room'] = entry['title'][entry['title'].find('(')+1:entry['title'].find(')')]

                self.data_dict[key].append(data_entry)
        # safe dict 
        self.__print_dict(self.data_dict, "data_dict")
