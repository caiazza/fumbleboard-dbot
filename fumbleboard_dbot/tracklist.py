import json
import itertools
import logging

class Track:
    """The class representing a track to be managed by the bot"""
    def __init__(self, *, SourceURL, Title, Artist = "FumbleGDR", Tags = []):
        self.SourceURL = SourceURL
        self.Title = Title
        self.Artist = Artist
        self.Tags = Tags
    
    @classmethod    
    def fromdict(self, Data):
        self.SourceURL = Data["SourceURL"]
        # self.SourceFile = Data["SourceFile"]
        self.Title = Data["Title"]
        self.Artist = Data["Artist"]
        self.Tags = Data["Tags"]

    def asdict(self):
        return {"SourceURL":self.SourceURL, "Title":self.Title, "Artist":self.Artist, "Tags":self.Tags}
    
    def __repr__(self):
        return f"Track(SourceURL={self.SourceURL}, Title={self.Title}, Artist={self.Artist}, Tags={self.Tags})"
        

class Tracklist:
    """The list of track loaded by the bot"""
    
    def __init__(self, InList = []):
        self.Tracks = InList
        logging.info('Loaded {} tracks in the tracklist'.format(len(self)))
        
    def __len__(self):
        return len(self.Tracks)