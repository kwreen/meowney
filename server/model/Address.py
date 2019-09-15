class Address:
    def __init__(self, principalResidence: PrincipalResidence):
        self.principalResidence = principalResidence
        

class PrincipalResidence:
    def __init__(self, addressType: int, latitude: float, longitude: float, municipality: str, postalCode: str, streetName: str, streetNumber: str):
        self.addressType = addressType
        self.latitute = latitude
        self.longitude = longitude
        self.municipality = municipality
        self.postalCode = postalCode
        self.streetName = streetName
        self.streetNumber = streetNumber
