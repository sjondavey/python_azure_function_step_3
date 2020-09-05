import logging

from .. import stock_forwards_mc
import json
import numpy as np
from ast import literal_eval
import azure.functions as func


def main(myblob: func.InputStream, EEOutputBlob: func.Out[func.InputStream]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    msg = myblob.read()
    try:
        data = literal_eval(msg.decode('utf8'))
    except:
        func.HttpResponse('Unable to read input blob', status_code=400)
    else:
        try:
            portfolio_df = stock_forwards_mc.convert_dict_to_dataframe(data)
        except ValueError as e:
            logging.info(str(e))
    
    mc = stock_forwards_mc.StockForwardMC(portfolio_df)
    expected_values = mc.get_expected_value()
    ev_as_string = np.array2string(expected_values, precision=2, separator=', ', max_line_width=1000000)
    response_str = '"Expected Value":' + ev_as_string
    response_json = json.dumps(response_str)
    EEOutputBlob.set(response_str)
