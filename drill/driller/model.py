from datetime import datetime

class Klass(object):
    def __repr__(self):
        return str(self.__dict__)

    def __iter__(self):
        return self.__dict__.iteritems()

    def __len__(self):
        return len(self.__dict__)
    
class ExamAnswer(Klass):
    def __init__(self, qnum, year, num):
        self.qnum = qnum
        self.year = year
        self.num = num
        self.start = datetime.utcnow()
        self.answers = []

    def __repr__(self):
        # return '<%s: %r>' % (type(self).__name__, self.qnum)
        return '<%d: %d/%d: %r>' % (self.qnum, self.year, self.num, self.answers)

    
class ExamConf(object):
    def __init__(self, n, method, tags=[], n_per_page=5):
        self.n = n
        self.method = method
        self.tags = tags
        self.n_per_page = n_per_page

    def __repr__(self):
        return '<%d, %s, %r>' % (self.n, self.method, self.tags)
