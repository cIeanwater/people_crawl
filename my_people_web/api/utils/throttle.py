from rest_framework.throttling import BaseThrottle


import time
VISIT_RECORD = {}


class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 1. 获取用户IP
        remote_addr = self.get_ident(request)
        print(remote_addr)

        ctime = time.time()
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [ctime,]
            return True
        history = VISIT_RECORD.get(remote_addr)
        self.history = history

        while history and history[-1] < ctime - 60:
            history.pop()

        if len(history) < 3:
            history.insert(0, ctime)
            return True

        # return True    # 表示可以继续访问
        # return False # 表示访问频率太高，被限制

    def wait(self):
        # 还需要等多少秒才能访问
        ctime = time.time()
        return 60 - (ctime - self.history[-1])