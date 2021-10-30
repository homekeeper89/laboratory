import factory
from . import RunningFactory, UserFactory, RunningParticipantFactory


class RunningDomainFactory(RunningFactory):
    @factory.post_generation
    def RunningParticipant(self, create, extracted, **kwargs):
        try:
            counts = extracted - 1
        except Exception:
            counts = 0
        RunningParticipantFactory(user_id=self.user_id)
        UserFactory(id=self.user_id)
        if counts >= 1:
            for _ in range(extracted - 1):
                res = RunningParticipantFactory(**kwargs)
                UserFactory(id=res.user_id)


DOMAIN_FACTORIES = [RunningDomainFactory]
