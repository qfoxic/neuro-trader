//+------------------------------------------------------------------+
//|                                                              rna |
//|                                             Volodymyr Paslavskyy |
//|                                                                  |
//+------------------------------------------------------------------+
#include "states.mqh"
#include "trader.mqh"


//+------------------------------------------------------------------+
//|                                                                  |


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
    Up up01(0, 1), up12(1, 2), up23(2, 3), up34(3, 4), up45(4, 5),
       up56(5, 6), up67(6, 7), up78(7, 8), up89(8, 9), up910(9, 10),
       up1011(10, 11), up1112(11, 12);
    Down down1211(12, 11), down1110(11, 10), down109(10, 9), down98(9, 8),
         down87(8, 7), down76(7, 6), down65(6, 5), down54(5, 4),
         down43(4, 3), down32(3, 2), down21(2, 1), down10(1, 0);
    Stop stop();
// Buy always win.
   down32 | down21 | stop; // pullback 1h 3. 28 pos. large buys, small loses. st:tp=1:2(28% win),2:2(35% win)
   up23 | up12 | stop; // perfect pullback 1h 3. 24 pos. good buys, small loses. st:tp=1:2(66% win),2:2(66% win). good for pending sells.
   up910 | up1011 | stop; // breakout 1h 9. 42 pos. good buys, small loses. st:tp=1:2(47% win),2:2(57% win) good for pending sells
   down109 | down1110 | stop; // perfect breakout 1h, 9. 18 pos. large buys, small loses. st:tp=1:2(44% win),2:2(66% win) good for martingail.
//MurrayLevelsStateMachine state_machine(GetPointer(down32), 3);
// Sell ops
    BuyOp buy_op;
    SellOp sell_op;
    // BUY
    MurrayLevelsStateMachine b1(&up23, 3);
    //MurrayLevelsStateMachine b2(&up910, 9);
    //MurrayLevelsStateMachine b3(&down109, 9);
    //MurrayLevelsStateMachine b4(&down32, 3);
    TraderStrategy st23_11(&b1, &buy_op);
    //TraderStrategy st23_12(&b2, &buy_op);
    //TraderStrategy st23_13(&b3, &buy_op);
    //TraderStrategy st23_14(&b4, &buy_op);
    
    // SELL
    //down1110 | down1211 | stop;
    //MurrayLevelsStateMachine b2(&down1110, 10);
    //TraderStrategy st109_1110(&b2, &sell_op);
    
    
    RNATrader trader;
    trader.addStrategy(&st23_11);
    //trader.addStrategy(&st23_12);
    //trader.addStrategy(&st23_13);
    //trader.addStrategy(&st23_14);
    //trader.addStrategy(&st109_1110);
    trader.start_loop();
    
    /*MurrayLevelsStateMachine sell_signal(GetPointer(up910), 9);
    SellOp sell_op;
    RNATrader trader_sell(GetPointer(sell_signal), GetPointer(sell_op));
    trader_sell.start_loop();*/
    //TODO. Instead of using levels for tp, st - calc level dist in pips and just multiply it.
    //TODO. Please rewrite buy as sell and test all strategies.
    //TODO. Please use parameter for a symbol.
}
//+------------------------------------------------------------------+
