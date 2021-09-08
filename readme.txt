This project is made using Django REST Framework and PlaidAPI

Users App -> API calls for User Register, Login, Logout. Token Authentication has been used.
PlaidBackend -> This app has been used for all the API calls and WebHooks. 

Resources used in making the project :

	- Youtube - JustDjango REST Framework series
			  - Corey Schafer Django series

	- Great help from Github Repositories
	- REST framework and PlaidAPI documentation

ERROR : (HELP REQUIRED) 
	
	- plaid_client module in PlaidBackend is for making Client and 	
	- I came accross an unforseen error 'cannot import 'Client' from 'plaid'

Measures Taken to Solve the error:
	- Searched on Stackoverflow. No Luck. 
	- Searched on Github. Installed plaid-python. No luck.
	- Modified the '__init__.py' file in the 'plaid' package. Imported the function api_client with the name 'Client'.

Current Situation : 
	- Previous error got resolved. 
	- Now it shows invalid parameters but the parameters are default.


Django rest Apis for signup, login and logout

	api/register/ - Create user using username, email and password

	api/login/ - Login using username and password

	api/logout/ - Logout using knox token

Fetch and store data from Plaid Apis
	
	get_public_token/ - Get public token from Plaid

	get_access_token/ - Exchange public token with access token

	get_transactions/ - Get transactions from plaid api

	get_transactions_from_db/ - Fetch transactions saved in db

	get_account_balance/ - Get account details from plaid api

	get_account_balance_from_db/ - Fetch account details saved in db

Webhooks

	webhook_test/ - Fire a test sandbox webhook

	webhook_transactions/ - Transactions Webhook