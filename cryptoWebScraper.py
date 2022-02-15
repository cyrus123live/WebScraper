import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np

def main():

    # This is necessary so that the website doesn't know we are a bot and kick us out
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    name = ""

    # Inifinite loop for error-checking user
    while (True):
        try:
            # Get the name of the crypto and then find the website
            name = input("Please enter crypto: ").lower()
            URL = "https://ca.investing.com/crypto/" + name + "/historical-data"
            r = requests.get(URL, headers=headers)

            name = name[0].upper() + name[1:]

            # Parse the information using beautiful soup and then get all HTML <tr> tags
            # (except the first one which is formatting stuff) within a <table> with class "genTbl closedTbl historicalTbl"
            soup = BeautifulSoup(r.content, 'html.parser')
            info = soup.findAll("table", {"class": "genTbl closedTbl historicalTbl"})[0].findAll("tr")[1:]
            break
        except:
            print("Invalid crypto!")
            continue

    prices = []
    dates = []
    nums = []

    counter = 0

    # Loop through every <tr>
    for tr in info:
        # <td> contains the data within the <tr>, the first is date and second is price
        date = tr.findAll("td")[0]
        price = tr.findAll("td")[1]

        dates.append(date.text.split(",")[0])

        # This records total number of data-points for the x-axis of our graph
        nums.append(counter)
        counter += 1

        # Python int() method doesn't like commas, so get rid of them
        if("," in price.text):
            price = (price.text.split(",")[0] + price.text.split(",")[1])
        else:
            price = price.text

        # Python int() method also doesn't like periods, so we gotta get rid of those too, maintaining the decimal precision
        price = int(price.split(".")[0]) + (1/(10**len(price.split(".")[1])))*int(price.split(".")[1])
        prices.append(price)
        print(date.text + "    //    " + str(price))

    # Data comes out of the website in reverse
    prices.reverse()

    plt.ylabel(f"$CAD")
    plt.xlabel(f"Days In Last Month")

    # plt.xticks(nums, dates) # This is for labelling x-axis with dates
    plt.plot(nums, prices)
    plt.title("Price of " + name)

    plt.show()

if __name__ == "__main__":
    main()
