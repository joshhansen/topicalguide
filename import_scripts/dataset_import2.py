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

import os
import re
import sys

from django.db import transaction

from topic_modeling.visualize.models import Dataset, Document, Word
from topic_modeling import anyjson

class DatasetImporter(object):
    NUM_DOTS = 100
    
    def __init__(self, name, readable_name, description, dataset_dir, files_dir, metadata_types, metadata_files, token_regex):
        print 'DatasetImporter({0},{1},{2},{3},{4},{5},{6},{7}'.format(name, readable_name, description, dataset_dir, files_dir, metadata_types, metadata_files, token_regex)
        self.name = name
        self.readable_name = readable_name
        self.description = description
        self.dataset_dir = dataset_dir
        self.files_dir = files_dir
        self.metadata_types = metadata_types
        self.metadata_files = metadata_files
        self.token_regex = token_regex
        
        self.dataset = Dataset.objects.get_or_create( \
            name=name, readable_name=readable_name, description=description,
            dataset_dir=dataset_dir, files_dir=files_dir)[0]
    
    def _document_metadata(self):
        return anyjson.deserialize(open(self.metadata_files['documents']).read())
    
    def _dataset_metadata(self):
        return anyjson.deserialize(open(self.metadata_files['datasets']).read())
    
    @transaction.commit_manually
    def import_dataset(self):
        for doc_filename in self.document_filenames():
            print 'Importing '+doc_filename,
            sys.stdout.flush()
            doc = Document.objects.get_or_create(filename=doc_filename,dataset=self.dataset)[0]
            
#            token_count = 0
            for i,token_s in enumerate(self.document_tokens(doc_filename)):
                if i % self.NUM_DOTS == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                type = Word.objects.get_or_create(value=token_s)[0]
                WordToken.objects.get_or_create(type=type,document=doc)[0]
            transaction.commit()
            sys.stdout.write('\n')
            sys.stdout.flush()
    
    
    
    
    def document_filenames(self):
        for filename in os.listdir(self.files_dir):
            yield '{0}/{1}'.format(self.files_dir, filename) 
    
    def document_tokens(self, filename):
        text = open(filename).read()
        for match in re.finditer(self.token_regex, text):
            yield match.group()

