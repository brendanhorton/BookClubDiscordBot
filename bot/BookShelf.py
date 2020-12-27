class BookShelf:
    def __init__(self):
        self.bookCollection = { 
            "January": "Fifteen Dogs",
            "February": "Can't Hurt Me",
            "March": "Children of Hurin",
            "April": "Nothing",
            "May": "Nothing",
            "June": "Nothing",
            "July": "Nothing",
            "August": "Nothing",
            "September": "Nothing",
            "October": "Nothing",
            "November": "Nothing",
            "December": "Death on The Nile",
        }

    def updateMonth(self, month, bookName):
        self.bookCollection[month.capitalize()] = bookName

    def getBook(self, month):
        return self.bookCollection[month.capitalize()]

    def allBooks(self):
        for month in self.bookCollection:
            print(month, self.bookCollection[month])



    