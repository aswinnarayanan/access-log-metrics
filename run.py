import sys
import monitor


def write_data(infile, outfile):
    with open(outfile, 'w+') as fout:
        fout.write('agent, ip_address, date, time, country, city, uri, agent_string')
        with open(infile) as fin:
            for line in fin:
                try:
                    entry = monitor.lineparse(line)
                    print(entry)
                    fout.write('\n')
                    fout.write(','.join(entry))
                except KeyboardInterrupt:
                    fout.flush()
                    break


def print_data(infile):
    with open(infile) as fin:
        for line in fin:
            try:
                entry = monitor.lineparse(line)
                print(entry)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    infile = sys.argv[1]
    if len(sys.argv) == 2:
        print_data(sys.argv[1])
    elif len(sys.argv) == 3:
        write_data(sys.argv[1], sys.argv[2])
    else:
        raise Exception
