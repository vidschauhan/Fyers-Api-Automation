from time import sleep

import credentials as cd
from fyers_apiv3 import fyersModel
import login as l
import popupWindow as popup

global daily_limit, limit_reached_count


def get_position_details() :
    with open('access.txt', 'r') as a:
        access_token = a.read()

    fyers = fyersModel.FyersModel(client_id=cd.client_id, is_async=False, token=access_token, log_path="")
    # Make a request to get the user profile information
    details = fyers.positions()


    if details['code'] != 200:
        print("Token Expired... Generating new access token")
        l.generate_access_token(cd.client_id,cd.secret_key,cd.redirect_uri)
        get_position_details()

    print(details)

    return details['overall']['count_open'],details['overall']['pl_total'],details['overall']['pl_realized'],details['overall']['pl_unrealized'],details['overall']['count_total']

def over_trading_analyser():
    print("\nInside -> over_trading_analyser()")
    print(f"\nToday's Max Loss Limit is :: {daily_limit}\n")


    #returns details['overall']['count_open'],details['overall']['pl_total'],details['overall']['pl_realized'],details['overall']['pl_unrealized']
    positions = get_position_details()

    count_open = positions[0]
    pl_total = positions[1]
    pl_realized = positions[2]
    pl_unrealized = positions[3]
    count_total = positions[4]
    daily_limit_threshold = daily_limit - (0.1 * daily_limit)
    #pl_total = -1872.17
    #pl_realized = -3244.23
    #count_open = 1
    #count_total = 10
    MB_ICONWARNING = 0x00000030
    WS_EX_TOPMOST = 0x40000

    daily_limit_reached_message = (' ******** You have reached daily limit of loss ********* \n\n'
                                   f'MAX LOSS LIMIT {daily_limit} || REALIZED P&L {pl_realized}'
                                   '\n\nSTAY DISCIPLINED. SMALL LOSSES CAN BE RECOVERED.'
                                   '\n\n1.Save Your Capital.'
                                   '\n2.Stop Impulsive Trading. Its not your Day'
                                   '\n3.Remember, There will be opportunity Tomorrow as Well.'
                                   '\n4.The goal is to survive so that you can stay in the GAME << THINK LONG TERM >>'
                                   '\n5.Do not fight with the Market, Do not Revenge Trade.'
                                   '\n\n******** Dont get Emotional,Just close the Terminal. *********'
                                   '\n\nREMEMBER : YOU HAVE TO ESCAPE 9-5 JOB, STAY FOCUSED')

    daily_limit_threshold_message = ('******************* WARNING ******************'
                                     '\n\nSTAY DISCIPLINED. SMALL LOSSES CAN BE RECOVERED.'
                                     '\n\nYou have crossed the threshold loss.'
                                     f'\n\nTHRESHOLD: {daily_limit_threshold} | TOTAL LOSS NOW : {pl_total}'
                                     '\n\nEither close existing trade or Stop Taking more Trades.'
                                     '\n\nREMEMBER : YOU HAVE TO ESCAPE 9-5 JOB, STAY FOCUSED')

    dont_trade_anymore = ('**************** OPEN POSITION FOUND ***************'
                          '\n\nYou have already crossed the Loss Threshold.'
                          '\n\nDO NOT EXECUTE MORE TRADES. STAY DISCIPLINED.'
                          '\n\nConsider exiting all INTRADAY trades.'
                          '\n\nREMEMBER : YOU HAVE TO ESCAPE 9-5 JOB, STAY FOCUSED'
                          '\n\n*********************************************************')

    over_trading_detected = ('############ OVER TRADING DETECTED ############'
                             f'\n\nTotal Number of Trades Today :: {count_total}'
                             f'\nTotal Number of Running Trades :: {count_open}'
                             f'\n\n1.If You are in PROFIT then take this profit Home.'
                             '\n2.If You are in LOSS then time to close the terminal.'
                             '\n3.Remember,The goal is to Survive in the Market'
                             '\n4.You will always get the better opportunities'
                             '\n5.BE A SNIPER TRADER not MACHINE GUNNER.'
                             '\n\nTRADE YOUR PLAN & STICK TO IT'
                             '\n\n############################################')

    trading_awareness = ('############ ONLY TRADE YOUR SETUP ############'
                             f'\n\nALWAYS TRADE YOUR PLAN. STAY DISCIPLINED'
                             f'\nTRADE ONLY A & A+ SETUPS -> LIQUIDITY SWEEP <-'
                             f'\n\n* WAIT FOR YOUR SETUP PATIENTLY.'
                             '\n* LOSS DUE TO BAD DISCIPLINE DESTROY PSYCHOLOGY.'
                             '\n* BIG LOSS GIVES YOU BIG PAIN.'
                             '\n* ALWAYS KEEP YOUR LOSS IN CONTROL.'
                             '\n* REMEMBER : LESS IS MORE.'
                             '\n* PRESERVE YOUR CAPITAL FROM UNNECESSARY RISKS.'
                             '\n\nPROPER RISK MANAGEMENT WILL SAVE YOU IN MARKET.'
                             '\n\n############################################')



    # Trading awareness so that I am trading my plan only.
    if count_total == 0 and pl_total == 0 :
        print("No Trading position for now.")
        popup.AutoCloseMessageBoxW(trading_awareness, 'TRADING PSYCHOLOGY',60, MB_ICONWARNING)
        return

    #Over trading alert if number of all position > 10
    if count_total >= 10 :
        print("Over trading Detected.")
        popup.AutoCloseMessageBoxW(over_trading_detected, f'OVER TRADING ALERT ! Total P&L : {pl_total}',
                                   30, MB_ICONWARNING)


    if pl_total < 0 :

        if pl_total > daily_limit :
            count = 0
            while count <= 5 and pl_realized > daily_limit:
                if pl_total <= daily_limit_threshold:
                    popup.AutoCloseMessageBoxW(daily_limit_threshold_message, f'LOSS THRESHOLD CROSSED !  Total Loss : {pl_total}',
                                         15, MB_ICONWARNING)
                    if count_open > 0:
                        popup.AutoCloseMessageBoxW(dont_trade_anymore,f'DO NOT TRADE ANYMORE ! Total Loss : {pl_total}',15, MB_ICONWARNING)
                sleep(30)
                count = count + 1


        if pl_realized < daily_limit or pl_total < daily_limit:
            count = 0
            while count <= 5 :
                popup.AutoCloseMessageBoxW(daily_limit_reached_message, f'DAILY LIMIT BREACHED -> HARD STOP NOW ! Total Loss : {pl_total}', 30, 16)
                if count_open > 0:
                    popup.AutoCloseMessageBoxW(dont_trade_anymore, f'DO NOT TRADE ANYMORE ! Total Loss : {pl_total}', 20,
                                               16)
                sleep(30)
                count = count + 1

        over_trading_analyser()


def execute():
    global daily_limit
    try:
        while True:
            try:
                daily_limit = -abs(float(input("\nEnter today's Loss Limit of the Day ::  ")))
                break
            except ValueError:
                print("Please input a valid amount in numbers.")

        while True :
            over_trading_analyser()
            sleep(300)
    except:
        print("Error Encountered. Retry...")


if __name__ == '__main__':
    execute()
