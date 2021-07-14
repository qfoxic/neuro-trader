//+------------------------------------------------------------------+
//|                                                              rna |
//|                                             Volodymyr Paslavskyy |
//|                                                                  |
//+------------------------------------------------------------------+

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
#include <Generic\Stack.mqh>

#include "utils.mqh"

class Move {
  protected:
    short            start;
    short            stop;
    Move*            next_;
    short            min;
    short            max;

  public:
                     Move(short strt, short stp): start(strt), stop(stp), next_(NULL) {
        min = fmin(start, stop);
        max = fmax(start, stop);
    };
    virtual         ~Move() {}; // TODO. When/what to delete?

    virtual Move*    operator|(Move &other) {
        next_ = GetPointer(other);
        return next_;
    };
    Move*            next() const {
        return next_;
    };
    string             name() const {
        return StringFormat("%i -> %i", start, stop);
    };
    virtual bool             exit(const short level) const {
        return level < min || level > max;
        //return mlevel < min(self.levels) or mlevel > max(self.levels);
    };
    virtual bool     enter(const short level) const = 0;
};


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class Up: public Move {
  public:
                     Up(short strt, short stp): Move(strt, stp) {};
    virtual         ~Up() {}; // TODO. When/what to delete?

    virtual bool     enter(const short level) const override {
        return min < level && level <= max;
        // return min(self.levels) < level <= max(self.levels);
    };
};


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class Down: public Move {
  public:
                     Down(short strt, short stp): Move(strt, stp) {};
    virtual         ~Down() {}; // TODO. When/what to delete?

    virtual bool     enter(const short level) const override {
        return max > level && level >= min;
        
        //return max(self.levels) > mlevel >= min(self.levels)
    };
};


//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class Stop: public Move {
  public:
                     Stop(): Move(0, 0) {};
    virtual         ~Stop() {}; // TODO. When/what to delete?

    virtual bool     enter(const short level) const override {
        return true;
    };
    virtual bool     exit(const short level) const override {
        return true;
    };
};



//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
class MurrayLevelsStateMachine {
  private:
    Move*            root;
    Move*            state;
    MqlRates         last_rate;
    CStack<string>   op_stack;
    double           cur_close_price;
    int              start;
    int              trigger_level;
    int              bn_v1, bn_v2, OctLinesCnt, P;
    double v1, v2, v4, mn, mx, x1, x2, x3, x4, x5, x6, y1,
           y2, y3, y4, y5, y6, octave, fractal, range, finalH,
           finalL, mml[13], dmml, dvtl, sum;
  public:
                     MurrayLevelsStateMachine(Move* node, int trigger): root(node), state(node), trigger_level(trigger) {
        start = 0;
        bn_v1 = 0;
        bn_v2 = 0;
        OctLinesCnt = 13;
        cur_close_price = 0;
        P = 200;
        v1 = 0;
        v2 = 0;
        v4 = 0;
        mn = 0;
        mx = 0;
        x1 = 0;
        x2 = 0;
        x3 = 0;
        x4 = 0;
        x5 = 0;
        x6 = 0;
        y1 = 0;
        y2 = 0;
        y3 = 0;
        y4 = 0;
        y5 = 0;
        y6 = 0;
        octave = 0;
        fractal = 0;
        range = 0;
        finalH = 0;
        finalL = 0;
        dmml = 0;
        dvtl = 0;
        sum = 0;
        calc_murray_levels();
    };
                    ~MurrayLevelsStateMachine() {};

