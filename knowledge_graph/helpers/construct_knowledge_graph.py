# Construct the graph using the extracted SPO triples

from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config, StructuredRel

config.DATABASE_URL = "bolt://neo4j:user@1234@localhost:7687"

class Relationship(StructuredRel):
    DBpeadiaURL = StringProperty()
    relationType = StringProperty()

class Object(StructuredNode):
    object_name = StringProperty(unique_index=True)
    DBpeadiaURL = StringProperty()


class Subject(StructuredNode):
    subject_name = StringProperty(unique_index=True)
    DBpeadiaURL = StringProperty()
    predicate = RelationshipTo(Object, 'predicate', model=Relationship)


class Graph:
    def construct_knowledge_graph(self, spolist, entity_linking):
        print("Constructing knowledge graph")

        for index in range(len(spolist)):
            spo = spolist[index]

            sub_dbpeadia_url = entity_linking[index][0]
            obj_dbpeadia_url = entity_linking[index][2]

            # Check if subject node already exists
            subject = Subject.nodes.first_or_none(subject_name=spo[0])
            subject_temp = None
            if subject == None:
                subject_temp = Subject(subject_name=spo[0], DBpeadiaURL=sub_dbpeadia_url).save()
            else:
                subject_temp = subject

            # Check if object node already exists
            object = Object.nodes.first_or_none(object_name=spo[2])
            object_temp = None
            if object == None:
                object_temp = Object(object_name=spo[2], DBpeadiaURL=obj_dbpeadia_url).save()
            else:
                object_temp = object

            # if subject_temp.predicate.is_connected(object_temp):
            #     relation = subject_temp.predicate.relationship(object_temp)
            #     print("Relation name ", relation.predicateName)

            # Set the relation details between subject and object
            subject_temp.predicate.definition['relation_type'] = spo[1]
            relationship = subject_temp.predicate.connect(object_temp)
            relationship.relationType = spo[1]
            relationship.DBpeadiaURL = entity_linking[index][1]
            relationship.save()

        subject_nodes = Subject.nodes.all()
        object_nodes = Object.nodes.all()

        for node in subject_nodes:
            print(node)

        for node in object_nodes:
            print(node)

    def delete_nodes(self):
        subject_nodes = Subject.nodes.all()
        object_nodes = Object.nodes.all()

        for node in subject_nodes:
            node.delete()

        for node in object_nodes:
            node.delete()



