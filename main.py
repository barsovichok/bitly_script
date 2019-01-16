import requests
import os
import argparse

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

shorten_url = "https://api-ssl.bitly.com/v4/shorten"
headers =  {'Authorization': f'Bearer {os.getenv("TOKEN")}'}


def user_input():
  parser = argparse.ArgumentParser(description=
    "Hi! Add link to short or bitlink to get the stats data"
  )
  parser.add_argument('link', help='Добавь ссылку')
  args = parser.parse_args()
  return args.link


def get_bitly_response(user_input):
  click_summary_link = f"https://api-ssl.bitly.com/v4/bitlinks/{user_input}/clicks/summary"
  bitly_response = requests.get(click_summary_link, headers=headers)
  return bitly_response

def check_user_input_result(bitly_response):
  if bitly_response.ok == False:
    data = {"long_url": user_input}
    bitly_info = requests.post(shorten_url, headers=headers, json=data)
    if bitly_info.status_code == 400:
      return None
    else:
      return bitly_info.text
  else:
    return bitly_response.text

def print_result(check_user_input_result):
  if check_user_input_result is None:
    print('You add the wrong link, please restart the script')
  else:
    print(check_user_input_result)

if __name__ == '__main__':
  
  user_input = user_input()
  bitly_response = get_bitly_response(user_input)
  check_user_input_result = check_user_input_result(bitly_response)
  print_result(check_user_input_result)
  


