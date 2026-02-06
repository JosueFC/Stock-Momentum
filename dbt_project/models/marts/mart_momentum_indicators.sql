with stock_data as (
    select * from {{ ref('stg_stock_prices') }}
),

moving_averages as (
    select
        market_date,
        ticker_symbol,
        close_price,
        volume,
        
        -- Calculate 50-day Moving Average
        avg(close_price) over (
            partition by ticker_symbol 
            order by market_date 
            rows between 49 preceding and current row
        ) as ma_50_day,

        -- Calculate 200-day Moving Average
        avg(close_price) over (
            partition by ticker_symbol 
            order by market_date 
            rows between 199 preceding and current row
        ) as ma_200_day

    from stock_data
),

final_signals as (
    select
        *,
        case 
            when ma_50_day > ma_200_day then 'BULLISH'
            when ma_50_day < ma_200_day then 'BEARISH'
            else 'NEUTRAL'
        end as momentum_signal
    from moving_averages
)

select * from final_signals
