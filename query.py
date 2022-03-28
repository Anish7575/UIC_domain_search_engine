# Name: Sai Anish Garapati
# UIN: 650208577

import pickle, math
from IR_system import text_preprocesser, IR_system


def display_results(i, ranked_docs, page_rank_scores):
    print('\nResults with Cosine Similarity:')
    for key, val in list(ranked_docs.items())[10*i: 10*i + 10]:
        print(key, val)


def display_results_page_rank(i, page_rank_scores, ranked_docs):
    ranked_docs = {key: val for key, val in list(ranked_docs.items())[10*i: 10*i + 10]}
    page_rank_scores = {key: val for key, val in list(page_rank_scores.items()) if key in ranked_docs}
        
    ranked_docs = {key: val for key, val in sorted(ranked_docs.items(), key=lambda x: page_rank_scores[x[0]], reverse=True)}
    
    print('\nResults with Page Rank ordering:')
    for key, val in list(ranked_docs.items()):
        print(key)
    

def take_Query(IR_syst, page_rank_scores):
    while (1):
        i = 0
        page_rank_enable = 0
        input_query = input('\nGive a query (End query with p to rank with page rank). Enter \'stop\' to exit the search:\n')
        if input_query == 'stop':
            break
        if input_query.split(' ')[-1].lower() == 'p':
            page_rank_enable = 1
        ranked_docs = IR_syst.compute_ranked_docs(input_query)
        
        page_rank_scores = {key: val for key, val in sorted(page_rank_scores.items(), key=lambda x: x[1], reverse=True)}
        
        if page_rank_enable == 0:
            display_results(i, ranked_docs, page_rank_scores)
        else:
            display_results_page_rank(i, page_rank_scores, ranked_docs)

        i += 1

        input_choice = input('\nDo you want to display the next 10 more results (yes/no)? ')
        while (input_choice.lower() == 'yes'):
            display_results(i, ranked_docs, page_rank_scores)
            i += 1
            input_choice = input('\nDo you want to display the next 10 results (yes/no)? ')
            if 10*i >= len(ranked_docs):
                print('\nEnd of Documents to rank')
                break


def main():
    with open('inverted_index_temp.pickle', 'rb') as file:
        IR_syst = pickle.load(file)

    with open('page_rank_scores_temp.pickle', 'rb') as file:
        page_rank_scores = pickle.load(file)

    take_Query(IR_syst, page_rank_scores)

if __name__ == '__main__':
    main()
