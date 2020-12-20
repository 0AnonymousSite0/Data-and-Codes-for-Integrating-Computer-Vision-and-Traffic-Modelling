

import rdflib
from rdflib import Graph
from scipy.special import comb, perm
from itertools import combinations

g = Graph()
g.parse(r'/Users/shenghua/Desktop/ontology/ontology.owl')
deleted_str=r"http://www.semanticweb.org/zhou/ontologies/2020/3/untitled-ontology-19#"
len_deleted_st=len(deleted_str)



query = """
SELECT * WHERE {
        ?s rdfs:range ?o .
}
"""

query_class = """
SELECT ?o WHERE {
        ?s rdfs:subClassOf ?o .
}
"""


query1 = """SELECT ?downp ?downq ?action WHERE { 
    ?action rdfs:domain ?dp.
    ?action rdfs:range ?rq.
    ?dcp rdfs:subClassOf ?dp.
    ?rcq rdfs:subClassOf ?rq.
    ?downp rdfs:subClassOf ?dcp.
    ?downq rdfs:subClassOf ?rcq.
    
}
"""

query2 = """SELECT  ?dp ?rq ?action WHERE { 
    ?action rdfs:domain ?dcp.
    ?action rdfs:range ?rcq.
    ?dp rdfs:subClassOf ?dcp.
    ?rq rdfs:subClassOf ?rcq.

    
}
"""

query3 = """SELECT ?dcp ?downq ?action WHERE { 
    ?action rdfs:domain ?dp.
    ?action rdfs:range ?rq.
    ?dcp rdfs:subClassOf ?dp.
    ?rcq rdfs:subClassOf ?rq.
    ?downq rdfs:subClassOf ?rcq.

}
"""

query4 = """SELECT  ?downp ?rcq ?action WHERE { 
    ?action rdfs:domain ?dp.
    ?action rdfs:range ?rq.
    ?dcp rdfs:subClassOf ?dp.
    ?rcq rdfs:subClassOf ?rq.
    ?downp rdfs:subClassOf ?dcp.
  
}
"""


#print (g.subject_objects(predicate=None))


a=[]
for row in g.query(query):
    for i in range(0,len(row)):
        if (str(row[0])[len_deleted_st:])=='detect':
            #print(str(row[1])[len_deleted_st:])
            a.append(str(row[1])[len_deleted_st:])
#print (set(a))

detected_elements=set(a)
print ("detected_elements:")
print (detected_elements)

allclass=[]
for row in g.query(query_class):
    allclass.append(str(row[0])[len_deleted_st:])
all_high_level_class=set(allclass)
print (all_high_level_class)



track=[]
for row in g.query(query):
    for i in range(0,len(row)):
        if (str(row[0])[len_deleted_st:])=='track':
            #print(str(row[1])[len_deleted_st:])
            track.append(str(row[1])[len_deleted_st:])
#print (set(a))

tracked_elements=set(track)
print ("tracked_elements:")
print (tracked_elements)

detected_or_tracked_elements=tracked_elements.union(detected_elements)

d=[]
for row in g.query(query1): #3-3
    for i in range(0,len(row)):

        if  ((str(row[2])[len_deleted_st:len_deleted_st+6])=='affect')and ((str(row[0])[len_deleted_st:]) !=(str(row[1])[len_deleted_st:]) )and ((str(row[0])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[1])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[0])[len_deleted_st:]) not in all_high_level_class) and ((str(row[1])[len_deleted_st:]) not in all_high_level_class):
            #print(str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:])
            d.append((str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:]))
            #print(len(d))
affected_elements_3_3=set(d)
print("affected_elements_3_3")
print(affected_elements_3_3)

d=[]
for row in g.query(query2): #2-2
    print (row)
    for i in range(0,len(row)):
        if  ((str(row[2])[len_deleted_st:len_deleted_st+6])=='affect')and ((str(row[0])[len_deleted_st:]) !=(str(row[1])[len_deleted_st:]) )and ((str(row[0])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[1])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[0])[len_deleted_st:]) not in all_high_level_class) and ((str(row[1])[len_deleted_st:]) not in all_high_level_class):
            #print(str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:])
            d.append((str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:]))
            print(d)
            #print(len(d))
affected_elements_2_2=set(d)
print("affected_elements_2_2")
print(affected_elements_2_2)

d=[]

for row in g.query(query3): #2-3
    for i in range(0,len(row)):
        if  ((str(row[2])[len_deleted_st:len_deleted_st+6])=='affect')and ((str(row[0])[len_deleted_st:]) !=(str(row[1])[len_deleted_st:]) )and ((str(row[0])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[1])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[0])[len_deleted_st:]) not in all_high_level_class) and ((str(row[1])[len_deleted_st:]) not in all_high_level_class):
            #print(str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:])
            d.append((str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:]))
            #print(len(d))
affected_elements_2_3=set(d)
print("affected_elements_2_3")
print(affected_elements_2_3)

d=[]
for row in g.query(query4): #3-2
    for i in range(0,len(row)):
        if  ((str(row[2])[len_deleted_st:len_deleted_st+6])=='affect')and ((str(row[0])[len_deleted_st:]) !=(str(row[1])[len_deleted_st:]) )and ((str(row[0])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[1])[len_deleted_st:]) in (detected_or_tracked_elements)) and ((str(row[0])[len_deleted_st:]) not in all_high_level_class) and ((str(row[1])[len_deleted_st:]) not in all_high_level_class):
            #print(str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:])
            d.append((str(row[0])[len_deleted_st:],str(row[1])[len_deleted_st:]))
            #print(len(d))
affected_elements_3_2=set(d)
print("affected_elements_3_2")
print(affected_elements_3_2)


affected_elements=((affected_elements_3_3.union(affected_elements_2_2)).union(affected_elements_3_2)).union(affected_elements_2_3)
set(affected_elements)
print ("affected_elements")
for i in affected_elements:
    print(i)
print (affected_elements)
print (len(affected_elements))
potential_applications=[]
number_of_potential_applications=0
for j in range(1, len(affected_elements)+1):
    number_of_potential_applications=number_of_potential_applications+comb(len(affected_elements), i)

print (number_of_potential_applications)
for p in list(combinations(affected_elements, 3)):
    potential_applications.append(p)


