#!/usr/bin/python


import telnetlib
import csv
import sys
import socket

with open('dxlist.csv') as csv_file:
    with open('cleaned.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #print(', '.join(row))
            line_count += 1
            #print(row[0])
            host = row[1].replace('/','').split(':')
            port = 23
            if(len(host) == 2) :
                port = int(host[1])
            
            print('Connecting to ' + host[0] + ' ' + str(port))
            try:
                tn = telnetlib.Telnet(host[0],port,10)
                tn.read_until(b"login: ",10)
                tn.close()
                print(row[0] +' OKAY!')
                writer.writerow([row[0],host[0]+':'+str(port)])
                csvfile.flush()
            except socket.timeout:
                print( row[0] + ' Timed Out!')
            except ConnectionRefusedError:
                print( row[0] + ' Socket Refused Error')
            except socket.gaierror:
                print( row[0] + ' DNS Error')
            except ConnectionResetError:
                print( row[0] + ' Connection Reset Error')
            except OSError:
                print( row[0] + ' No Route to Host')
        print('Processed '+str(line_count)+' lines.')
