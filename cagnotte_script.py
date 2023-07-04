import json
import time
import calendar
import requests
import statistics
import multiprocessing as mp

def display_stats(donations):
    amounts = [donation["amount"] for donation in donations]
    std_deviation = statistics.stdev(amounts)
    mean = statistics.mean(amounts)
    median = statistics.median(amounts)
    print("--------------------------")
    print("Length :", len(donations))
    print("Mean :", mean)
    print("Median :", median)
    print("Standart Deviation :", std_deviation)

    t = time.localtime()
    current_time = time.strftime("Current time: %H:%M:%S", t)
    print(current_time)
    time.sleep(5)

def get_all_donations(limit, offset, offset_limit, filename = ""):

    def log():
        print("all_donations: ", all_donations)
        print("new_donations: ", new_donations)
        print("donation: ", donation)
        time.sleep(10.0)

    url = "https://gateway.gofundme.com/web-gateway/v2/feed/z86fy-soutien-pour-la-famille-du-policier-de-nanterre/donations"

    if filename == "":
        print("No filename specified")
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        filename = '../dataset_dons_limit{0}_offset{1}_offset_limit{2}_{3}.json'.format(limit, offset, offset_limit, ts)
        all_donations = []
    
    else:
        print("Loading Dataset...")
        all_donations = open(filename)
        all_donations = json.load(all_donations)
        print("DATASET LOADED !")

    while True:
        print(limit, offset)

        params = {
            "limit": limit,
            "offset": offset
        }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            new_donations = []
            donations = data["references"]["donations"]

            for donation in donations:
                if len(all_donations) == 0 and len(new_donations) == 0:
                    print("ALTERNATIVE GARBAGE")
                    new_donations.append(donation)

                elif donation not in all_donations and donation not in new_donations:
                    print("Adding !")
                    new_donations.append(donation)

            all_donations.extend(new_donations)

        except Exception as e:
            print("Error: ", e)
            print("Debug - limit:{0} offset_limit:{1}".format(limit, offset_limit))
            break

        if offset == offset_limit-1:
            break

        offset += 1


    with open(filename, 'w') as fp:
        json.dump(all_donations, fp)
        print("File Saved !")

    return filename, all_donations

def donations_update(filename, data):
    pass



if __name__ == "__main__":

    """
    # Create separate processes for running the functions
    donations1 = mp.Process(target=get_all_donations, args=(100, 0, 1)) # limit, offset, offset_limit
    donations2 = mp.Process(target=get_all_donations, args=(50, 0, 1))  # limit, offset, offset_limit

    # Start the processes
    donations1.start()
    donations2.start()

    # Join the processes
    donations1.join()
    donations2.join()
    """
    
    LIMIT = 100
    OFFSET = 0
    OFFSET_LIMIT = -1 # Set to -1 for infinite browsing
    #FILENAME = ""
    FILENAME = "../dataset_dons_limit100_offset0_offset_limit-1_1688415830.json"

    while True:
        FILENAME, ALL_DONATIONS = get_all_donations(LIMIT, OFFSET, OFFSET_LIMIT, filename=FILENAME)
        display_stats(ALL_DONATIONS)