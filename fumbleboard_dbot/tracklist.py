import json
import itertools
import logging

class Track:
    """The class representing a track to be managed by the bot"""
    def __init__(self, Data):
        self.SourceFile = Data["SourceFile"]
        self.Title = Data["Title"]
        self.Artist = Data["Artist"]
        self.Tags = Data["Tags"]
        

class Tracklist:
    """The list of track loaded by the bot"""
    
    def __init__(self, InList):
        self.Tracks = [Track(Element) for Element in InList]
        logging.info('Loaded {} tracks in the tracklist'.format(len(self)))
        
    def __len__(self):
        return len(self.Tracks)