import sys
import hashlib

#### param 1 : filepath
if __name__ == '__main__':
    args = sys.argv
    filename = args[1]

    with open(filename, 'rb') as f:
        #md5 = hashlib.md5(f.read()).hexdigest()
        f.seek(0)
        sha256 = hashlib.sha256(f.read()).hexdigest()
        print(sha256)