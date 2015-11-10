import uuid
from .common import Tintin

if __name__ == "__main__":
    tt = Tintin()
    tt.write("#var uuid %s"%(str(uuid.uuid4())))
