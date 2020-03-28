#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
    EzTest
    Ver: 1.0

    This program use threads to run tests on list of objects
    Developer: Shavit Ilan (ilansh5@bezeq.co.il)
"""
from threading import Thread
import subprocess
import os
import logging
from ConfigParser import SafeConfigParser
RESULT = {}

def get_ip_list():
    """
    Test in IP and return test result: 'G'(good) or 'B' (bad)
    """
    ip_list = []
    with open("eztest.ip", "r") as in_file:
        all_lines = in_file.readlines()
    for each_line in all_lines:
        ip_list.append(each_line.strip())
    return ip_list

def write_result(result):
    """
    Test in IP and return test result: 'G'(good) or 'B' (bad)
    """
    with open("eztest.result", "w") as out_file:
        out_file.write(str(result))

def test_one_ip(ip_address):
    """
    Test in IP and return test result: 'G'(good) or 'B' (bad)
    """
    global RESULT
    fnull = open(os.devnull, "w")
    the_result = subprocess.call(['ping', '-c', '1', ip_address], stdout=fnull)
    if the_result == 0:
        RESULT[ip_address] = "G"
    else:
        RESULT[ip_address] = "B"

def test_list(the_list):
    """
    Test list of objects using threads
    """
    process_list = []
    for each_ip in the_list:
        process = Thread(target=test_one_ip, args=[each_ip])
        process.start()
        process_list.append(process)
    for each_process in process_list:
        each_process.join()

def main():
    """
    Test list of objects using threads
    """
    global RESULT
    parser = SafeConfigParser()
    parser.read('eztest.ini')
    max_threads = int(parser.get('CONFIG', 'MAX_THREADS'))
    debug_mode = parser.get('CONFIG', 'DEBUG_MODE')

    if debug_mode == 'DEBUG':
        logging.basicConfig(filename='eztest.log', level=logging.DEBUG,\
            format='%(asctime)s:%(levelname)s:%(message)s')
    else:
        logging.basicConfig(filename='eztest.log', level=logging.CRITICAL,\
            format='%(asctime)s:%(levelname)s:%(message)s')

    logging.info("Start running")
    the_log = "Number Threads:  %s" % max_threads
    logging.info(the_log)

    ip_list = get_ip_list()
    list_to_check = []
    while len(ip_list) >= (max_threads - len(list_to_check)):
        the_ip = ip_list.pop()
        list_to_check.append(the_ip)
        if len(list_to_check) == max_threads:
            the_log = "Testing: %s" % list_to_check
            logging.info(the_log)
            test_list(list_to_check)
            list_to_check = []

    if ip_list != []:
        the_log = "Testing: %s" % list_to_check
        logging.info(the_log)
        test_list(ip_list)

    logging.info("Writing results to: 'eztest.result'")
    write_result(RESULT)

    logging.info("End running")

if __name__ == "__main__":
    main()
