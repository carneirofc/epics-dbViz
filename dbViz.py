#!/usr/bin/python3
import re

class Record():
    def __init__(self, raw_str):
        self.raw_str = raw_str
        self.name = ''
        self.type = ''
        self.process()
        self.str_filter = re.compile(r'(?!__|name|type|process|str_filter|raw_str)')

    def __str__(self):
        return '<Record %s\t%s\t%s>' % \
            (self.type, self.name,['%s=%s'%(attr,getattr(self, attr)) for attr in dir(self) \
                if self.str_filter.match(attr)])

    def process(self):
        # não está pegando tudo !
        rec = re.findall(r'record[^)]*\)', self.raw_str )[0]
        self.type = re.sub(r'record\(', '', rec.replace(' ', '').split(',')[0])
        self.name = re.sub(r'"\).*|"', '', rec.replace(' ', '').split(',')[1])

        for field in re.findall(r'field[^)]*\)', self.raw_str ):
            setattr(self,
                re.sub(r'field\s*\(\s*|\s*,.*', '', field).strip(),
                re.sub(r'[^,]*,|"\s*\)|\s*"', '', field).strip())

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
 
g = Digraph('G', filename='db.gv') 

for r in db.records.values():
    attrs = ['FLNK','OUT','INP','INPA']
    for attr in attrs:
        p_to = db.points_to(r.name, [attr])
        if p_to:
            for p in p_to:
                if not 'Const'in p:
                    g.edge(p.replace(':',' '),r.name.replace(':',' '),label=attr)
                    # print(p, r.name,attr)
    # if p_to:
    #     print('Attr %s from %s -> %s' % (attrs, p_to, r.name))
g.view()

# python3 -m xdot db.gv
