import asyncio
import GetterPriceBinance



async def main():
    
    sth = GetterPriceBinance.book_ticker_price_binance(symbol='BTCUAH')
    await asyncio.sleep(15)
    print(sth.get_price('BTCUAH'))
    
    
if __name__ == '__main__':
    asyncio.run(main())