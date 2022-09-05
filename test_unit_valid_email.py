from class_main import MainApp

def test_wrong_email_address_1():
    assert MainApp.is_valid_email_address('') == False
    
def test_wrong_email_address_2():
    assert MainApp.is_valid_email_address('kk') == False
    
def test_wrong_email_address_3():
    assert MainApp.is_valid_email_address('kk@') == False
    
def test_wrong_email_address_4():
    assert MainApp.is_valid_email_address('<<<>>>') == False
    
def test_wrong_email_address_5():
    assert MainApp.is_valid_email_address('<<<>>>@<<<<>>>>.OO') == False
    
def test_wrong_email_address_6():
    assert MainApp.is_valid_email_address('fawfaw@f.a') == False
    
def test_wrong_email_address_7():
    assert MainApp.is_valid_email_address('Ok..google@oh_shit.com') == False
    
def test_wrong_email_address_8():
    assert MainApp.is_valid_email_address('what\'upDUUDE@@unicyb.org.ua') == False
    
def test_wrong_email_address_9():
    assert MainApp.is_valid_email_address('@help@help.ua') == False

def test_wrong_email_address_10():
    assert MainApp.is_valid_email_address('$aying(R1nGe@is-cringe.com') == False

def test_valid_email_address_1():
    assert MainApp.is_valid_email_address('sth@sth.com') == True

def test_valid_email_address_2():
    assert MainApp.is_valid_email_address('sth.sth@sth.com') == True

def test_valid_email_address_3():
    assert MainApp.is_valid_email_address('SthSthsth@sth.com') == True

def test_valid_email_address_4():
    assert MainApp.is_valid_email_address('Sth.Sth.Sth@sth.com') == True

def test_valid_email_address_5():
    assert MainApp.is_valid_email_address('Sth0111.sTH.01.2@sth.com') == True

def test_valid_email_address_6():
    assert MainApp.is_valid_email_address('Sth0111.sTh.01.2@sth-sth.com') == True

def test_valid_email_address_7():
    assert MainApp.is_valid_email_address('1.2.3.4.5.6.7.8.9@sth.com') == True

def test_valid_email_address_8():
    assert MainApp.is_valid_email_address('dejfwy@gmail.com') == True

def test_valid_email_address_9():
    assert MainApp.is_valid_email_address('vingar@unicyb.kiev.ua') == True
