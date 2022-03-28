# Name: Sai Anish Garapati
# UIN: 650208577

class PageRank:
    def __init__(self, epsilon, max_iterations):
        self.epsilon = epsilon
        self.max_iterations = max_iterations
    
    def compute_page_rank_scores(self, web_graph, index_table):
        print(len(web_graph))
        tot_nodes = len(index_table)
        
        for link in index_table.keys():
            tot_nodes += len(web_graph[link])
        
        rankScore = {webpage: 1/tot_nodes for webpage in index_table.keys()}

        for i in range(self.max_iterations):
            tmp_rankScore = {}
            for from_link in index_table.keys():
                for to_link in web_graph[from_link]:
                    if to_link not in tmp_rankScore:
                        tmp_rankScore[to_link] = 0
                    tmp_rankScore[to_link] += (rankScore[from_link]/len(web_graph[from_link]))
            
            for link in index_table.keys():
                if link in tmp_rankScore:
                    tmp_rankScore[link] += (self.epsilon/tot_nodes + (1 - self.epsilon) * tmp_rankScore[link])

            rankScore = tmp_rankScore

        rankScore = {key: val for key, val in rankScore.items() if key in index_table}
        return rankScore