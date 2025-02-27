from tvDatafeed import TvDatafeed, Interval
from talipp.indicators import (   # https://nardew.github.io/talipp/latest/
    EMA, ADX, ATR, AO, BB, CCI, EMV, Ichimoku, KVO, ALMA, DEMA,
    HMA, KAMA, SMA, SMMA, T3, TEMA, VWMA, WMA, ZLEMA, MACD, ParabolicSAR,
    ROC, RSI, StdDev, Stoch, StochRSI, VTX
)
from talipp.ohlcv import OHLCVFactory
import matplotlib.pyplot as plt


def add_indicator_to_df(indicator_name, indicator_data, df):
    df[indicator_name] = indicator_data
    return df


def extract_attr(items, attr_name):
    res = []
    for item in items:
        if item is not None:
            res.append(getattr(item, attr_name))
        else:
            res.append(None)
    return res


if __name__ == "__main__":
    tv = TvDatafeed()

    df = tv.get_hist(
        "BTCUSD",
        exchange="BITSTAMP",
        interval=Interval.in_daily,
        n_bars=1_000_000
    )
    ohlcv = OHLCVFactory.from_dict(
        {
            "open": df["open"].values,
            "close": df["close"].values,
            "high": df["high"].values,
            "low": df["low"].values,
            "volume": df["volume"].values,
        }
    )

    # EMA
    ema_period = 9
    ema = EMA(period=ema_period, input_values=df["close"].values)
    df = add_indicator_to_df(
        indicator_name="EMA",
        indicator_data=ema,
        df=df
    )

    # ADX
    di_period = 14
    adx_period = 14
    adx = ADX(
        di_period, adx_period, ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="ADX",
        indicator_data=extract_attr(adx, "adx"),
        df=df
    )

    # SMA
    sma_period = 9
    sma = SMA(period=sma_period, input_values=df["close"].values)
    df = add_indicator_to_df(
        indicator_name="SMA",
        indicator_data=sma,
        df=df
    )

    # ATR
    atr_period = 14
    atr = ATR(
        atr_period, ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="ATR",
        indicator_data=atr,
        df=df
    )

    # AO
    fast_period = 5
    slow_period = 34
    ao = AO(
        fast_period=fast_period,
        slow_period=slow_period,
        input_values=ohlcv,
    )
    df = add_indicator_to_df(
        indicator_name="AO",
        indicator_data=ao,
        df=df
    )

    # BB
    period = 20
    std_dev_mult = 2
    bb = BB(
        period=period,
        std_dev_mult=std_dev_mult,
        input_values=df["close"]
    )
    df = add_indicator_to_df(
        indicator_name="BB_lb",
        indicator_data=extract_attr(bb, "lb"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="BB_ub",
        indicator_data=extract_attr(bb, "ub"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="BB_cb",
        indicator_data=extract_attr(bb, "cb"),
        df=df
    )

    # CCI
    period = 20
    cci = CCI(
        period=period,
        input_values=ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="CCI",
        indicator_data=cci,
        df=df
    )

    # EMV
    # Ease of Movement.
    period = 14
    volume = 10000
    emv = EMV(
        period=period,
        volume_div=volume,
        input_values=ohlcv,
    )
    df = add_indicator_to_df(
        indicator_name="EMV",
        indicator_data=emv,
        df=df
    )

    # Ichimoku
    ichimoku = Ichimoku(
        kijun_period=26,
        tenkan_period=9,
        chikou_lag_period=26,
        senkou_slow_period=52,
        senkou_lookup_period=26,
        input_values=ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="ichimoku_base_line",
        indicator_data=extract_attr(ichimoku, "base_line"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="ichimoku_conversion_line",
        indicator_data=extract_attr(ichimoku, "conversion_line"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="ichimoku_lagging_line",
        indicator_data=extract_attr(ichimoku, "lagging_line"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="ichimoku_cloud_leading_fast_line",
        indicator_data=extract_attr(ichimoku, "cloud_leading_fast_line"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="ichimoku_cloud_leading_slow_line",
        indicator_data=extract_attr(ichimoku, "cloud_leading_slow_line"),
        df=df
    )

    # KVO
    kvo = KVO(
        fast_period=34,
        slow_period=55,
        input_values=ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="KVO",
        indicator_data=kvo,
        df=df
    )

    # alma
    alma = ALMA(period=9, offset=0.85, sigma=6, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="ALMA",
        indicator_data=alma,
        df=df
    )

    # DEMA: Double EMA
    dema = DEMA(period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="DEMA",
        indicator_data=dema,
        df=df
    )

    # HMA
    hma = HMA(period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="HMA",
        indicator_data=hma,
        df=df
    )

    # KAMA
    kama = KAMA(
        period=14,
        fast_ema_constant_period=2,
        slow_ema_constant_period=30,
        input_values=df["close"]
    )
    df = add_indicator_to_df(
        indicator_name="KAMA",
        indicator_data=kama,
        df=df
    )

    # SMMA
    smma = SMMA(period=7, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="SMMA",
        indicator_data=smma,
        df=df
    )

    # T3
    t3ma = T3(period=5, factor=0.7, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="T3MA",
        indicator_data=t3ma,
        df=df
    )

    # TEMA: Triple EMA
    tema = TEMA(period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="TEMA",
        indicator_data=tema,
        df=df
    )

    # VWMA
    vwma = VWMA(period=20, input_values=ohlcv)
    df = add_indicator_to_df(
        indicator_name="VWMA",
        indicator_data=vwma,
        df=df
    )

    # WMA
    wma = WMA(period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="WMA",
        indicator_data=wma,
        df=df
    )

    # ZLEMA
    zlema = ZLEMA(period=14, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="ZLEMA",
        indicator_data=zlema,
        df=df
    )

    # MACD
    macd = MACD(fast_period=12, slow_period=26, signal_period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="MACD_macd",
        indicator_data=extract_attr(macd, "macd"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="MACD_signal",
        indicator_data=extract_attr(macd, "signal"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="MACD_histogram",
        indicator_data=extract_attr(macd, "histogram"),
        df=df
    )

    # ParabolicSAR
    parabolic_sar = ParabolicSAR(
        init_accel_factor=0.02,
        accel_factor_inc=0.02,
        max_accel_factor=0.2,
        input_values=ohlcv
    )
    df = add_indicator_to_df(
        indicator_name="ParabolicSAR_value",
        indicator_data=extract_attr(parabolic_sar, "value"),
        df=df
    )

    # ROC
    roc = ROC(period=9, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="ROC",
        indicator_data=roc,
        df=df
    )

    # RSI
    rsi = RSI(period=14, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="RSI",
        indicator_data=rsi,
        df=df
    )

    # StdDev
    stddev = StdDev(period=20, input_values=df["close"])
    df = add_indicator_to_df(
        indicator_name="StdDev",
        indicator_data=stddev,
        df=df
    )

    # Stoch
    stoch = Stoch(period=14, smoothing_period=1, input_values=ohlcv)
    df = add_indicator_to_df(
        indicator_name="Stoch_d",
        indicator_data=extract_attr(stoch, "d"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="Stoch_k",
        indicator_data=extract_attr(stoch, "k"),
        df=df
    )

    # StochRSI
    stoch_rsi = StochRSI(
        rsi_period=14,
        stoch_period=14,
        k_smoothing_period=3,
        d_smoothing_period=3,
        input_values=df["close"]
    )
    df = add_indicator_to_df(
        indicator_name="StochRSI_k",
        indicator_data=extract_attr(stoch_rsi, "k"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="StochRSI_d",
        indicator_data=extract_attr(stoch_rsi, "d"),
        df=df
    )

    # VTX
    vtx = VTX(period=14, input_values=ohlcv)
    df = add_indicator_to_df(
        indicator_name="VTX_plus_vtx",
        indicator_data=extract_attr(vtx, "plus_vtx"),
        df=df
    )
    df = add_indicator_to_df(
        indicator_name="VTX_minus_vtx",
        indicator_data=extract_attr(vtx, "minus_vtx"),
        df=df
    )

    print(df.head())
    df.to_csv("BTCUSD_BITSTAMP_ALL_DAILY.csv")
    # plt.plot(df["EMA"], label="EMA")
    # plt.legend()
    # plt.savefig('plt.png')
