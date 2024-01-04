import threading
import collections


# reference: https://gist.github.com/vitaliyp/6d54dd76ca2c3cdfc1149d33007dc34a
class FIFOLock(object):
    def __init__(self):
        self._lock = threading.Lock()
        self._inner_lock = threading.Lock()
        self._pending_threads = collections.deque()

    def acquire(self, blocking=True):
        with self._inner_lock:
            lock_acquired = self._lock.acquire(False)
            if lock_acquired:
                return True
            elif not blocking:
                return False

            release_event = threading.Event()
            self._pending_threads.append(release_event)

        release_event.wait()
        return self._lock.acquire()

    def release(self):
        with self._inner_lock:
            if self._pending_threads:
                release_event = self._pending_threads.popleft()
                release_event.set()

            self._lock.release()

    __enter__ = acquire

    def __exit__(self, t, v, tb):
        self.release()

class UidLock(FIFOLock):

    def acquire(self, blocking=True, uni_id=None):
        with self._inner_lock:
            lock_acquired = self._lock.acquire(False)
            if lock_acquired:
                return True
            else:
                index, count = self._get_index(uni_id)
                if index != -1:
                    raise Exception(f'the uni_id({uni_id}) is already is queue')

                release_event = threading.Event()
                self._pending_threads.append((uni_id,release_event))
                if not blocking and uni_id is not None:
                    # index, event
                    return len(self._pending_threads),release_event
                
        release_event.wait()
        return self._lock.acquire()

    def release(self):
        with self._inner_lock:
            if self._pending_threads:
                uni_id,release_event = self._pending_threads.popleft()
                release_event.set()

            self._lock.release()


    def get_index(self,uni_id):
        with self._inner_lock:
            return self._get_index(uni_id)
        
    def _get_index(self,uni_id):
        for index,tup in enumerate(self._pending_threads):
                if uni_id == tup[0]:
                    return index+1, len(self._pending_threads)
        return -1, len(self._pending_threads)

    def __enter__(self):
        self.acquire()