import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AeuaeARvSQbaWjTXclZ-93PsMwipYpGgFRGWpCi2C9m-3T8P1jmDmEeTZsRqbM99o2SXyNYyX3g41f-X"
        self.client_secret = "ELzV85lf-cuwm2KfYcMsUey--fe9z0RdjpoIrCRarpxXtyN8Fq-l8I__zVxtYpt0ujKaXeAa7I-0k8q2"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
