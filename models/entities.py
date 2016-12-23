from pymodm import EmbeddedMongoModel, MongoModel, fields
from pymodm.manager import Manager
import datetime


class CollectionManager(Manager):
    def comment_counts(self):
        '''Get a map of title -> # comments for each Post.'''
        return 'blap'



    #created = fields.DateTimeField()
    #updated = fields.DateTimeField()



class Collection(MongoModel):
    
    class Meta:
        final = True

    id = fields.CharField(primary_key=True)

    objects = CollectionManager()

    #jobs = fields.ReferenceField(Job)
    #units = fields.EmbeddedDocumentListField(Unit)
    #workers = fields.EmbeddedDocumentListField(Worker)
    #judgments = fields.EmbeddedDocumentListField(Judgment)

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)



class Job(MongoModel):

    class Meta:
        final = True

    id = fields.CharField(primary_key=True)
    collection = fields.ReferenceField(Collection)
    #units = fields.EmbeddedDocumentListField(Unit)
    #workers = fields.EmbeddedDocumentListField(Worker)
    #judgments = fields.EmbeddedDocumentListField(Judgment)

    platform = fields.CharField()
    #completion = fields.CharField()
    #cost = fields.CharField()

    #started = fields.DateTimeField()
    #ended = fields.DateTimeField()
    #duration = fields.CharField()
    #judgmentCount
    #unitCount

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)




class UnitManager(Manager):

    def refresh(self):
        self.update(
            {'$set': 
                {'judgments': Judgment.objects.raw({'unit': self}).count()}
            }
        )


class Unit(MongoModel):
    id = fields.CharField(primary_key=True)
    collection = fields.ReferenceField(Collection)
    job = fields.ReferenceField(Job)
    workers = fields.ListField()
    judgments = fields.ListField()
    platform = fields.CharField()
    content = fields.DictField()

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)

    workers = fields.ListField()

    objects = UnitManager()
    class Meta:
        final = True

    def getFeatures(self):
        self.features = {}
        self.features['judgments'] = Judgment.objects.raw({'unit': self.id}).count()


class Worker(MongoModel):

    id = fields.CharField(primary_key=True)
    platform = fields.CharField()
    flagged = fields.BooleanField(default=False)
    blocked = fields.BooleanField(default=False)

    features = fields.DictField()

    #city = fields.CharField()
    #country = fields.CharField()
    #region = fields.CharField()
    class Meta:
        final = True
    #first_seen = fields.DateTimeField()
    #last_seen = fields.DateTimeField()

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)

    def getFeatures(self):
        self.features = {}
        self.features['judgments'] = Judgment.objects.raw({'worker': self.id}).count()


class Judgment(MongoModel):

    class Meta:
        final = True

    id = fields.CharField(primary_key=True)
    collection = fields.ReferenceField(Collection)
    job = fields.ReferenceField(Job)
    unit = fields.ReferenceField(Unit)
    worker = fields.ReferenceField(Worker)

    platform = fields.CharField()

    content = fields.DictField()
    annotationVector = fields.DictField()

    started = fields.DateTimeField()
    submitted = fields.DateTimeField()
    duration = fields.CharField()

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)

    #content = fields.CharField()




