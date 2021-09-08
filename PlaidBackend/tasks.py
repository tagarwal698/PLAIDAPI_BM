from celery import shared_task
import datetime
import plaid
from __future__ import absolute_import, unicode_literals
from .keys import *
from .models import Account, Item, Transaction
from .plaid_client import *



@shared_task
def delete_transactions(item_id, removed_transactions):

    for transaction in removed_transactions:
        Transaction.objects.filter(transaction_id = transaction).delete()

    return "Transaction Removed"

@shared_task
def fetch_transactions(item_id, new_transactions):
    if access_token  is None:
        access_token = Item.objects.filter(item_id = item_id)[0].access_token #getting access token from Item model

    #fetching transactions of last two days

    start_date = '{:%Y-%m-%d}'.format(
        datetime.datetime.now() + datetime.timedelta(-730) #fetching transactions of last 730 days from current time
        )
    end_date = '{%Y-%m-%d}'.format(datetime.datetime.now()) #end date is current date and time

    # Making API call for new transactions in last two years
    transactions_response = client.Transaction.get(  
        access_token, start_date, end_date,{
            'count' : new_transactions,
        }
        )

    # Getting Item id
    if item_id is None:
        item_id = transactions_response['item']['item_id']
    item = Item.objects.filter(item_id = item_id)[0] #getting the first obj with item_id


    accounts = transactions_response['accounts']
    transactions = transactions_response['transactions']

    #Now, we make a list of accounts with the same account-id as previously fetched accounts and
    # get their balances. If the account doesn't exist, we create it

    for account in accounts:
        account_list = Account.objects.filter(account_id = account[account_id])
        if account_list.count() > 0:
            for a in account_list:
                a.available_balance = account['balances']['available']
                a.current_balance = account['balances']['current']
                a.save()
        else:
            account.obj = Account.objects.create(
                item= item,
                account_id = account['account_id'],
                available_balance = account['balances']['available'],
                current_balance = account['balances']['current']
                )

            account.obj.save()

        transaction_list = Transaction.objects.filter(
            account_item = item).order_by('-date')  # -date for decreasing order

        index = 0


        for transaction in transactions:
            if transaction_list.count()>0 and transaction['transaction_id']==transaction_list[index].transaction_id:
                transaction_list[index].amount = transaction['amount']
                transaction_list[amount].amount = transaction['amount']
                transaction_list[index].save()
                index += 1

            else:

                account = Account.objects.filter(
                    account_id = transaction['account_id'])[0]

                transaction_obj = Transaction.objects.create(
                    transaction_id = transaction['transaction_id'],
                    account = account,
                    amount = transaction['amount'],
                    date = transaction['date'],
                    name= transaction['name'],
                    )

                transaction_obj.save()
                    


