class Customer:
  def __init__(self, addresses: [Address], age: int, birthDate: str, gender: str, givenName: str, habitationStatus: str, id: str, maidenName: str, 
                occupationIndustry: str, otherName: str, relationshipStatus: str, schoolAttendance: str, schools: [], surname: str, totalIncome: float,
                customerType: str, workActivity: str):
    self.addresses = addresses
    self.age = age
    self.birthDate = birthDate
    self.gender = gender
    self.givenName = givenName
    self.habitationStatus = habitationStatus
    self.id = id
    self.maidenName = maidenName
    self.occupationIndustry = occupationIndustry
    self.otherName = otherName
    self.relationshipStatus = relationshipStatus
    self.schoolAttendance = schoolAttendance
    self.schools = schools
    self.surname = surname
    self.totalIncome = totalIncome
    self.type = customerType
    self.workActivity = workActivity