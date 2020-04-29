import os
import time
import csv
import json

import asyncio
import aiohttp
from aiohttp_sse import sse_response
from aiohttp.web import Application, Response

from preprocessing import join_data_preprocessing


def row_generator(path):
    """ Generator that yields single rows from csv file

    :param path: file location
    :return: yield row
    """
    with open(path) as csvfile:
        csv_data = csv.reader(csvfile, delimiter=';')
        headers = next(csv_data, None)

        for row in csv_data:

            message = dict(zip(headers, row))
            json_mess_en = json.dumps(message)
            yield json_mess_en


# Async stream
async def subscribe(request):

    print('new sub created!')

    data_dir = os.environ.get('DATA_DIR', '/data/')
    data_file = os.environ.get('FILE_ALL', 'all_data.csv')
    data_loc = os.path.join(data_dir, data_file)

    if not os.path.isfile(data_loc):
        join_data_preprocessing()

    # instantiate generator
    r = row_generator(data_loc)

    print('\n REQUEST MADE WAS: ', request)

    async with sse_response(request) as resp:

        while True:
            try:
                await asyncio.sleep(1)
                await resp.send(next(r))
            except StopIteration: #catches end of generator
                break
        return resp


# grab asyncio eventloop
loop = asyncio.get_event_loop()
# instantiate app
app = Application(loop = loop)
# define route
app.router.add_route('GET', '/sub', subscribe)


if __name__ == "__main__":
    # startup
    aiohttp.web.run_app(app, host='0.0.0.0', port=8080)