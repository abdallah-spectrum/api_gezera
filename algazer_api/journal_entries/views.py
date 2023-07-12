from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound
import dotenv
dotenv.load_dotenv()
import os


# Create your views here.
import xmlrpc.client

# url = os.environ.get('url')
# db = os.environ.get('db')
# username = os.environ.get('db_username')
# password =os.environ.get('password')
url = 'http://localhost:8069'
db = 'Gezira_Live'
username = 'admin@yahoo.com'
password = 'spectrum@2023' 

# password = env('DATABASE_PASS')
common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))








class CreateJournalItem(APIView):


    def post(self,request):

        
        ref = request.data.get('ref', None)
        account_items = request.data.get('account_items', None)
        currency = request.data.get('currency', None)
        created_date = request.data.get('created_date', None)
        note = request.data.get('note', None)
        	
        miscellaneous_operations_id = 3
        # try:

        # journal data 
        journal_entry_data = {
            'ref': ref,
            'journal_id':miscellaneous_operations_id,
            'date':created_date,
            'narration':note,
            'currency_id':currency,
            
            
        }
        account_move_id = models.execute_kw(db, uid, password, 'account.move', 'create', [journal_entry_data
        ])


        # loop all lines except last one check balnce off
        for item_index in range(0 , len(account_items) -1):
             models.execute_kw(db, uid, password, 'account.move.line', 'create',
                            [{
                            'move_id': account_move_id, 
                            **account_items[item_index]  
                            }],{'context' :{'check_move_validity': False}})

                            # 
        # last entry check balance   on
        models.execute_kw(db, uid, password, 'account.move.line', 'create',
                            [{
                            'move_id': account_move_id, 
                            **account_items[-1]  
                            }],{'context' :{'check_move_validity': True}})
               

        

        # post created journal 
        account_move_object = models.execute_kw(db, uid, password, 'account.move', 'search_read', 
                [[('id', '=',account_move_id)]], {'fields':["id",'name','amount_total_signed'],})
        try:
            models.execute_kw(db, uid, password, 'account.move', 'action_post', [[account_move_object[0]['id']]])
        except Exception as e:
            return Response({'error': str(e)}, status=500)

        return Response({'result':account_move_id ,'Status':bool(account_move_id)})




class CancelJournal(APIView):
   
    def post(self,request):


        ref = request.data.get('ref', None)
        note = request.data.get('note',None)

        # account_items = request.data.get('account_items', None)
        # created_date = request.data.get('created_date', None)
        currency = request.data.get('currency', None)
        # search by reference 
        move_ids = models.execute_kw(db,uid, password,'account.move','search',[[['ref','=',ref]]])
        if not move_ids:

            return Response({"message":'cant find invoice number'},status=404 ) 
        # reverse journal 
        miscellaneous_operations_id = 3
        reversal_id = models.execute_kw(db, uid, password, 'account.move.reversal', 'create', [{
             'journal_id': miscellaneous_operations_id,
            #  'narration':note,
              'move_ids': [(4, move_ids[0])],

        }])
        # reverse_moves method 
        print(reversal_id,"_____________ ")
        reverse = models.execute_kw(db, uid, password, 'account.move.reversal', 'custome_reverse', [[]],{'args':reversal_id})
        if not reverse:
            raise NotFound("not found journal with this ref") 

        return Response({'result':reversal_id , 'message':bool(reversal_id)})


