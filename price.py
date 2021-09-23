import numpy as np
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
api_key = "hbOfUeQs7wRpllIrZfbXgxRMNudnWybfoyE4MOhtO2nU2iuHta5A21TxHpapWRSY"
api_secret = "Zhb9OuU8g3zUmUmabxxZwdL9AGT21eOBTPR7VsUmNUrNxzzO3GvMSuZvNP6BIhxf"
client = Client(api_key, api_secret)  # 用自己創立的Key,Secret登入binance帳戶
def GetEma(CloseList,_len):
    EmaList = []
    ema_len = _len
    k = 2/(ema_len + 1)
    for i in range(len(CloseList)):
        if(i == 0):
            EmaList.append(CloseList[i])
        else:
            ema_last = EmaList[i-1]
            TempEma = (CloseList[i]*k) + (ema_last*(1-k))
            EmaList.append(TempEma)
    return EmaList

def GetEVolume(VolumeList,_len):
    EVolume = []
    k = 2/(_len + 1)
    for i in range(len(VolumeList)):
        if(i == 0):
            EVolume.append(VolumeList[i])
        else:
            volume_last = VolumeList[i-1]
            Temp = (VolumeList[i]*k) + (volume_last*(1-k))
            EVolume.append(Temp)
    return EVolume

def GetPrice(Coin_Money,Interval,Time_Interval):
    OpenList = []
    CloseList = []
    HighList = []
    LowList = []
    VolumeList = []
    NumOfTradeList = []
    AvList = []
    Time = []
    i = 0
    # 讀取K線
    for kline in client.get_historical_klines(Coin_Money, Interval,  Time_Interval):
        Open = float(kline[1])
        OpenList.append(Open)
        High = float(kline[2])
        HighList.append(High)
        Low = float(kline[3])
        LowList.append(Low)
        Close = float(kline[4])
        CloseList.append(Close)
        Volume = float(kline[5])
        VolumeList.append(Volume)
        Trade = float(kline[8])
        NumOfTradeList.append(Trade)
        TempAv = (Open + Close)/2
        AvList.append(TempAv)
        Time.append(i)
        i += 1
    klines = [OpenList,CloseList,HighList,LowList,VolumeList,NumOfTradeList,AvList,Time]
    return klines

def Show(klines,Ema):
    plttime = 0
    if(plttime == 0):
        Data = [go.Candlestick(x=klines[7], open=klines[0], high=klines[2], low=klines[3],
                            close=klines[1], increasing_line_color='red', decreasing_line_color='green'),
                go.Scatter(
            x=klines[7],
            y=Ema,
            name='EMA',
            mode='lines',
            line=go.Line(
                color='#77AAFF'
            )
        )]
        fig = go.Figure(Data)

        fig.show()
        plttime = 1

def GetKlineState(Open,Close,High,Low):
    #print(Open,Close,High,Low)
    state = ''
    if Close >= Open:
        state = 'Green'
        if High >Close:
            upcandle = True
        else:
            upcandle = False
        if Low < Open:
            downcandle = True
        else:
            downcandle = False
    else:
        state = 'Red'
        if High > Open:
            upcandle = True
        else:
            upcandle = False
        if Low < Close:
            downcandle = True
        else:
            downcandle = False
    candle = ''
    candle = candle + state
    
    if upcandle:
        candle = candle + 'Up'
    if downcandle:
        candle = candle + 'Down'''
    return candle

def WinOrLose(Close,High,Low,nowtime):
    state = True
    time = nowtime + 1
    startprice = Close[nowtime]
    winprice = startprice * 1.01
    loseprice = startprice * 0.993
    answer = 0
    while state:
        if time >= len(Close) -2:
            break
        high = High[time]
        low = Low[time]
        if loseprice >= low:
            state = False
        elif winprice <= high:
            answer = 1
            state = False
        else:
            time += 1
        #print(f'現在測試時間 :{nowtime},起始價格 :{startprice},測試價格為 :{price},斜率為 :{(price - startprice)/startprice}')
    return answer
     

def GetData(Coin_Money,Interval,Time_Interval,klen):
    #Coin = "BTC"    # 設定貨幣為"..."
    #Money = "USDT"  # 設定法幣為為"...""
    #Coin_Money = Coin + Money
    #Interval = Client.KLINE_INTERVAL_5MINUTE
    #Time_Interval = "5 day ago UTC"
    klines = GetPrice(Coin_Money, Interval, Time_Interval)
    EmaLen = klen
    Ema = GetEma(klines[1], EmaLen)
    EVolume = GetEVolume(klines[4], klen)
    #Show(klines,Ema)
    Open = klines[0]
    Close = klines[1]
    High = klines[2]
    Low = klines[3]
    Volume = klines[4]
    Trade = klines[5]
    Av = klines[6]
    Time = klines[7]
    X = [] #Ma斜率,價格斜率,價格是否大於ma,移動平均volume斜率,9跟k線狀態,k線型態
    Y = [] #是否成功
    '''
    for i in range(len(Open)):
        if i < EmaLen:
            continue
        else:
            Ema_Angle = ((Ema[i] - Ema[i-1]) / Ema[i-1]) 
            Price_Angle = ((Close[i] - Close[i-1]) / Close[i-1]) 
            if Close[i] >= Ema[i]:
                BullOrBear = 1
            else:
                BullOrBear = 0
            
            EVolume_angle = (EVolume[i] - EVolume[i-1]) / EVolume[i-1]
            Candle = GetKlineState(Open[i], Close[i], High[i], Low[i])
            #print(f'EMA:{Ema_Angle},PRICE:{Price_Angle},BullOrBear:{BullOrBear},VOLUME:{EVolume_angle},CANDLE:{Candle}')
            X.append([Ema_Angle,Price_Angle,BullOrBear,EVolume_angle])
            win = WinOrLose(Close, High, Low, i)
            #print(win)
            Y.append(win)'''
    for i in range(len(Open)):
        X.append([Open,Close,High,Low,Volume,Trade])
        win = WinOrLose(Close, High, Low, i)
        Y.append(win)
    X = np.array(X)
    Y = np.array(Y)
    return X,Y


if __name__ == '__main__':
    X,Y = GetData('BTCUSDT','15m', '5 day ago UTC', 89)
    print(X.shape,Y.shape)
    print(X[0],Y[0])