# This is helper class that helps extracting SPO (Subject Predicate Object) from text

import spacy
import textacy

class SPOExtraction:

    def retrieve_spos(self, input):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(input)

        extracted_text = textacy.extract.triples.subject_verb_object_triples(doc)
        return list(extracted_text)

