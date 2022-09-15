from src.price_provider.price_storage import PriceStorage, symbol_t

def test_price_storage():
    sth = PriceStorage()
    sth.update_price(symbol_t('BTCUAH'), price=800000)
    assert sth.get_price(symbol_t('BTCUAH')) == 800000
