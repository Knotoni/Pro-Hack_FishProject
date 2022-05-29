from pyvis.network import Network
import csv
import random

def read():
    with open('test_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        row = [row for row in reader]
        return row

def main():
    l = []
    sp = ["red", "blue", "green"]
    rd = read()
    network = Network('1500px', '1500px')
    for count, i in enumerate(rd):
        i = "".join(i)
        i = i.split(",")[3]
        if i not in l and "P" not in i:
            network.add_node(count, label=i, title='title', color=random.choice(sp))
            l.append(i)

    for i, count in enumerate(l):
        r = random.randint(0, 1)
        if r == 1:
            try:
                network.add_edge(i, i + 1)
            except:
                pass

    network.toggle_physics(False)
    network.show('templates/graph.html')

main()