class InvestMinTradesSingleton(object):
    """ Синглтон
    """
    # флаг отвечающий за выполнение отслеживания
    is_working = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InvestMinTradesSingleton, cls).__new__(cls)
        return cls.instance
