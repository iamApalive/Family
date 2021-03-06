# -*- coding: UTF-8 -*-
# /**
# * Software Name : family
# * Version : 0.1.0
# *
# * Copyright 2020. PUNDIR ASHISH.
# *
# *--------------------------------------------------------
# * File Name : family/family.py
# * Created : 2020-06-28
# * Authors : PUNDIR ASHISH
# *--------------------------------------------------------
# */

from src.family import person
from src.family.constants import Sex, Message, RelationShip


class Family:
    """
    Class representing Family
    """

    def __init__(self, name, gender=Sex.Male):
        self.family_head = self.create_member(name, gender)
        self.relationship_map = {
            RelationShip.SON: self.search_son,
            RelationShip.DAUGHTER: self.search_daughters,
            RelationShip.SIBLINGS: self.search_siblings,
            RelationShip.BROTHER_IN_LAW: self.search_brother_in_law,
            RelationShip.SISTER_IN_LAW: self.search_sister_in_law,
            RelationShip.MATERNAL_AUNT: self.search_maternal_aunt,
            RelationShip.PATERNAL_AUNT: self.search_paternal_aunt,
            RelationShip.PATERNAL_UNCLE: self.search_paternal_uncle,
            RelationShip.MATERNAL_UNCLE: self.search_maternal_uncle,
        }

    def get_relationship(self, relationship, person_name):
        """
        get relationshipt based on relationship map and return the output.
        :param relationship: output of relationship to be provided
        :param person_name: person name to realate to.
        :return: relationship output
        """
        family_member = self.search_family_member(self.family_head, person_name)

        if family_member is None:
            return Message.PERSON_NOT_FOUND.value
        relationship = eval("RelationShip.%s" % relationship.upper())
        if relationship not in self.relationship_map:
            return Message.PERSON_NOT_FOUND.value
        # call message related to relationship in the relationship map
        relations = self.relationship_map[relationship](person_name)
        # if relations return values, else return NONE
        if len(relations):
            return " ".join(relations)
        else:
            return Message.NONE.value

    @staticmethod
    def get_childrens_from_family(family_head):
        """
        get detailed list of childrens from the family related to family head.
        :param family_head: object of family
        :return: list of childrens of family.
        """
        if family_head.get_sex() == Sex.Female:
            return family_head.get_all_childs()
        elif family_head.is_married():
            return family_head.get_spouse().get_all_childs()
        else:
            return []

    def search_family_member(self, family_head, member_name):
        """
        Search a member in the family based on family head and member names.
        :param family_head: Object of the family head where member to be searched
        :param member_name: name of the family member to be searched.
        :return: return family member object or None if not found.
        """
        if family_head is None or member_name is None:
            return None
        # if member to be searched is head or head spouse.
        if member_name == family_head.name:
            return family_head
        elif family_head.is_married():
            if family_head.get_spouse().name == member_name:
                return family_head.get_spouse()

        # fetch children list for family.
        children_list = self.get_childrens_from_family(family_head)
        # search member in children lists.
        return self.find_member_in_family_members(children_list, member_name)

    def find_member_in_family_members(self, family_members, member_name):
        """
        Find the member in a list of family members members
        :param family_members:list of member to search by membername
        :param member_name: name of member to be searched.
        :return:
        """
        found_member = None
        for family_member in family_members:
            found_member = self.search_family_member(family_member, member_name)
            if found_member is not None:
                break
        return found_member

    @staticmethod
    def create_member(member_name, gender):
        """
        Create the member from details provided.
        :param member_name: name of the member.
        :param gender: gender of the member.
        :return:
        """
        if Sex.Male == gender:
            return person.Male(member_name)
        else:
            return person.Female(member_name)

    def add_spouse(self, member_name, spouse_name, spouse_gender):
        """
        add spouse to family in to member with member name,
        :param member_name: name of family member to add spouse to.
        :param spouse_name: Spouse name to be added to family.
        :param spouse_gender: gender of spouse to be added.
        :return: True is succeed, False if fails.
        """
        family_member = self.search_family_member(self.family_head, member_name)
        if family_member is None or family_member.is_married():
            return False

        spouse = self.create_member(spouse_name, spouse_gender)
        return family_member.add_spouse(spouse)

    def add_child(self, mother_name, child_name, gender):
        """
        add child to the family, with mother provided.
        :param mother_name: name of mother to add the child.
        :param child_name: name of the child member to be added.
        :param gender: gender of child to be added.
        :return: result of child addition.
        """
        family_member = self.search_family_member(self.family_head, mother_name)
        if family_member is None:
            return Message.PERSON_NOT_FOUND.value
        # check if family_member is female.
        if child_name is None or gender is None or family_member.is_boy():
            return Message.CHILD_ADDITION_FAILED.value
        child_member = self.create_member(child_name, gender)
        if family_member.add_child(child_member):
            return Message.CHILD_ADDITION_SUCCEEDED.value

    def search_siblings(self, member_name):
        """
        Search the siblings based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        if family_member.get_mother() is None:
            return ""
        return family_member.get_mother().get_siblings(member_name)

    def search_son(self, member_name):
        """
        Search the childs based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        if family_member.is_boy():
            if family_member.is_married():
                return family_member.get_spouse().get_childs(Sex.Male)
            else:
                return []
        return family_member.get_childs(Sex.Male)

    def search_daughters(self, member_name):
        """
        Search the daughter based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        if family_member.is_boy():
            if family_member.is_married():
                return family_member.get_spouse().get_childs(Sex.Female)
            else:
                return []
        return family_member.get_childs(Sex.Female)

    def search_brother_in_law(self, member_name):
        """
        Search the brother in law based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        inlaws = []
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch spouse if not married return empty list.
        siblings = family_member.get_siblings_of(Sex.Female, member_name)
        for sibling in siblings:
            if sibling.is_married():
                inlaws.append(sibling.get_spouse().name)
        if family_member.is_married():
            inlaws.extend(family_member.get_spouse().get_siblings_name(Sex.Male, family_member.get_spouse().name))
        return inlaws

    def search_sister_in_law(self, member_name):
        """
        Search the Sister in law based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        inlaws = []
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch spouse if not married return empty list.
        siblings = family_member.get_siblings_of(Sex.Male,member_name)
        for sibling in siblings:
            if sibling.is_married():
                inlaws.append(sibling.get_spouse().name)
        if family_member.is_married():
            inlaws.extend(family_member.get_spouse().get_siblings_name(Sex.Female,family_member.get_spouse().name))
        return inlaws

    def search_maternal_aunt(self, member_name):
        """
        Search the Maternal Aunt based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch mother if not married return empty list.
        mother = family_member.get_mother()
        if mother is None:
            return []
        return mother.get_siblings_name(Sex.Female,family_member.get_mother().name)

    def search_maternal_uncle(self, member_name):
        """
        Search the Maternal Uncle based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch mother if not married return empty list.
        mother = family_member.get_mother()
        if mother is None:
            return []
        return mother.get_siblings_name(Sex.Male,family_member.get_mother().name)

    def search_paternal_aunt(self, member_name):
        """
        Search the Paternal Aunt based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch spouse if not married return empty list.
        father = family_member.get_father()
        if father is None:
            return []
        return father.get_siblings_name(Sex.Female,family_member.get_father().name)

    def search_paternal_uncle(self, member_name):
        """
        Search the Paternal Uncle based on the member_name.
        :param member_name: gender of the childs.
        :return: list of childs
        """
        family_member = self.search_family_member(self.family_head, member_name)
        # fetch spouse if not married return empty list.
        father = family_member.get_father()
        if father is None:
            return []
        return father.get_siblings_name(Sex.Male,family_member.get_father().name)
