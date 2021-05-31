import requests
from datetime import date
from datetime import timedelta

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

def capacity(i):
      for j in i['sessions']:
            return j['available_capacity']

def slotsmdn(pin = int()):
      date_today = date.today() 
      date_tommorrow = date.today() + timedelta(days = 1)
      date_today = date_today.strftime("%d-%m-%Y")
      date_tommorrow = date_tommorrow.strftime("%d-%m-%Y")

      url_1 = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date_today}"
      url_2 = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date_tommorrow}"
      
      response = requests.request("GET", url_1, headers=headers)
      response_2 = requests.request("GET", url_2, headers=headers)

      r = response.json()
      r_2 = response_2.json()

      result = dict()
      for i in r['centers']:
            if(capacity(i)!=0):
                  result[date_today].update({i:capacity(i)})
      if r_2 != None:
            for i in r_2['centers']:
                  if(capacity(i!=0)):
                        result[date_tommorrow].update({i:capacity(i)})
      if result == {}:
            return "No slots"
      else:
            return result



      












