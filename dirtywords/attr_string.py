class AttrString(unicode):
    def __new__(cls, s, **kwargs):
        self = super(AttrString, cls).__new__(cls, s)
        self.set_attrs(s, **kwargs)
        return self

    def set_attrs(self, reference='', **kwargs):
        defaults = {
            'bold': False,
            'italic': False,
            'underline': False,
            'fg_color': (255, 255, 255),
            'bg_color': (0, 0, 0),
        }

        for attr in defaults.iterkeys():
            if attr in kwargs:
                value = kwargs[attr]
            elif isinstance(reference, AttrString):
                value = getattr(reference, attr)
            else:
                value = defaults[attr]

            setattr(self, attr, value)

    def get_attrs(self):
        return {
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'fg_color': self.fg_color,
            'bg_color': self.bg_color,
        }

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __getitem__(self, i):
        ch = unicode.__getitem__(self, i)
        return AttrString(ch, **self.get_attrs())
