import sys
import monitor


def write_data():
    with open('output.csv', 'w+') as f:
        f.write('agent, ip_address, date, time, country, city, uri, agent_string')
        run = True
        while run:
            f.write('\n')
            try:
                line = sys.stdin.readline()
            except KeyboardInterrupt:
                f.flush()
                break

            if not line:
                break

            entry = monitor.lineparse(line)
            print(entry)
            f.write(','.join(entry))


def print_data():
    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if line:
            entry = monitor.lineparse(line)
            print(entry)


if __name__ == '__main__':
    print_data()
