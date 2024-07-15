import argparse
import glob
import requests
import sys
import pandas as pd
from tqdm import tqdm

def main(address, outfile):
    print(f'Reaching out to godbolt at: "{address}"')
    if not address.endswith('/'):
        address += '/'
    # connect to rest api
    sess = requests.Session()
    sess.headers.update({"Accept": "text/json"})
    resp = sess.get(f'{address}api/compilers')
    if not resp.status_code == 200:
        print('Unable to connect, exiting!')
        sys.exit(-1)
    # get list of files from sorce dir
    save_data = []
    files = glob.glob('source/**.c', recursive=True)
    for i in tqdm(range(len(files))):
        with open(files[i], 'r') as fd:
            content = fd.read()
        # tests
        # curl 'https://godbolt.org/api/clang1810/compile?options=-emit-llvm' --data-binary 'int foo() { return 1; }'
        # curl 'http://localhost:10240/api/compiler/clang10/compile?options=-Wall' --data-binary 'int foo() { return 1; }'
        # curl 'http://localhost:10240/api/compiler/clang10/compile?options=-emit-llvm' --data-binary 'int foo() { return 1; }'
        resp_ir = sess.post(f'{address}api/compiler/clang10/compile?options=-emit-llvm', data=content)
        resp_asm = sess.post(f'{address}api/compiler/clang10/compile?options=-Wall', data=content)
        save_data.append({'source_file': files[i], 'compiler': 'clang10', 'ir':resp_ir.text, 'ir_flags':'-emit-llvm', 'asm':resp_asm.text, 'asm_flags':'-Wall'})

    df = pd.DataFrame.from_dict(save_data)
    df.to_csv(outfile, index=False)
    print('Done!')
    # todo: generate dot files of the control flow graph
    # looks like we can use opt
    # more info: https://stackoverflow.com/questions/67393329/llvm-doesnt-generate-cfg


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--address', type=str, required=True, help='address of godbolt (compiler explorer)\n\te.g. http://localhost:10240/')
    ap.add_argument('-o', '--outfile', type=str, required=True, help='file to save output (csv)')
    args = ap.parse_args()
    main(args.address, args.outfile)
