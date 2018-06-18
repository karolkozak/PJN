from WNQuery import *
import networkx
import matplotlib.pyplot as plt
import math
import data as d

graph = []


def print_synset(wnid):
    print(d.WNQUERY.getSynset(wnid, 'n').toString())


def dfs(wnquery, wnid, pos, rel):
    results = []
    ids = wnquery.lookUpRelation(wnid, pos, rel)
    results.append(wnid)
    print_synset(wnid)
    for i in ids:
        graph.append((wnid, i))
        results.extend(dfs(wnquery, i, pos, rel))
    return results


def injury_meanings_with_synonyms():
    print("Znajdź wszystkie znaczenia rzeczownika szkoda oraz wymień ich synonimy (jeśli posiadają).")
    meanings = d.WNQUERY.lookUpLiteral('szkoda', 'n')
    for meaning in meanings:
        print(meaning.toString())


def transitive_closure_road_accident():
    print(
        "Znajdź domknięcie przechodnie relacji hiperonimi dla pierwszego znaczenia wyrażenia wypadek drogowy i przedstaw je w postaci grafu skierowanego.")
    meaning = d.WNQUERY.lookUpSense('wypadek drogowy', 1, 'n')
    dfs(d.WNQUERY, meaning.wnid, 'n', 'hypernym')
    diGraph = networkx.DiGraph()
    diGraph.add_edges_from(graph)
    plt.figure(figsize=(12, 3))
    networkx.draw_spring(diGraph, with_labels=True)
    plt.show()


def find_direct_hyponyms_of_accident():
    print("Znajdź bezpośrednie hiponimy rzeczownika wypadek1.")
    meaning = d.WNQUERY.lookUpSense('wypadek', 1, 'n')
    relation = d.WNQUERY.lookUpRelation(meaning.wnid, meaning.pos, 'hyponym')
    for meaning in relation:
        print_synset(meaning)


def find_secondary_hyponyms_of_accident():
    print("Znajdź hiponimy drugiego rzędu dla rzeczownika wypadek1.")
    meaning = d.WNQUERY.lookUpSense('wypadek', 1, 'n')
    relation = d.WNQUERY.lookUpRelation(meaning.wnid, meaning.pos, 'hyponym')
    for meaning in relation:
        meaning2 = d.WNQUERY.getSynset(meaning, 'n')
        relation2 = d.WNQUERY.lookUpRelation(meaning2.wnid, meaning2.pos, 'hyponym')
        for rel in relation2:
            print_synset(rel)


def compute_relations(literals):
    synsets = []
    for literal, pos in literals.items():
        synsets.append(d.WNQUERY.lookUpSense(literal, pos, 'n'))
    synsets_ids = [synset.wnid for synset in synsets]
    diGraph = networkx.DiGraph()
    for synset in synsets:
        for target_id, relation_type in synset.ilrs:
            if target_id in synsets_ids:
                diGraph.add_edge(
                    '\n'.join(filter(lambda x: x in literals, [synonym.literal for synonym in synset.synonyms])),
                    '\n'.join(filter(lambda x: x in literals,
                                     [synonym.literal for synonym in d.WNQUERY.lookUpID(target_id, 'n').synonyms])),
                    rel=relation_type)
    plt.figure(figsize=(20, 20))
    pos = networkx.spring_layout(diGraph)
    networkx.draw(diGraph, pos, with_labels=True, arrows=False)
    networkx.draw_networkx_edge_labels(diGraph, pos, label_pos=0.2)
    plt.show()


def show_semantic_relations():
    print(
        "Przedstaw w postaci grafu skierowanego (z etykietami dla krawędzi) relacje semantyczne pomiędzy następującymi grupami leksemów")
    compute_relations(d.TOKENS_GROUP_1)
    compute_relations(d.TOKENS_GROUP_2)


def find_all_measure_Leacock_Chodorow():
    print("Znajdź wartość miary pokrewieństwa semantycznego Leacocka-Chodorowa pomiędzy następującymi parami leksemów:")
    i = 0
    for synset_pair in d.L_C_SYNSETS:
        paths = []
        first_to_top = d.WNQUERY.getReach(synset_pair[0].wnid, 'n', 'hypernym', True)
        second_to_top = d.WNQUERY.getReach(synset_pair[1].wnid, 'n', 'hypernym', True)
        for first_on_path in first_to_top:
            for second_on_path in second_to_top:
                if first_on_path[0] == second_on_path[0]:
                    paths.append(first_on_path[1] + second_on_path[1] - 1)
        distance = min(paths)
        print(d.L_C_NAMES[i] + " " + str(
            -math.log(
                distance / (2.0 * (max(d.WNQUERY.getMaxDepth(wnid, 'n', 'hypernym') for wnid in d.WNQUERY.m_ndat))))))
        i += 1


injury_meanings_with_synonyms()
transitive_closure_road_accident()
find_direct_hyponyms_of_accident()
find_secondary_hyponyms_of_accident()
show_semantic_relations()
find_all_measure_Leacock_Chodorow()
