import os

if os.path.exists('fp-lib-table'):
    with open('fp-lib-table', 'r', encoding='utf-8') as f:
        print("fp-lib-table contents:\n", f.read())
else:
    print("fp-lib-table DOES NOT EXIST in workspace!")

if os.path.exists('sym-lib-table'):
    with open('sym-lib-table', 'r', encoding='utf-8') as f:
        print("sym-lib-table contents:\n", f.read()[:500])
