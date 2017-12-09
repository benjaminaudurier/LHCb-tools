# Getting file from the grid

if __name__ == '__main__':

    from subprocess import call
    from sys import argv

    if len(argv) > 1:
        files = argv[1]
        with open(files, 'w') as f:
            n_files = 0
            for l in f:
                print('Getting file {0}'.format(l))
                call('dirac-dms-get-file {0}'.format(f), shell=True)
                n_files += 1

        print('Done getting {0} files'.format(n_files))
