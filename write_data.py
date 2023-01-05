import sys
import parse_log
import multiprocessing as mp
import pathlib
import re


# def parse_filename(filename):
#     if 'FSL' in filename:
#         return 'atlas package', 'nii'
#     else:
#         fileparts = re.split('[- _ .]', filename)
#         feature = f'{fileparts[3]} {fileparts[2]}'
#         fileformat = fileparts[-3]
#         return feature, fileformat


# def write_data(infile):
#     with open(infile, 'r') as in_fh:
#         rows = []
#         for line in in_fh:
#             print(line)
#             try:
#                 if 'tissuestack' in line :
#                     entry = parse_log.lineparse(line)
#                     outline = ','.join(entry)

#                     filename = entry[6].split('/')[-1]
#                     feature, fileformat = parse_filename(filename)
#                     download = f'{entry[1]}:{feature}'
#                     outline = f'{outline},{download},{filename},{feature},{fileformat}'
#                     rows.append(outline)
#             except:
#                 print(line)
#         return rows

def write_data(infile):
    with open(infile, 'r') as in_fh:
        rows = []
        for line in in_fh:
            # print(line)
            try:
                if 'tissuestack' in line or 'desktop.html' in line or 'tablet.html' in line or 'phone.html' in line:
                    entry = parse_log.lineparse(line)
                    outline = ','.join(entry)
                    rows.append(outline)
            except:
                print(line)
        return rows


if __name__ == '__main__':
    indir = pathlib.Path(sys.argv[1])
    cores = mp.cpu_count()
    pools = mp.Pool(cores)

    infiles = indir.glob('access_log*')
    
    # outfile = indir/'output.csv'
    # with open(outfile, 'w+') as f:
    #     f.write('agent,ip_address,date,time,country,city,uri,agent_string,download,filename,feature,fileformat')
    #     for infile in infiles:
    #         file_result = write_data(infile)
    #         for row in file_result:
    #             f.write('\n')
    #             f.write(row)


    results = pools.map(write_data, infiles)

    outfile = indir/'output.csv'
    with open(outfile, 'w+') as f:
        f.write('agent,ip_address,date,time,country,city,uri,agent_string,download,filename,feature,fileformat')
        for file_result in results:
            for row in file_result:
                f.write('\n')
                f.write(row)

    pass
    # write_data(pathlib.Path('.\\imaging.org.au\\logs\\access_log-20190322').resolve(strict=True))
