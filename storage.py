""""""

class StorageTank:
        
    data = {

        "Source": [],
        "Name": [],
        "Blurb": [],
        "Description": [],
        "Rating": [],
        "Reviews": [],
        "Followers": [],
        "Category": [],
        "Link": []
    }


    @classmethod
    def add_data(cls, parsed_page: dict):
        '''Add info from parsed page'''

        for key, value in parsed_page.items():
            cls.data[key].append(value)
        

    @classmethod
    def avoid_repetition(cls, product_url):
        '''Check if given product is alredy added'''

        if product_url not in cls.data["Link"]:
            return True
        return False
