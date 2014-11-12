__author__ = 'Alexander Horkun'
__email__ = 'mindkilleralexs@gmail.com'


class Website(object):
    """
    Holds data about added websites to parse.
    """
    id = 0
    name = ""
    pages = set()
    host = ""


class Page(object):
    """
    Holds info about loaded pages.
    """
    id = 0
    url = ""
    website = None
    loadings = []

    def isloaded(self):
        """
        Checks if the page's content was successfully loaded at least once.

        :return: bool
        """
        for loading in self.loadings:
            if loading.success:
                return True
        return False

    def getcontent(self):
        """
        Returns content of last successful loading.
        :return: Content (HTML) or None
        """
        loading = self.get_last_successful_loading()
        if not loading is None:
            return loading.content
        else:
            return None

    def get_last_successful_loading(self):
        last_loading = None
        for l in self.loadings:
            if l.success and (last_loading is None or last_loading.time < l.time):
                last_loading = l
        if last_loading:
            return last_loading
        else:
            return None


class Loading(object):
    """
    Holds info about a loading attempt.
    """
    id = 0
    page = None
    success = False
    headers = {}
    content = ""
    time = None
    loading_time = 0