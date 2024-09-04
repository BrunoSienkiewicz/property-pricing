from ts.torch_handler.base_handler import BaseHandler


class Handler(BaseHandler):
    def __init__(self):
        super(Handler, self).__init__()

    def preprocess(self, requests):
        pass

    def postprocess(self, data):
        pass

