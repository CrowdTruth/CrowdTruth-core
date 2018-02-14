from pymodm import EmbeddedMongoModel, MongoModel, fields
from pymodm.manager import Manager
import datetime
import job
import unit
import worker


class Judgment(MongoModel):

    class Meta:
        final = True

    id = fields.CharField(primary_key=True)
    collection = fields.CharField()
    job = fields.CharField()
    unit = fields.CharField()
    worker = fields.CharField()

    platform = fields.CharField()

    content = fields.DictField()
    annotations = fields.DictField()

    started = fields.DateTimeField()
    submitted = fields.DateTimeField()
    duration = fields.CharField()

    now = datetime.datetime.utcnow()
    created = fields.DateTimeField(default=now)
    updated = fields.DateTimeField(default=now)

    features = fields.DictField()
    #content = fields.CharField()


    def setAgreement(self, agreement):

        if 'features' not in self:
            self.features = {}
        self.features['agreement'] = agreement
        self.save()



