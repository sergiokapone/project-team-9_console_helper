from collections import UserDict
from datetime import datetime


class Notebook(UserDict):
    id_count = 1        
    def __str__ (self)->str:
        return self.value
    
    def add_record(self, record):
        self.data[str(Notebook.id_count)] = record
        Notebook.id_count += 1

    def delete_record_by_id(self, record_id):
        if self.data[str(record_id)]:
            del self.data[str(record_id)]

    def find_record_by_tags(self, tag):
        result = []
        for record in self.data.values():
            for tag_ in record.tags:
                if tag == str(tag_):
                    result.append(str(record) + " ")
        if result:
            return result
        return f"Tag '{tag}' not found"

    def find_record_by_text(self, text_part):
        result = []
        for record in self.data.values():
            if text_part in record.text:
                result.append(str(record) + " ")
        if result:
            return result
        return f"The text '{text_part}' not found"

    def find_record_by_date(self, date):
        for record in self.data.values():
            if date == record.date:
                return record
        return f"Not found"

    def find_record_by_id(self, id_record):
        return self.data[str(id_record)] if str(id_record) in self.data else "Not found"
        
         #   вивід всіх тегів у нотатках
    def show_all_tags(self):
        result = []
        for record in self.data.values():
            for tag_ in record.tags:
                result.append("#" + tag_ + " ")                            
        for tag_ in result:          
            if result.count(tag_) > 1:
                result.remove(tag_)
                return result
        return f"Tags  not found"
    

class Field:
    def __init__(self, value):
        self.value = value


class Tags(Field):
    def __str__(self):
        return self.value


class Record:
    def __init__(self, text):
        self.text = text
        self.tags = []
        self.date = datetime.today().strftime("%d %B %Y")

    def add_tag(self, tag):
         self.tags.append(tag)
        

    def change_text(self, new_text):
        self.text = new_text
        
    #   сортування тегів по алфавіту у нотатці    
    def sort_tag(self,tag):
          self.tags.sort()
          
    #   видалееня тегу з нотатки    
    def remove_tag(self,tag):
        self.tags.remove(tag)
    
    def __str__(self):
        result = self.text + " ("
        for tag in self.tags:
            result += str(tag) + ", "
        return result + ") " + self.date
    
    def __repr__(self) -> str:
        return self.text + " [" + ', '.join([p for p in self.tags]) +"] "+ self.date

notebook = Notebook()

record1 = Record("Some text")
record2 = Record("Another some text ")
record3 = Record("text ")
record1.add_tag("work")
record1.add_tag("job")
record2.add_tag("work")
record2.add_tag("eat")
record2.add_tag("sport")
record2.add_tag("our journey")
record3.add_tag("journey")
notebook.add_record(record1)
notebook.add_record(record2)
notebook.add_record(record3)
# record2.sort_tag(record2.tags)
record1.change_text("What doesn't kill you makes you stronger")
# record2.remove_tag("sport")
# print(notebook.show_all_tags())
