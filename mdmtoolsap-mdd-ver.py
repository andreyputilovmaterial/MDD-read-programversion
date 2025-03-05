
import re
import argparse
from pathlib import Path
import traceback
import sys



import_unicom_err = None
try:
    import win32com.client
except Exception as e:
    import_unicom_err = e



def sanitize_progver_value(txt):
    try:
        if re.match(r'^\s*?(\d+)\s*?$',txt,flags=re.I|re.DOTALL):
            return re.sub(r'^\s*?(\d+)\s*?$',lambda m: m[1],txt,flags=re.I|re.DOTALL)
        elif re.match(r'^\s*?"\s*(.*)\s*"\s*?$',txt,flags=re.I|re.DOTALL):
            return re.sub(r'^\s*?"\s*(.*)\s*"\s*?$',lambda m: m[1],txt,flags=re.I|re.DOTALL)
        else:
            return re.sub(r'^\s*?(.*?)\s*$',lambda m: m[1],txt,flags=re.I|re.DOTALL)
    except:
        return '???'


def read_mdd(mdd_path,method='open'):
    if import_unicom_err:
        raise Exception('import win32com failed: please make sure you have the pywin32 python package installed and you have Unicom tools installed: {e}'.format(e=import_unicom_err)) from import_unicom_err
    mdmdocument = None
    if method=='open':
        mdmdocument = win32com.client.Dispatch("MDM.Document")
        # openConstants_oNOSAVE = 3
        openConstants_oREAD = 1
        # openConstants_oREADWRITE = 2
        mdmdocument.Open( mdd_path, "", openConstants_oREAD )
    elif method=='join':
        mdmdocument = win32com.client.Dispatch("MDM.Document")
        mdmdocument.Join(mdd_path, "{..}", 1, 32|16|512)
    else:
        raise ValueError('MDM Open: Unknown open method, {method}'.format(method=method))
    
    return mdmdocument



def read_routing_scripts(mdmdocument):
    return mdmdocument.Routing.Script



def parse_program_version(txt):
    result = []
    lines = re.split(r'(?:\r?\n|\r|\n)',txt,flags=re.I|re.DOTALL)
    for line in lines:
        matches = re.match(r'^\s*?ProgramVersion\s*?=\s*([^\s\'].*?)\s*(?:\'.*?)?\s*?$',line,flags=re.I|re.DOTALL)
        if matches:
            result.append(sanitize_progver_value(matches[1]))
    
    return ','.join(result)



def main():
    try:
        parser = argparse.ArgumentParser(
            description="Read MDD program version utility"
        )
        parser.add_argument(
            'mdd',
            type=str,
        )
        args = parser.parse_args()

        mdd_filename = None
        if args.mdd:
            mdd_filename = '{arg}'.format(arg=args.mdd)
            mdd_filename = Path(mdd_filename)
            mdd_filename = mdd_filename.resolve()
            if not Path(mdd_filename).is_file():
                raise FileNotFoundError('MDD file not found: "{fname}"'.format(fname=mdd_filename))
            mdd_filename = '{name}'.format(name=mdd_filename)
        if not mdd_filename:
            raise AttributeError('MDD not specified')
        
        mdd = read_mdd(mdd_filename)
        routing_scripts = read_routing_scripts(mdd)
        program_version = parse_program_version(routing_scripts)

        print(program_version)


    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro(, file=sys.stderr)"
        print('', file=sys.stderr)
        print('Stack trace:', file=sys.stderr)
        print('', file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('', file=sys.stderr)
        print('', file=sys.stderr)
        print('', file=sys.stderr)
        print('Error:', file=sys.stderr)
        print('', file=sys.stderr)
        print('{e}'.format(e=e), file=sys.stderr)
        print('', file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()


