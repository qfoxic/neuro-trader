//+------------------------------------------------------------------+
//|                                                              rna |
//|                                             Volodymyr Paslavskyy |
//|                                                                  |
//+------------------------------------------------------------------+
#include "flows.mqh"


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
bool isNewBar() {
//--- memorize the time of opening of the last bar in the static variable
    static datetime last_time = 0;
//--- current time
    datetime lastbar_time = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE);
//--- if it is the first call of the function
    if(last_time == 0) {
        //--- set the time and exit
        last_time = lastbar_time;
        return(false);
    }
//--- if the time differs
    if(last_time != lastbar_time) {
        //--- memorize the time and return true
        last_time = lastbar_time;
        return(true);
    }
//--- if we passed to this line, then the bar is not new; return false
    return(false);
}

//+------------------------------------------------------------------+
//|                                                          rna.mq5 |
//|                                             Volodymyr Paslavskyy |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit() {
    /*Up up23(2, 3), up45(4, 5);
    Down down32(3, 2), down65(6, 5);
    Stop stop();
    up23 | up45 | down32 | down65 | stop;

    Move* node = GetPointer(up23);
    while (CheckPointer(node) != POINTER_INVALID) {
       node.name();
       node = node.next();
    }*/
    return(INIT_SUCCEEDED);
}
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason) {
//---
}
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick() {
// TODO. Check only on a new candle;
    Up up23(2, 3), up34(3, 4), up45(4, 5);
    Down down32(3, 2), down21(2, 1);
    Stop stop();
    down32 | down21 | stop; // not bad sell config;
    if (isNewBar()) {
        MurrayLevelsStateMachine state_machine(GetPointer(down32));
        int status = 0;
        while (true) {
            status = state_machine.move();
            if (status == 1) {
                continue;
            } else if (status == 2) {
                PrintFormat("YAY got it");
                break;
            };
            break;
        }
    }
}
//+------------------------------------------------------------------+
