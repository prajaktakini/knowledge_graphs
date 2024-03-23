import helpers.entity_linking as entity_linking
import helpers.spo_extraction as spo_extraction
import helpers.construct_knowledge_graph as graph

def clean_text(text):
    """
    Returns the cleaned text
    :param text: text to be cleaned e.g. [Bill, Gates]
    :return: cleaned text e.g. Bill Gates
    """
    return ' '.join(str(text).strip("[]").split(", "))

def main():
    input_text = u"Startup companies create jobs and innovation. Bill Gates supports entrepreneurship."

    # 1. Extract SOP Triples
    spo_extraction_obj = spo_extraction.SPOExtraction()
    spo_list = spo_extraction_obj.retrieve_spos(input_text)

    # print(spo_list)

    spo_list_str = []
    for spo in spo_list:
        spo_str = []
        spo_str.append(clean_text(spo[0]))
        spo_str.append(clean_text(spo[1]))
        spo_str.append(clean_text(spo[2]))
        spo_list_str.append(spo_str)

    print(spo_list_str)

    # 2. Establish entity linking
    entity_linking_obj = entity_linking.EntityLinking()
    annotate_result = entity_linking_obj.entity_linking(input_text)

    linking_triplets = []

    for spo in spo_list_str:
        spo_triplet = ['', '', '']
        for resource in annotate_result['Resources']:
            if resource['@surfaceForm'] == clean_text(spo[0]):
                spo_triplet[0] = resource['@URI']
            if resource['@surfaceForm'] == clean_text(spo[1]):
                spo_triplet[1] = resource['@URI']
            if resource['@surfaceForm'] == clean_text(spo[2]):
                spo_triplet[2] = resource['@URI']
        linking_triplets.append(spo_triplet)

    print(linking_triplets)

    # 3. Construct knowledge graph
    graph_obj = graph.Graph()
    graph_construction_result = graph_obj.construct_knowledge_graph(spo_list_str, linking_triplets)


if __name__ == "__main__":
    main()


















