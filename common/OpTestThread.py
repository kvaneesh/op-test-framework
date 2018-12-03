#!/usr/bin/python2
# OpenPOWER Automated Test Project
#
# Contributors Listed Below - COPYRIGHT 2018
# [+] International Business Machines Corp.
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#

'''
Multithreaded library
---------------------
This adds a new multithreaded library with having different
variants of thread based SSH/SOL session runs, each thread logs
to a different log file.
'''

import random
import unittest
import time
import threading
import pexpect

import OpTestConfiguration
from Exceptions import CommandFailed

import logging
import OpTestLogger
log = OpTestLogger.optest_logger_glob.get_logger(__name__)


class OpSSHThread(threading.Thread):
    '''
    Create a thread and run commands in it.
    '''
    def __init__(self, threadID, name, cmd_list=None, cmd_dict=None,
                 sleep_time=None, execution_time, ignore_fail=False):

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.cmd_list = cmd_list
        self.cmd_dict = cmd_dict
        self.sleep_time = sleep_time
        self.execution_time = execution_time
        self.ignore_fail = ignore_fail
        self.name = name
        conf = OpTestConfiguration.conf
        self.host = conf.host()
        self.c = self.host.get_new_ssh_connection(name)

    def run(self):
        log.debug("Starting %s" % self.name)
        if cmd_dict:
            self.run_dict()
        else:
            self.run_list()
        log.debug("Thread exiting after run for desired time")


    def run_list(self):
        '''
        Runs a list of commands in a loop with equal sleep times in linear order
        '''
        execution_time = time.time() + 60 * self.execution_time,
        log.debug("Starting %s for new SSH thread %s" % (threadName, self.cmd_list))
        while True:
            for cmd in self.cmd_list:
                if self.ignore_fail:
                    try:
                        self.c.run_command(cmd)
                    except CommandFailed as cf:
                        pass
                else:
                    self.c.run_command(cmd)
                time.sleep(self.sleep_time)
            if time.time() > execution_time:
                break

    def run_dict(self):
        execution_time = time.time() + 60*self.execution_time,
        log.debug("Starting %s for new SSH thread %s" % (threadName, self.cmd_dict))
        while True:
            for cmd, tm in self.cmd_dict.iteritems():
                if self.ignore_fail:
                    try:
                        self.c.run_command(cmd)
                    except CommandFailed as cf:
                        pass
                else:
                    self.c.run_command(cmd)
                time.sleep(tm)
            if time.time() > execution_time:
                break
