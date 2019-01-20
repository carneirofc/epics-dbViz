#!/usr/bin/python3
# structs_revisited.py - http://www.graphviz.org/pdf/dotguide.pdf Figure 12

# from graphviz import Digraph

# s = Digraph('structs', filename='structs_revisited.gv', node_attr={'shape': 'record'})

# s.node('struct1', '<f0> left|<f1> middle|<f2> right')
# s.node('struct2', '<f0> one|<f1> two')
# s.node('struct3', r'hello\nworld |{ b |{c|<here> d|e}| f}| g | h')

# s.edges([('struct1:f1', 'struct2:f0'), ('struct1:f2', 'struct3:here')])

# s.view()

# from graphviz import Digraph

# f = Digraph('finite_state_machine', filename='fsm.gv')
# f.attr(rankdir='LR', size='8,5')

# f.attr('node', shape='doublecircle')
# f.node('LR_0')
# f.node('LR_3')
# f.node('LR_4')
# f.node('LR_8')

# f.attr('node', shape='circle')
# f.edge('LR_0', 'LR_2', label='SS(B)')
# f.edge('LR_0', 'LR_1', label='SS(S)')
# f.edge('LR_1', 'LR_3', label='S($end)')
# f.edge('LR_2', 'LR_6', label='SS(b)')
# f.edge('LR_2', 'LR_5', label='SS(a)')
# f.edge('LR_2', 'LR_4', label='S(A)')
# f.edge('LR_5', 'LR_7', label='S(b)')
# f.edge('LR_5', 'LR_5', label='S(a)')
# f.edge('LR_6', 'LR_6', label='S(b)')
# f.edge('LR_6', 'LR_5', label='S(a)')
# f.edge('LR_7', 'LR_8', label='S(b)')
# f.edge('LR_7', 'LR_5', label='S(a)')
# f.edge('LR_8', 'LR_6', label='S(b)')
# f.edge('LR_8', 'LR_5', label='S(a)')

# f.view()
from graphviz import Digraph

g = Digraph('G', filename='hello.gv')

g.edge('BR-RF-DLLRF-01 SL KP ETRIG','BR-RF-DLLRF-01 SL KP')
# g.edge('BR-RF-DLLRF-01:SL:KP:ETRIG','BR-RF-DLLRF-01:SL:KP')

g.view()