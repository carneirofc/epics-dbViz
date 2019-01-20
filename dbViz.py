#!/usr/bin/python3
import re

class Record():
    def __init__(self, raw_str):
        self.__raw_str = raw_str
        self.name = ''
        self.type = ''
        self.__process()
        self.__str_filter = re.compile(r'(?!_|name|type|node)')
        # self.__node_filter = re.compile(r'(?!_|node)')

    def __str__(self):
        return '<Record %s\t%s\t%s>' % \
            (self.type, self.name,['%s=%s'%(attr,getattr(self, attr)) for attr in dir(self) \
                if self.__str_filter.match(attr)])

    def node(self, digraph):
        lbl = '{%s}'%'|'.join(
                ['{<%s> %s| %s}'%('name','name', getattr(self, 'name'))] +
                ['{<%s> %s| %s}'%('type','type', getattr(self, 'type'))] +
                ['{<%s> %s| %s}'%(attr,attr,getattr(self, attr)) for attr in dir(self) if self.__str_filter.match(attr)])

        digraph.node(self.name.replace(':',' '), shape='record',label=lbl)

    def __process(self):
        # não está pegando tudo !
        rec = re.findall(r'record[^)]*\)', self.__raw_str )[0]
        self.type = re.sub(r'record\(', '', rec.replace(' ', '').split(',',1)[0])
        self.name = re.sub(r'"\).*|"', '', rec.replace(' ', '').split(',',1)[1])

        # for field in re.findall(r'field[^)]*\)', self.__raw_str ):
        for field in re.findall(r'field.+?(?<=")\)', self.__raw_str ):
            f_splt = field.split(',',1)
            setattr(self,
                re.sub(r'field\s*\(\s*', '', f_splt[0]).strip(),
                re.sub(r'"\s*\)|\s*"', '', f_splt[1]).strip())

class Database():

    def __init__(self, sub = {}):
        self.lines = []
        self.data = ''
        self.sub = sub
        self.records = {}
        self.sub_dict = {}

    def __str__(self):
        return '<Database Sub=%s RecordsQty=%s >' % \
            (self.sub_dict, len(self.records))

    def print_records(self):
        for val in sorted([rec for rec in self.records.values()],\
            key=lambda record: record.type if hasattr(record, 'type') else ''):
            print(val)

    def load(self, f_name):
        with open(f_name, 'r') as f:
            for line in f.readlines():
                self.lines.append(re.sub(r'[#].*|\n|\t', '', line).strip())

        self.data = ''.join(self.lines)
        for k, v in self.sub_dict.items():
            self.data = self.data.replace(k, v)

        self.update_records()

    def get_record(self, record_name):
        return self.records.get(record_name, None)

    def update_records(self):
        aux = set(re.findall(r'\$\([^\)]*\)', self.data))
        if aux:
            for s in aux:
                self.data = self.data.replace(s, '%s' % re.sub(r'[^\d\w\.\-\:]', '',s))

        for raw_str in re.findall(r'record[^}]*}', self.data):
            rec = Record(raw_str)
            if rec.name in self.records.keys():
                self.merge_record(rec)
            else:
                self.records[rec.name] = rec

    def merge_record(self, new_rec):
        for attr in dir(new_rec):
            if not attr.startswith('__'):
                setattr(self.records[new_rec.name], attr, getattr(new_rec, attr))

    def points_to(self, record, fields):
        connections = set()
        rec = self.get_record(record)
        rec.regex = re.compile(r'^{}\.*(\s*|\s+\w*)$'.format(rec.name))
        for r in self.records.values():
            if rec.name != r.name:
                for field in fields:
                    if hasattr(r, field) and (rec.regex.match(getattr(r, field))):
                        connections.add(r.name)
        return connections


db = Database()
# db.sub_dict['BR-RF-DLLRF-01'] = '$(device)'
db.load('db')

from graphviz import Digraph
s = Digraph('structs', filename='db.dot', node_attr={'shape': 'record'})
for r in db.records.values():
    # if r.type == 'calc' or r.type == 'calcout':
    if ':CAV:' in  r.name and not 'Const' in r.name:
        r.node(s)
s.view()
# g = Digraph('G', filename='db.dot')

# for r in db.records.values():
#     attrs = ['INP','INPA','INPB','INPC','INPD','INPE','INPF','INPG','INPH','INPI']
#     for attr in attrs:
#         p_to = db.points_to(r.name, [attr])
#         if p_to:
#             for p in p_to:
#                 if not 'Const'in p:
#                     g.edge(r.name.replace(':',' '),p.replace(':',' '),label=attr)
#                     # print(p, r.name,attr)

# g.view()

# kgraphviewer kgraphviewer-dev
# sfdp -x -Goverlap=scale -Tx11 -Tpng db.dot > db.png
# sfdp -x -Goverlap=scale -Tx11 
# ./dbViz.py && sfdp -x -Goverlap=scale -Tx11 -Tpng db.dot