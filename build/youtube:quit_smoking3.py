# The Topic Browser
# Copyright 2010-2011 Brigham Young University
#
# This file is part of the Topic Browser <http://nlp.cs.byu.edu/topic_browser>.
#
# The Topic Browser is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The Topic Browser is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with the Topic Browser.  If not, see <http://www.gnu.org/licenses/>.
#
# If you have inquiries regarding any further use of the Topic Browser, please
# contact the Copyright Licensing Office, Brigham Young University, 3760 HBLL,
# Provo, UT 84602, (801) 422-9339 or 422-3821, e-mail copyright@byu.edu.

#YouTube comments
#import os

num_topics = 40
dataset_name = 'youtube:quit_smoking3'
dataset_description = '''YouTube video comments. One document corresponds to one video. Videos selected by depth 3 breadth-first search from video id "dn50mTEGnrU". Links between videos come from Google's relatedness. Max comments per video is 1000.'''
nums = r'0123456789'
undesired_chars = r'''\s'",./<>?:;()\[\]\-=~!#$\^*_+''' + nums
undesired_chars_escaped = r'''\\s'\",./<>?:;\\(\\)\[\]\-=~!#$\^*_+''' + nums
python_token_regex = r'[^' + undesired_chars + ']+'
java_token_regex = r'"[^' + undesired_chars_escaped + ']+"'
#suppress_default_attributes_task = True

#def task_attributes():
#    task = dict()
#    task['targets'] = [attributes_file]
#    task['actions'] = [(generate_attributes_file,
#                [dataset_dir+'/'+chron_list_filename, attributes_file])]
#    task['clean'] = ['rm -f '+attributes_file]
#    return task
#
#def task_extract_data():
#    task = dict()
#    task['targets'] = [files_dir]
#    task['actions'] = [
#        (extract_state_of_the_union,
#         [dataset_dir+'/'+chron_list_filename,
#          dataset_dir+'/'+addresses_filename,
#          files_dir]
#        )
#    ]
#    task['clean'] = ['rm -rf '+files_dir]
#    task['uptodate'] = [os.path.exists(files_dir)]
#    return task
