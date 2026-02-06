with source as (
    
    -- "source" tells dbt to look at the sources.yml file we just made
    select * from {{ source('finance_db', 'raw_stock_data') }}

),

renamed as (

    select
        -- Create a unique key for testing later
        ticker || '-' || date::text as id,
        
        -- Select and cast columns
        date::date as market_date,
        ticker as ticker_symbol,
        
        -- ensure numeric types are correct
        cast(open as float) as open_price,
        cast(high as float) as high_price,
        cast(low as float) as low_price,
        cast(close as float) as close_price,
        cast(volume as int) as volume

    from source

)

select * from renamed
