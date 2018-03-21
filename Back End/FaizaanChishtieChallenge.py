import json
from pprint import pprint

'''
    @Author: Faizaan Chishtie
    LinkedIn: in/fchishtie/
    GitHub: /FaizChishtie
'''



class Menu:
    def __init__(self, items):
        '''
        (Menu, Items) -> None
        Class menu takes object Items to create menus to bre processed as valid or invalid.
        self.items: List - contains items list
        self.menus: Dictionary - contains menu that is created by createMenus() method
        self.valid: List - Contains valid menus
        self.invalid: List - Contains invalid menus
        '''
        self.items = items
        self.menus = self.createMenus()
        self.valid = []
        self.invalid = []

    def createMenus(self):
        '''
        (Menu) -> List of root nodes with children as dictionaries
        Takes self.items and transforms it into a list with dictionaries based on the items root node boolean value.
        Sample list of items in: [1,2,3,4,5,6]
        Sample output [{'root': 1, 'children': [1,3,5]}, {'root': 2, 'children': [4,6]}]
        '''
        menus = []
        for node in self.items: #iterates through nodes in items list to find root nodes
            if node.isRoot:
                menu = {} #create dictionary for given root node
                menu["root"] = node
                menu["children"] = []
                menus.append(menu) #append dictionary to list of menus
        for i in range(len(menus)): #iterates through the length of menus established above
        #INITAL SEARCH
            for node in self.items: #iterates through nodes to find children within the root nodes
                if node in menus[i]["root"].children: #if node is contained within root node's children, append to dictionary
                    menus[i]["children"].append(node.id) #appends id to be able to write to JSON
                    for j in range(len(node.children)):
                        menus[i]["children"].append(node.children[j]) #checks children of child above and appends if they exist
        for i in range(len(menus)):
        #FINAL SEARCH
            for j in range(len(menus[i]["children"])): #goes through the existing menus children to do a final search for child nodes
                try: #try except block to catch case where the item does not have a parent ID
                    c = self.items.index(menus[i]["children"][j]) #finds index of children in items list
                    for child in self.items[c].children:
                        if not child in menus[i]["children"]: #if child does not exist in menu dictionary, append
                            menus[i]["children"].append(child)
                except ValueError: #if value error pass
                    pass
        for i in range(len(menus)): #sort the children list within both menus
            menus[i]["children"].sort()
        return menus

    def retMenuValidity(self):
        '''
        (Menu) -> Takes self.menus and returns validity of each given menu based on the presence of root node in children
        '''
        menus = self.menus
        for menu in menus: #iterates through menus to check if root node exist in children
            if menu["root"] in menu["children"]:
                tmp = menu["root"]
                menu["root"] = tmp.id #change root from item to id so that JSON can parse
                self.invalid.append(menu) #append to invalid
            else:
                tmp = menu["root"]
                menu["root"] = tmp.id
                self.valid.append(menu) #append to valid if not invalid

class Item:
    def __init__(self, id):
        '''
        (Item, id) -> None
        Creates item object to store from JSON data file
        self.id: int - contains id of item
        self.isRoot: boolean - true or false based on if item is root or not
        self.parent: int - id of items' parent item
        self.children: list - contains children for the item object
        '''
        self.id = id
        self.isRoot = True
        self.parent = None
        self.children = []

    def __eq__(self, otherId):
        '''
        (Item, otherItem) -> Returns if self.id equals otherId
        '''
        return self.id==otherId

    def addChildren(self, children):
        '''
        (Item, list of children) -> None
        Assigns list of children to self.children
        '''
        self.children = children

    def addParent(self, parentID):
        '''
        (Item, Id) -> None
        Assigns parentID to Id and isRoot to False for self
        '''
        self.isRoot = False
        self.parent = parentID

    def __repr__(self):
        '''
        (Item) -> String
        Takes item and returns self.id as repr
        '''
        return str(self.id)

def startApp():
    '''
    (None) -> None
    Starts when app is executed
    '''
    data_file = input("Enter data file to be processed:") #prompts user for input
    data = json.load(open(data_file)) #loads JSON file that user specifies
    len_m = len(data["menus"]) #takes len of menus
    items = [] #list of items
    for i in range(len_m):#iterates through menus to create item objects for ids
        u = Item(data["menus"][i]["id"]) #Create new item object with id taken from JSON
        if data["menus"][i]["child_ids"]: #if child ids exist
            u.addChildren(data["menus"][i]["child_ids"]) #adds children to item
        if "parent_id" in data["menus"][i]: #adds parent_id if key "parent_id" exists in dictionary
            u.addParent(data["menus"][i]["parent_id"])
        items.append(u)#appends
    m = Menu(items)#creates new menu for items
    m.retMenuValidity()#executes validity of menus in menu object
    out = {"valid_menus": m.valid, "invalid_menus": m.invalid} #dumps valid and invalid menus to JSON file
    with open('valid.json', 'w') as outfile:
        json.dump(out, outfile)
    data = json.load(open('valid.json'))#loads file that data was dumped
    pprint(data)#prints file

if __name__ == "__main__":
    startApp()