    void             calc_murray_levels() {
        bn_v1 = iLowest(NULL, _Period, MODE_LOW, P, 0);
        bn_v2 = iHighest(NULL, _Period, MODE_HIGH, P, 0);
        v1    = iLow(NULL, _Period, bn_v1);
        v2    = iHigh(NULL, _Period, bn_v2);
//determine fractal.....
        if( v2 <= 250000 && v2 > 25000 )                 fractal  =  100000;
        else if( v2 <= 25000 && v2 > 2500 )              fractal  =   10000;
        else if( v2 <= 2500 && v2 > 250 )               fractal  =    1000;
        else if( v2 <= 250 && v2 > 25 )                fractal  =     100;
        else if( v2 <= 25 && v2 > 12.5 )              fractal  =      12.5;
        else if( v2 <= 12.5 && v2 > 6.25)            fractal  =      12.5;
        else if( v2 <= 6.25 && v2 > 3.125 )         fractal  =       6.25;
        else if( v2 <= 3.125 && v2 > 1.5625 )      fractal  =       3.125;
        else if( v2 <= 1.5625 && v2 > 0.390625 )  fractal  =       1.5625;
        else if( v2 <= 0.390625 && v2 > 0)       fractal  =       0.1953125;
        range    = (v2 - v1);
        sum      = MathFloor(MathLog(fractal / range) / MathLog(2));
        octave   = fractal * (MathPow(0.5, sum));
        mn       = MathFloor(v1 / octave) * octave;
        if( (mn + octave) > v2 )
            mx = mn + octave;
        else
            mx = mn + (2 * octave);
// calculating xx
        if( (v1 >= (3 * (mx - mn) / 16 + mn)) && (v2 <= (9 * (mx - mn) / 16 + mn)))              x2 = mn + (mx - mn) / 2;
        else x2 = 0;
        if( (v1 >= (mn - (mx - mn) / 8))    && (v2 <= (5 * (mx - mn) / 8 + mn)) && (x2 == 0))    x1 = mn + (mx - mn) / 2;
        else x1 = 0;
        if( (v1 >= (mn + 7 * (mx - mn) / 16)) && (v2 <= (13 * (mx - mn) / 16 + mn)))             x4 = mn + 3 * (mx - mn) / 4;
        else x4 = 0;
        if( (v1 >= (mn + 3 * (mx - mn) / 8))  && (v2 <= (9 * (mx - mn) / 8 + mn)) && (x4 == 0))     x5 = mx;
        else x5 = 0;
        if( (v1 >= (mn + (mx - mn) / 8))    && (v2 <= (7 * (mx - mn) / 8 + mn)) && (x1 == 0)
                && (x2 == 0) && (x4 == 0) && (x5 == 0))             x3 = mn + 3 * (mx - mn) / 4;
        else x3 = 0;
        if( (x1 + x2 + x3 + x4 + x5) == 0 )    x6 = mx;
        else x6 = 0;
        finalH = x1 + x2 + x3 + x4 + x5 + x6;
// calculating yy
        if( x1 > 0 )    y1 = mn;
        else y1 = 0;
        if( x2 > 0 )    y2 = mn + (mx - mn) / 4;
        else y2 = 0;
        if( x3 > 0 )    y3 = mn + (mx - mn) / 4;
        else y3 = 0;
        if( x4 > 0 )    y4 = mn + (mx - mn) / 2;
        else y4 = 0;
        if( x5 > 0 )    y5 = mn + (mx - mn) / 2;
        else y5 = 0;
        if( (finalH > 0) && ((y1 + y2 + y3 + y4 + y5) == 0) )    y6 = mn;
        else y6 = 0;
        finalL = y1 + y2 + y3 + y4 + y5 + y6;
        for(short i = 0; i < OctLinesCnt; i++) {
            mml[i] = 0;
        }
        dmml = (finalH - finalL) / 8;
        mml[0] = (finalL - dmml * 2); //-2/8
        for(short i = 1; i < OctLinesCnt; i++) {
            mml[i] = mml[i - 1] + dmml;
        }
    }
    double           get_price_percentage(const double price, const double max_price, const double min_price) {
//Answers a question how close we are to the min in percents. Min == 0%, Max == 100%
        return ((price - min_price) * 100) / (max_price - min_price);
    }

    short            get_murray_level(double price) {
        double mml_price = mml[0];
        short lvl = 0;
        while (price > mml_price) mml_price = mml[++lvl];
        if (lvl <= 0 || lvl >= 12) return lvl;
        short maxLvl = lvl, minLvl = --lvl;
        return get_price_percentage(price, mml[maxLvl], mml[minLvl]) <= 50.0 ? minLvl : maxLvl;
    }
    datetime            get_last_candle_time() const {
        return last_rate.time;
    }
    double            get_last_candle_price() const {
        return last_rate.close;
    }
    double           get_first_candle_price() const {
        // For some reason when trying to store MqlRates it behaves like a static variable.
        return cur_close_price;
    }
    double           get_mml_price(const short lvl) const {
        return mml[lvl];
    }
    double           get_mml_diff() const {
        return pips2price(price2pips(mml[0], mml[1]));
    }
    void             debug_print_ops() {
        while(op_stack.Count() > 0) {
            Print(op_stack.Pop());
        }
    }
    short            move() {
        // return 1 == continue; return 2 == MATCH; return 3 == no match - exit;
        MqlRates rate = next();
        double price = rate.close;
        if (price <= 0) return 3;
        short murray_level = get_murray_level(price);
        if (!murray_level == trigger_level) return 3;
        Move *next_state = NULL;
        op_stack.Add(StringFormat("%s, price %f, low %f, high %f, Total pips %f, Level pips %f, time %s, it %i, lvl %i", state.name(), price, mml[0], mml[12], price2pips(mml[0], mml[12]), price2pips(mml[0], mml[1]), TimeToString(rate.time), start, murray_level));
        if (state.next() == NULL) return 2;
        if (state.enter(murray_level)) next_state = state.next();
        if (state.exit(murray_level)) return 3;
        if (next_state != NULL) state = next_state;
        return 1;
    };

    MqlRates         next() {
        MqlRates rates[1];
        int copied = CopyRates(Symbol(), Period(), start, 1, rates);
        //if (copied <= 0) return -1;
        start++;
        last_rate = rates[0];
        if (cur_close_price == 0.0) cur_close_price = last_rate.close;
        return last_rate;
    }
};
//+------------------------------------------------------------------+
