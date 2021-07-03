class MetaSingleton(type):
    Nil = {}

    def __call__(cls, *args):
        if cls not in cls.Nil:
            cls.Nil[cls] = super().__call__(*args)
        return cls.Nil[cls] if not args else super().__call__(*args)
