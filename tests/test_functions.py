import pytest 
from functions import *
#from faker import Faker

 
@pytest.fixture
def test_register_successful (): 
    Register = register ('João', 'joao@gmail.com', '123456')
 #   app = Flask (__name__)
  #  app.config ['TESTING'] =True
   # fake= Faker()
    #form_data= {
     #  'username' : fake.random_username(),
      #  'email' : fake.random_email(),
       # 'password' : fake.random_password ()}
    

    #result =register (form_data )

    assert Register.username == 'João'
    assert Register.email == 'joao@gmail.com'
    assert Register.password == '123456'
     