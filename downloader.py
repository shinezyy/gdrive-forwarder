import sh
from optparse import OptionParser
import re


parser = OptionParser()
parser.add_option('-d', '--download-dir',
        help='dir to download from', action='store')
parser.add_option('-o', '--output-dir',
        help='dir to download to', action='store')

(options, args) = parser.parse_args()

file_list = sh.gdrive('list')
m = re.search('(.+) +{} +dir'.format(options.download_dir), str(file_list))
dir_id = m.group(1).strip()
print(dir_id)

sh.gdrive('download', '-r', '--path', options.output_dir, dir_id)


