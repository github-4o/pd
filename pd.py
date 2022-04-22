import json
from git import Repo
import os


class pd:
    def __init__(self, filename, git = False):
        self.git = git
        if git:
            os.makedirs(filename, exist_ok=True)
            self.r = Repo.init(filename)
            fn = filename+'/'+filename
            self.pd = pd(fn)
            print(self.r.index.diff())
            if len(self.r.index.diff()) > 1:
                self.r.index.add(filename)
                self.r.index.commit('another commit')
        else:
            self.filename = filename
            try:
                with open(filename, 'r+') as fd:
                    self._dict = json.load(fd)
            except:
                print('hit')
                self._dict = {}
            print(self._dict)
            self.sync()
    
    def __setitem__(self, key, value):
        if self.git:
            self.pd.__setitem__(key, value)
        else:
            self._dict[key] = value
            self.sync()

    def __getitem__(self, key):
        return self._dict[key]

    def __delitem__(self, k):
        del(self._dict[k])

    def __str__(self):
        return str(self._dict)

    def __contains__(self, other):
        return other in self._dict

    def __iter__(self):
        yield from self._dict

    def keys(self):
        return self._dict.keys()

    def sync(self):
        with open(self.filename, "w+") as file:
            file.write(json.dumps(self._dict, indent = 2))
        
