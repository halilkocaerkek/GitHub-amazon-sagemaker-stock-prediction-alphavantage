import sys
import socket
import pandas as pd
from dateutil import parser

def read_historical_data_socket(sock, recv_buffer=4096):
    """
    Read the information from the socket, in a buffered
    fashion, receiving only 4096 bytes at a time.

    Parameters:
    sock - The socket object
    recv_buffer - Amount in bytes to receive per read
    """
    buffer = ""
    data = ""
    while True:
        data = sock.recv(recv_buffer)        
        buffer += data.decode()

        # Check if the end message string arrives
        if "!ENDMSG!" in buffer:
            break
   
    # Remove the end message string
    buffer = buffer[:-12]
    return buffer

if __name__ == "__main__":
    # Define server host, port and symbols to download
    host = "127.0.0.1"  # Localhost
    port = 9100  # Historical data socket port
    #syms = ["SPY"]
    syms = ['INTC','NFLX','GOOG','GOOGL','FB','ORCL','GS','XOM','AMZN','SPY','TU','C','CSCO','CR','GE','GM','HON','JNJ','JPM','KO','MCD','MSFT','ORCL','SUNW','SYAAF','UOMO','VZ','WMT','XOM','MMM','SPY','VOD','VIRT','AAPL','MMC','AAL','CEA','LUV','SAVE','UAL','HD','LULU','ANF','FL','GPS','RL','URBN','F','TSLA','FCAU','VWAGY','RACE']
    syms = ['RL','URBN','F','TSLA','FCAU','VWAGY','RACE']
    syms = ['ADM','BAYRY','BG','CF','CTVA','NTR','FMC','TSN','KO','PG','PEP']

    # Download each symbol to disk
    for sym in syms:
        print ("Downloading symbol: {}...".format(sym))

        # Construct the message needed by IQFeed to retrieve data   

        rate='60' # seconds
        startDate = '20191025' # YYYYMMDD
        startDateTime = '075000' # HHMMSS
        startTime = '093000'
        endTime = '160000'
        message = "HIT,{},{},{} {},,,{},{},1\n".format(sym, rate, startDate,startDateTime, startTime, endTime)

        # Open a streaming socket to the IQFeed server locally
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send the historical data request
        # message and buffer the data
        sock.sendall(message.encode())
        data = read_historical_data_socket(sock)
        sock.close

        # Remove all the endlines and line-ending
        # comma delimiter from each record
        data = "".join(data.split("\r"))
        data = data.replace(",\n","\n")[:-1]

        # convert csv to dataframe
        data = pd.DataFrame([data.split(',') for data in data.split('\n')])
        #print(data.head())

        # update column names
        # [YYYY-MM-DD HH:mm:SS],[OPEN],[LOW],[HIGH],[CLOSE],[VOLUME],[OPEN INTEREST]
        data['Mnemonic']=sym
        data['ISIN']=''
        data['SecurityDesc']=''
        data['SecurityType']='Common stock'
        data['Currency']=''
        data['SecurityID']=''
    # data['Time']=data['date'].time()
        data['NumberOfTrades'] = 1
        data=data.rename(columns={1: "StartPrice", 3: "MaxPrice", 2:"MinPrice", 4:"EndPrice", 5:"TradedVolume"})
        
        data.set_index(0, inplace=True)

        for i in data.index:
            time = parser.parse(i) 
            data.at[i, 'Time'] =  time.time()
            data.at[i, 'Date'] =  time.date()

        print('{} : {}'.format(sym, data.shape))
        #print(data.head())
        # Write the data stream to disk
        filename =  'data/download/{}.csv'.format( sym )

        data.to_csv(filename)  
        print(filename)