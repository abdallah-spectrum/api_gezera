from django.shortcuts import render
import os

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import xmlrpc.client
import dotenv
dotenv.load_dotenv()
import os



# third party
# import environ

# env = environ.Env()
# environ.Env.read_env()

# url = os.environ.get('url')
# db = os.environ.get('db')
# username = os.environ.get('db_username')
# password =os.environ.get('password')

url = 'http://localhost:8069'
db = 'Gezira_Live'
username = 'admin@yahoo.com'
password = 'spectrum@2023' 


common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



class AccountItemsList(APIView):
   
    def get(self,request, *args, **kwargs):

        limit = int(request.query_params.get('limit', 10000))
        offset = int(request.query_params.get('offset', 0))

        _id = request.query_params.get('id', None)
        user_type_id = request.query_params.get('user_type_id', None)
        code = request.query_params.get('code', None)
        name = request.query_params.get('name', None)
        domain = []
        if _id:
            domain.append(('id', '=',_id))
        if user_type_id:
            domain.append(('user_type_id', '=',user_type_id))
        if code:
            domain.append(('code', '=',code))
        if name:
            domain.append(('name', 'like',name))
        result = models.execute_kw(db, uid, password, 'account.account', 'search_read', 
                   [domain], {'fields':["code",'name','user_type_id'], 'limit': limit, 'offset': offset})
        items_count= len(result)
        
        return Response({'result': result,'items_count':items_count})





