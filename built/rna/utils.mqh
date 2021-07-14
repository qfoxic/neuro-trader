//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
double pips2price(const double pips) {
    return pips * _Point;
}


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
double price2pips(const double p1, const double p2) {
    return MathAbs(p1 - p2) / Point();
}

//+------------------------------------------------------------------+
bool isNewBar() {
//--- memorize the time of opening of the last bar in the static variable
    static datetime last_time = 0;
//--- current time
    datetime lastbar_time = (datetime)SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE);
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
