from typing import List, Dict, Any

class Tree:
    def __init__(self, value=None, *, sep="."):
        self.children: Dict[str, Tree] = {}
        self.sep = sep
        self.value = value
    
    def _setter(self, keys: List[str]=[], value: Any=None):
        if len(keys) > 0:
            if keys[0] not in self.children:
                self.children[keys[0]] = Tree(sep=self.sep)
            self.children[keys[0]]._setter(keys[1:], value)
        else:
            self.value = value
    
    def _getter(self, keys: List[str]=[]):
        if len(keys) > 1:
            return self.children[keys[0]]._getter(keys[1:])
        else:
            return self.children[keys[0]].value
    
    def _delete(self, keys: List[str]=[]):
        if len(keys) > 1:
            self.children[keys[0]]._delete(keys[1:])
        else:
            del self.children[keys[0]]
    
    def _to_dict(self):
        l = {}
        for i in self.children.copy():
            l[i] = self.children[i].value
            d = self.children[i].to_dict()
            for _ in d:
                l[self.sep.join([i, _])] = d[_]
        return l
    
    def set(self, key: str, value: Any):
        self._setter(key.split(self.sep), value)
    
    def get(self, key: str, default: Any=None):
        try: return self._getter(key.split(self.sep))
        except: return default
    
    def delete(self, key: str):
        try: self._delete(key.split(self.sep))
        except: pass
    
    def to_dict(self):
        return self._to_dict()