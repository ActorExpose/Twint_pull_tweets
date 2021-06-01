import twint
import time
import datetime
import os, glob
import pandas as pd

researchers = ["xu_xiuzhong", "DrewPavlou", "adrianzenz", "wang_maya"]
#researchers = ["adrianzenz", "DrewPavlou"]
Uighur_individuals = ["ziba116", "RushanAbbas","arslan_hidayat", "Omerkanat1", "JewherIlham", "MehmetTohti", "RayhanAsat", "AbdurehimGheni", "nyrola", "humarisaac", "ZumretErkin", "Uyghurian", "nuryturkel", "SamiraImin", "IKashgary", "Uyghurspeaker", "akida_p", "Qelbinur10", "Bsintash", "KuzzatAltay", "MamutjanAB", "NurgulSawut", "AbduwelA", "Mehray_T", "TQahiri", "mahire53263554","Save_NajibullaS","mirehmet"]


def prepare_input_data(names, pers):
    data_set = {}
    for name in names:
        data_set[name] = pers
    return data_set


def make_periods(start_date, end_date, size):
    """
    This function divides the duration of time starting at the "start date" until now into slots of size "size". The output is a list of tuples [(slot1_start_date, slot1_end_date), (slot2_start_date, slot2_end_date), ...]
    """
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    delta = end_date - start_date
    periods = []
    period_start = start_date
    if size <= 0 or delta.days <= 0:
        print(f"ERROR: Either the start_date is in the future or the period size is not between 0 and (today minus start_date).")
        return
    else:
        while True:
            if (delta.days) > size:
                period_end = period_start
                period_end += datetime.timedelta(days=size)
                delta = end_date - period_end
                start_end = (period_start, period_end)
                periods.append(start_end)
                period_start = period_end
            else:
                periods.append((period_start, end_date))
                break
        return periods


def get_tweets(input, out_dir, ext):
    """
    This function takes the list of individuals with the periods list and runs twint for each period. It stores the result in a csv file called c.Output and returns the dictionary of uncollected names and periods.
    """
    counter = 0
    uncollected = {}
    l = len(list(input.keys()))
    c = twint.Config()
    c.Store_csv = True
    for name in input:
        c.Search = name
        for p in input[name]:
            start = p[0].strftime("%Y-%m-%d")
            end = p[1].strftime("%Y-%m-%d")
            c.Output = f"{out_dir}{name}_{start}_{end}{ext}"
            c.Since = str(p[0])
            c.Until = str(p[1])
            try:
                twint.run.Search(c)
                counter += 1
                if counter < (l - 1):
                    time.sleep(7)
            except Exception as e:
                print(e)
                if name not in uncollected:
                    uncollected[name] = [p]
                else:
                    uncollected[name].append(p)
                try:
                    os.remove(c.Output)
                except OSError as e:
                    print(f"Error:  {c.Output} --> {e.strerror}")
                continue
    return uncollected


def user_input():
    while True:
        try:
           answer = int(input(f"Would you like to continue to retry the uncollected items? (Please enter 1 for yes or 0 for no.)"))
        except ValueError:
            print(f"Sorry, please enter 1 for Yes or 0 for no!")
            continue
        else:
            if answer < 0 or answer > 1:
                print(f"Sorry, please enter 1 for Yes or 0 for no!")
                continue
            else:
                break
    return answer


def print_uncollected(uncollected):
    print(f"Uncollected items due to possible server disconnection ...")
    for key,value in uncollected.items():
        print(f"{key} -- > {value}")


def combine_output(dir, out_file, ext):
    try:
        all_files = [file for file in glob.glob(f"{dir}*{ext}")]
        print(all_files)
        combined = pd.concat(pd.read_csv(f) for f in all_files)
        combined.to_csv( f"{dir}{out_file}{ext}", index=False, encoding='utf-8-sig')
        print(f"The combined results are in the file --> {dir}{out_file}{file_ext}!")
    except Exception as e:
        print(f"The results could not be combined due to {e}")


if __name__ == "__main__":
    iteration = 0
    name_list = Uighur_individuals
    output_dir = "./Tweets_Uighur_individuals/"
    output_file = "combined_results"
    file_ext = ".csv"
    period_size = 7
    start_date = "2021-01-01 00:00:00"
    #end_date = "2021-04-30 00:00:00"
    end_date = "now"
    if end_date == "now":
        end_date = datetime.datetime.now()
    # make_periods builds the list of time slots starting start_date of size period_size.
    periods = make_periods(start_date, end_date, period_size)
    if periods:
        # for period in periods:
        #     print(period)
        input_data = prepare_input_data(name_list, periods)
        while True:
            iteration += 1
            s = time.time()
            uncollected = get_tweets(input_data, output_dir, file_ext)
            e = time.time()
            print("-"*5 + "####" + "-"*5)
            print(f"Elapsed time for iteration {iteration} to get the tweets: {e-s} seconds!")
            if uncollected:
                print("-"*5 + "####" + "-"*5)
                print_uncollected(uncollected)
                print("Printing Uncollected - Done!")
                ui = user_input()
                if ui == 1:
                    input_data = uncollected
                    continue # itertion with with uncollected list
                else:
                    combine_output(output_dir, output_file, file_ext)
                    break
            else:
                combine_output(output_dir, output_file, file_ext)
                break
