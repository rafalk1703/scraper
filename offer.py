
# class used to create property object
class Offer:

    # def __init__(self, url, name=None, description=None, photos=None,
    #             address=None, coordinates=None, geo_level=None,
    #             characteristics=None, price=None, features=None,
    #             owner=None, extra=None, date_created=None,
    #             date_modified=None):
    #     self.url = url
    #     self.name = name
    #     self.description = description
    #     self.photos = photos
    #     self.address = address
    #     self.coordinates = coordinates
    #     self.geo_level = geo_level
    #     self.characteristics = characteristics
    #     self.price = price
    #     self.features = features
    #     self.owner = owner
    #     self.extra = extra
    #     self.date_created = date_created
    #     self.date_modified = date_modified
    def __init__(self, url, name=None, address=None, price=None):
        self.url = url
        self.name = name
        self.address = address
        self.price = price