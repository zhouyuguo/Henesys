

class XMLInfo(dict):
    def __init__(self):
        self[title_k]
        pass

class IndexSt:
    def __init__(self):
        self.file_path = None
        self.line_no = None
        self.title = None
        self.href = None

    def __cmp__(self, dest):
        return self.href == dest.href
        
    

if __name__ ==  "__main__":
    a = IndexSt();
    b = IndexSt();
    a.title = "bt"
    a.href = "bhref"
    b.title = "bt"
    b.href = "bhref"
    print a==b

