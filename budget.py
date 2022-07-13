from lib2to3.pgen2.token import PERCENT


class Category:
  def __init__(self, _categoryName) :
      self.name = _categoryName
      self.ledger = list()

    
  def deposit(self, _amount, _description = "") :
    self.ledger.append({
        "amount" : _amount,
        "description" : _description
    })

  
  def withdraw(self, _amount, _description = "") :
    if self.check_funds(_amount) == True :
      self.ledger.append({
          "amount" : - _amount,
          "description" : _description
      })
      return True
    else :
      return False


  def get_balance(self) :
      currentBalance = 0
      for operation in self.ledger :
          currentBalance += operation["amount"]

      return currentBalance

  
  def transfer(self, _amount, _budgetCategory) :
      if self.check_funds(_amount) == True :
        self.withdraw(_amount, "Transfer to " + _budgetCategory.name)
        _budgetCategory.deposit(_amount, "Transfer from " + self.name)
        return True
      else :
        return False


  def check_funds(self, _amount) :
      if self.get_balance() > _amount :
        return True
      else :
        return False
    
  
  def __repr__(self) :
    titleString = self.getTitleString()
    ledgerItems = self.getLedgerItems()

    return titleString + ledgerItems


  def getTitleString(self) :
    nameLength = len(self.name)
    asterisks = 30 - nameLength
    asteriskLine = ""
    for i in range(0, int(asterisks / 2)) :
      asteriskLine += '*'
    
    return asteriskLine + self.name + asteriskLine + "\n"


  def getLedgerItems(self) :
    actionString = ""
    totalMessage = "Total: "
    for i in self.ledger:
      amount = str(round(i["amount"], 2))
      description = i["description"][:23]
      whiteSpaceNeeded = 30 - (len(description) + len(amount))
      whiteSpace = getWhiteSpace(whiteSpaceNeeded)
      actionString += description + whiteSpace + amount + "\n"
      whiteSpace = ""

    actionString += totalMessage + str(round(self.get_balance(), 2)) + "\n"
    return actionString
  
  def getExpenses(self) :
    grandTotal = 0
    for i in self.ledger :
      if i["amount"] < 0 :
        grandTotal += i["amount"]
      
    return round(grandTotal, 2)


def getWhiteSpace(_whiteSpaceNeeded) :
    _whiteSpace = ""
    for j in range(0, _whiteSpaceNeeded) :
        _whiteSpace += " "
    
    return _whiteSpace



def create_spend_chart(categories):
  categoryList = getCategories(categories)
  finalString = "Percentage spent by category\n"
  finalString += printPercentages(categoryList)
  finalString += printCategoryNames(categoryList)
  return finalString


def printCategoryNames(_categoryList) :
  categoryNames = ""
  longestCategoryName = getLongestCategoryName(_categoryList)
  for i in range(0, len(longestCategoryName)) :
    categoryNames += "      "

    for category in _categoryList[:-1] :
      if i < len(category["name"]) :
        categoryNames += category["name"][i] + "  "
      else :
        categoryNames += "   "
    
    if i < len(_categoryList[-1]["name"]) :
      categoryNames += _categoryList[-1]["name"][i] + "\n"
    else :
      categoryNames += " " + "\n"
  
  return categoryNames


def getLongestCategoryName(_categoryList) :
  maxLength = 0
  longestName = ""
  for category in _categoryList :
    if len(category["name"]) > maxLength :
      maxLength = len(category["name"])
      longestName = category["name"]
    else :
      continue
  
  return longestName


def printPercentages(_categoryList) :
  percentageString = ""
  for i in reversed(range(0, 100 + 1)) :
    whiteSpaceNeeded = 3 - len(str(i))
    whiteSpace = getWhiteSpace(whiteSpaceNeeded)
    if i % 10 != 0 :
      continue
    else :
      percentageString += whiteSpace + str(i) + "| "
      for category in _categoryList[:-1] :
        if i <= category["percentage"] :
          percentageString += " O "
        else :
          percentageString += "   "
      
      if i <= _categoryList[-1]["percentage"] :
        percentageString += " O \n"
      else :
        percentageString += "   \n"
  
  percentageString += "     "
  for category in _categoryList[:-1] :
    percentageString += "---"
  
  percentageString += "---\n"

  return percentageString


def getCategories(_categories) :
  totalExpensesAcrossCategories = 0
  _categoryList = list()
  for i in _categories :
    _categoryList.append({
      "name": i.name,
      "totalExpenses" : i.getExpenses(),
      "percentage" : 0
    })
    totalExpensesAcrossCategories += _categoryList[-1]["totalExpenses"]
  
  for j in _categoryList :
    # Round down to the nearest 10.
    j["percentage"] = int(j["totalExpenses"] / totalExpensesAcrossCategories * 10) * 10

  return _categoryList

