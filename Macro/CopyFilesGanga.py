# Getting file from the grid
import os
import shutil

if __name__ == '__main__':

    from subprocess import call
    from sys import argv
    print 'Reading file '+ argv[-1]
    with open(argv[-1], 'r') as f:

        n_files = 0
        delete_all = False
        keep_all = False
        for l in f:
            # print '-- reading line '+l
            split_line = l.split('/')

            #create directory if necessary
            if os.path.isdir('{}'.format(split_line[-2])) is False:
                print ' -- No dir {}. Create one'.format(split_line[-2])
                os.mkdir(split_line[-2])

            # Ask for delete if file already exist, otherwise download in .
            if os.path.isfile('{0}/{1}'.format(split_line[-2],split_line[-1].replace("\n",''))):

                    if keep_all is not True and delete_all is not True:
                        decision = raw_input('File {0}/{1} already exist, would you like to replace it ? [y,yall,n,nall]: '.format(split_line[-2],split_line[-1].replace("\n",'')))
                        decision = decision.capitalize()

                        if not decision.isalnum() or decision not in ["Y",'Yall','N','Nall']:
                                print 'Don\'t know this answer'
                                break 

                        if decision == 'Yall':
                                delete_all = True
                                print " --- Will delete this file and others"
                                os.remove('{0}/{1}'.format(split_line[-2], split_line[-1].replace('\n', '')))

                        elif decision == 'Nall':
                                keep_all = True
                                print " --- Skip this file and the other ones"
                                skip_file = keep_all

                        elif decision == "N":
                                print " --- Skip this file: "+split_line[-2]+'/'+split_line[-1].replace("\n", '')
                                continue 

                        elif decision == 'Y':
                                print ' --- Delete file '+split_line[-2]+'/'+split_line[-1].replace('\n', '')
                                os.remove('{0}/{1}'.format(split_line[-2], split_line[-1].replace('\n', '')))

                    elif keep_all is True: continue 

                    elif delete_all is True:
                        print ' --- Delete file '+split_line[-2]+'/'+split_line[-1].replace('\n', '')
                        os.remove('{0}/{1}'.format(split_line[-2], split_line[-1].replace('\n', '')))
                        print('Getting file {0}'.format(l))
                        call('lb-run LHCbDIRAC dirac-dms-get-file {0}'.format(l), shell=True)

                        print('Moving file {0} to {1}'.format(l, split_line[-2]))
                        shutil.move(split_line[-1].replace("\n",''),'{0}'.format(split_line[-2]))
                        n_files += 1

            else:
                print('Getting file {0}'.format(l))
                call('lb-run LHCbDIRAC dirac-dms-get-file {0}'.format(l), shell=True)

                print('Moving file {0} to {1}'.format(l, split_line[-2]))
                shutil.move(split_line[-1].replace("\n",''),'{0}'.format(split_line[-2]))
                n_files += 1

        print('Done getting {0} files'.format(n_files))
