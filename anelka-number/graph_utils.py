import pickle

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class AnelkaNumberGraph:

    @staticmethod
    def get_graph(existing_graph_path, transfer_data_path):
        graph = None
        try:
            with open(existing_graph_path, "rb") as f:
                graph = pickle.load(f)
        except Exception:
            pass

        if not graph:
            graph = AnelkaNumberGraph(transfer_data_path)
            with open(existing_graph_path, "wb") as f:
                pickle.dump(graph, f)
        
        return graph


    def __init__(self, transfer_data_path):
        self._initialise_graph(transfer_data_path)
    

    def _initialise_graph(self, transfer_data_path):
        self.graph = nx.Graph()
        self.transfers = pd.read_csv(transfer_data_path)

        # calculate all edges
        grouped = self.transfers.groupby(["club_name", "season"])

        # add edges for each group of players within a season
        for (club, season), group in grouped:
            players = group["player_name"].tolist()
            for i, player1 in enumerate(players):
                for player2 in players[i + 1:]:
                    self.graph.add_edge(player1, player2, club=club, season=season)
        
        self.anelka_numbers = nx.single_source_shortest_path_length(self.graph, "NICOLAS ANELKA")
    

    def get_players(self):
        return sorted(self.anelka_numbers.keys())


    def get_anelka_number(self, player):
        return self.anelka_numbers[player]
    
    
    def get_all_anelka_number_graphs(self, player):
        """
        Returns all shortest paths between Nicolas Anelka and a player, combining them into a single graph
        """
        paths = list(nx.all_shortest_paths(self.graph, "NICOLAS ANELKA", player))

        subgraph = nx.Graph()
        for path in paths:
            subgraph.add_nodes_from(path)
            for u, v in zip(path, path[1:]):  # Consecutive nodes in the path
                if self.graph.has_edge(u, v):  # Check if edge exists
                    # Copy edge with data
                    subgraph.add_edge(u, v, **self.graph[u][v])
            
        return subgraph
    

    def get_anelka_number_graph(self, player):
        """
        Returns ONE shortest path between Nicolas Anelka and another player
        """
        path = nx.shortest_path(self.graph, "NICOLAS ANELKA", player)

        subgraph = nx.Graph()
        subgraph.add_nodes_from(path)
        for u, v in zip(path, path[1:]):  # Consecutive nodes in the path
            if self.graph.has_edge(u, v):  # Check if edge exists
                # Copy edge with data
                subgraph.add_edge(u, v, **self.graph[u][v])
            
        return subgraph


    def plot_anelka_number_graph(self, player, only_one=True):
        subgraph = None
        if only_one:
            subgraph = self.get_anelka_number_graph(player)
        else:
            subgraph = self.get_all_anelka_number_graphs(player)
        
        fig, axis = plt.subplots(figsize=(13, 8))

        # Anelka and the target player get their own colours
        color_map = {'NICOLAS ANELKA': 'orange', player: 'green'}
        default_color = 'lightblue'

        node_colors = [
            color_map.get(node, default_color)
            for node in subgraph.nodes()
        ]

        pos = nx.spring_layout(subgraph)
        nx.draw(subgraph,
                pos,
                with_labels=True,
                node_color=node_colors,
                edge_color='gray',
                ax=axis)

        # Add edge labels with data
        edge_labels = nx.get_edge_attributes(subgraph, 'club')  # Get a specific attribute, e.g., 'club'
        nx.draw_networkx_edge_labels(subgraph,
                                     pos,
                                     edge_labels=edge_labels,
                                     ax=axis)
        fig.tight_layout()
        return fig