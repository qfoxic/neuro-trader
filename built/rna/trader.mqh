//+------------------------------------------------------------------+
//|                                                              rna |
//|                                             Volodymyr Paslavskyy |
//|                                                                  |
//+------------------------------------------------------------------+
#include <Trade\Trade.mqh>
#include <Generic\Stack.mqh>


class Op {
  protected:
    CTrade           trade;
  public:
                     Op() {};
    virtual         ~Op() {};
    virtual void     perform(MurrayLevelsStateMachine* st) = 0;
};


class BuyOp: public Op {
  public:
                     BuyOp() {};
    virtual         ~BuyOp() {};
    virtual void     perform(MurrayLevelsStateMachine* stm) override {
        /*double price = stm.get_first_candle_price();
        short lvl = stm.get_murray_level(price);
        short st_lvl = (short)fmax(0, lvl - 1);
        short tp_lvl = (short)fmin(12, lvl + 2);
        double st = stm.get_mml_price(st_lvl);
        double tp = stm.get_mml_price(tp_lvl);
        // st = price - pips2price(fmax(price2pips(price, st), 300));
        PrintFormat("=======BUY P %f, TK %f, ST %f, ST Pips %f, TP Pips %f, TP_LVL %i, ST_LVL %i", price, tp, st, price2pips(price, st), price2pips(price, tp), tp_lvl, st_lvl);
        */
        double price = stm.get_first_candle_price();
        double mml_diff = stm.get_mml_diff();
        double st = price - (2 * mml_diff);
        double tp = price + (2 * mml_diff);
        PrintFormat("=======BUY P %f, TK %f, ST %f, ST Pips %f, TP Pips %f", price, tp, st, price2pips(price, st), price2pips(price, tp));
        trade.Buy(1.0, Symbol(), 0.0, st, tp);
        price = st;
        st = price - (2 * mml_diff);
        tp = price + (2 * mml_diff);
        trade.BuyLimit(2.0, price, Symbol(), st, tp);
        // TODO. Play with stoploss.
        // TODO. Lets try to sell as well in this trader. Just configure stoplosses.
        // TODO. Add floating stop losses.
        // TODO. Why not to put opposite pending orders
    };
};

class SellOp: public Op {
  public:
                     SellOp() {};
    virtual         ~SellOp() {};
    virtual void     perform(MurrayLevelsStateMachine* stm) override {
        double price = stm.get_first_candle_price();
        double mml_diff = stm.get_mml_diff();
        double st = price + (1 * mml_diff);
        double tp = price - (2 * mml_diff);
        PrintFormat("=======SELL P %f, TK %f, ST %f, ST Pips %f, TP Pips %f", price, tp, st, price2pips(price, st), price2pips(price, tp));
        trade.Sell(1.0, Symbol(), 0.0, st, tp);
        // TODO. Play with stoploss.
        // TODO. Lets try to sell as well in this trader. Just configure stoplosses.
        // TODO. Add floating stop losses.
        // TODO. Why not to put opposite pending orders
    };
};


class TraderStrategy {
  private:
    MurrayLevelsStateMachine* state_machine;
    Op*              ops;
  public:
                     TraderStrategy() {};
                     TraderStrategy(MurrayLevelsStateMachine* signal, Op* op) : state_machine(signal), ops(op) {};
                    ~TraderStrategy() {};
    short            status() const {
        return state_machine.move();
    };
    datetime         get_last_candle_time() const {
        return state_machine.get_last_candle_time();
    };
    void             do_operation() const {
        ops.perform(state_machine);
        state_machine.debug_print_ops();
    };
};


class RNATrader {
  private:
    CStack<TraderStrategy*>       strategies;

  public:
                     RNATrader() {};
                    ~RNATrader() {
        strategies.Clear();
    };
    void             addStrategy(TraderStrategy *strategy) {
        strategies.Push(strategy);
    }
    void             start_loop() {
        static datetime last_date = 0;
        if (isNewBar()) {
            while(strategies.Count() > 0) {
                TraderStrategy strategy = strategies.Pop();
                int status = 0;
                while (true) {
                    status = strategy.status();
                    if (status == 1) {
                        continue;
                    } else if (status == 2) {
                        datetime machine_time = strategy.get_last_candle_time();
                        int time_diff = (int)MathAbs(last_date - machine_time) / PeriodSeconds();
                        if (time_diff >= 10) strategy.do_operation();
                        last_date = machine_time;
                        break;
                    };
                    break;
                }
            }
        }
    }
};
//+------------------------------------------------------------------+
