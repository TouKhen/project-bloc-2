import getopt, sys
from data.data import DataManager
from utils.aws import AWSManager

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hmo:"

# Long options
long_options = ["Help",
                "My_file",
                "Output=",
                "FS_page_data",
                "FS_api_data"]

# Objects
s3 = ""
dataManager = ""

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--Help"):
            print("Displaying Help")

        elif currentArgument in ("-m", "--My_file"):
            print("Displaying file_name:", sys.argv[0])

        elif currentArgument in ("-o", "--Output"):
            print("Enabling special output mode (% s)" % currentValue)

        elif currentArgument in ("-f", "--FS_page_data"):
            print(f"Starting fetch and save command of scrapping data :")
            dataManager = DataManager()
            # Scrapping data
            dataManager.fetch_site_data()
            dataManager.save_data_to_csv(path="data/raw/scrapping_data.csv")

        elif currentArgument in ("-s", "--FS_api_data"):
            print(f"Starting fetch and save command of API data :")
            dataManager = DataManager(data_type="API")
            # API data
            dataManager.fetch_api_data()


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
