import requests
from bs4 import BeautifulSoup as bs
import random

session = requests.session() 


def get_sizes_in_stock():
	global session

	endpoint = "https://www.jimmyjazz.com/girls/footwear/jordan-1-mid-shoe/640735-700"
	response = session.get(endpoint)

	soup = bs(response.text, 'html.parser')

	div = soup.find("div", {"class":"box_wrapper"})
	all_sizes = div.find_all("a")

	sizes_in_stock = []
	for size in all_sizes :
		if "piunavailable" not in size["class"]:
			size_id = size["id"]
			sizes_in_stock.append(size_id.split("_")[1])

	return sizes_in_stock

print(get_sizes_in_stock())


def add_to_cart():
	global session
	sizes_in_stock = get_sizes_in_stock()
	size_chosen = random.choice(sizes_in_stock)

	endpoint = "https://www.jimmyjazz.com/cart-request/cart/add/%s/1"%(size_chosen)
	
	response = session.get(endpoint)
	print(response.text)

	return '"success":1' in response.text

print(add_to_cart())


def check_out():
	global session
	endpoint0 = "https://www.jimmyjazz.com/cart/checkout"

	response0 = session.get(endpoint0)

	soup = bs(response0.text, "html.parser")
	input = soup.find_all("input", {"name":"form_build_id"})
	print(input)
	form_build_id = input[1]["value"]
	# print(form_build_id)

	endpoint1 = "https://www.jimmyjazz.com/cart/checkout"

	payload1 = {
		"billing_email":"email@gmail.com",
		"billing_email_confirmation":"email@gmail.com",
		"billing_phone":"1234567890",
		"email_opt_in":"1",
		"shipping_first_name":"KKK",
		"shipping_last_name":"KHK",
		"shipping_address1":" 123 streat st.",
		"shipping_address2":"",
		"shipping_city":" LA",
		"shipping_state":" CA ",
		"shipping_zip":"94111",
		"shipping_method":"0",
		"signature_required":"1",
		"billing_same_as_shipping":"1",
		"billing_first_name":"",
		"billing_last_name":"",
		"billing_country":"US",
		"billing_address1":" ",
		"billing_address2":"",
		"billing_city":" ",
		"billing_state":" ",
		"billing_zip":"",
		"cc_type":"Visa",
		"cc_number":"1234 1234 1234 1234",
		"cc_exp_month":"07",
		"cc_exp_year":"25",
		"cc_cvv":"123",
		"gc_num":"",
		"form_build_id":form_build_id,
		"form_id":"cart_checkout_form"
		}

	response1 = session.post(endpoint1, data=payload1)
	
	soup = bs(response1.text, "html.parser")
	input = soup.findAll("input", {"name":"form_build_id"})
	form_build_id = input[1]["value"]

	endpoint2 = "https://www.jimmyjazz.com/cart/confirm"
	payload2 = {
		"form_build_id":form_build_id,
		"form_id":"cart_confirm_form"
	}
	response = session.post(endpoint2, data=payload2)

check_out()