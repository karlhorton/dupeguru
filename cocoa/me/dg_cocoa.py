# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from hscommon.cocoa import signature

from core.app_cocoa_inter import PyDupeGuruBase, PyDetailsPanel
from core_me.app_cocoa import DupeGuruME
from core.scanner import ScanType

# Fix py2app imports which chokes on relative imports and other stuff
import core_me.app_cocoa, core_me.data, core_me.fs, core_me.scanner
import hsaudiotag.aiff, hsaudiotag.flac, hsaudiotag.genres, hsaudiotag.id3v1,\
    hsaudiotag.id3v2, hsaudiotag.mp4, hsaudiotag.mpeg, hsaudiotag.ogg, hsaudiotag.wma
from hsaudiotag import aiff, flac, genres, id3v1, id3v2, mp4, mpeg, ogg, wma
import hscommon.conflict
import core.engine, core.fs, core.app
import xml.etree.ElementPath
import gzip
import aem.kae
import appscript.defaultterminology

class PyDupeGuru(PyDupeGuruBase):
    def init(self):
        self = super(PyDupeGuru,self).init()
        self.py = DupeGuruME()
        return self
    
    def removeDeadTracks(self):
        self.py.remove_dead_tracks()
    
    def scanDeadTracks(self):
        self.py.scan_dead_tracks()
    
    #---Information
    @signature('i@:')
    def deadTrackCount(self):
        return len(self.py.dead_tracks)
    
    #---Properties
    def setMinMatchPercentage_(self, percentage):
        self.py.scanner.min_match_percentage = int(percentage)
    
    def setScanType_(self, scan_type):
        try:
            self.py.scanner.scan_type = [
                ScanType.Filename,
                ScanType.Fields,
                ScanType.FieldsNoOrder,
                ScanType.Tag,
                ScanType.Contents,
                ScanType.ContentsAudio,
            ][scan_type]
        except IndexError:
            pass
    
    def setWordWeighting_(self, words_are_weighted):
        self.py.scanner.word_weighting = words_are_weighted
    
    def setMatchSimilarWords_(self, match_similar_words):
        self.py.scanner.match_similar_words = match_similar_words
    
    def enable_scanForTag_(self, enable, scan_tag):
        if enable:
            self.py.scanner.scanned_tags.add(scan_tag)
        else:
            self.py.scanner.scanned_tags.discard(scan_tag)
    
    #---Registration
    def appName(self):
        return "dupeGuru Music Edition"
    
