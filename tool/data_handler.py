import datetime
import requests
import json
import statistics

from worker import Worker
from db_connector import Database


class Handler(Worker):
    """ Main class of the tool:

        Retrieves messages from the queue (always listens)
        Submits data to storage in mysql db
        Queries DB to get patients records if patient still in ICU
        Calls API to compute probability given pat data
    """

    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self.db = Database()
        self.pat_id = None
        self.compute = False

    def handle(self, message):

        print("TOOL RECEINVED MESSAGE: ", message)
        # submit to mysql
        self.store_data(message)

        if self.compute:
            self.query_pat_info()

    def store_data(self, message):
        """ Transforms data and Submits data to MySQL Database in 1 table

        :param message:
        :return:
        """

        self.pat_id = int(message.get('pat_id'))
        date_admission = datetime.datetime.strptime(message.get('date_admission'), '%d/%m/%Y').strftime('%Y-%m-%d')
        date_discharge = message.get('date_discharge')
        if date_discharge == '':
            date_discharge = None
            self.compute = True
        else:
            date_discharge = datetime.datetime.strptime(message.get('date_discharge'), '%d/%m/%Y').strftime('%Y-%m-%d')

        age = float(message.get('age'))
        day = message.get('day')
        hour = int(message.get('hour'))
        parameter = message.get('parameter')
        value = round(float(message.get('value')), 4)

        context = self.db.contextual_cursor

        with context() as cursor:
            cursor.execute(
                '''
                INSERT INTO tooldb.patients (pat_id, date_admission, date_discharge, age, day, hour, parameter, value)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                ''',
                (self.pat_id, date_admission, date_discharge, age, day, hour, parameter, value))
            cursor.commit()

    def query_pat_info(self):
        """ Gets all records belonging to one patient and computes parameters to send to model API
        :return:
        """
        context = self.db.contextual_cursor

        with context() as cursor:
            all_records = cursor.fetch_all(
                '''
                SELECT age, parameter, value FROM tooldb.patients WHERE pat_id = %s AND date_discharge IS NULL'''
                , (self.pat_id,)
            )

            # Get age
            age_pat = all_records[0][0]
            # list of blood pressure vals
            bp = [record[2] for record in all_records if record[1] == 'blood_pressure']
            # list of respiration rate vals
            rr = [record[2] for record in all_records if record[1] == 'respiration_rate']
            mrr = statistics.mean(rr)
            # list of temperature vals
            tp = [record[2] for record in all_records if record[1] == 'temperature']

            if len(tp) > 2:
                stdev_tp = statistics.stdev(tp)
            else:
                stdev_tp = 0.0

            # Invoke API call
            self.call_model_api(age_pat, bp[-1], mrr, stdev_tp)

    def call_model_api(self, age, bp, mrr, stdev_tp):

        url = 'http://modelapi:5000/api/model'

        # Data prep
        values_model = {'age': age,
                        'last_blood_pressure': bp,
                        'rmean_respiration_rate': mrr,
                        'standard_deviation_temperature': stdev_tp}

        # MAke call
        r = requests.post(url, data=json.dumps(values_model))

        # Get result from Model
        print('API OUTPUT: ', r.content)