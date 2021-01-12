import rfid
import merger

def main():
    serialinput = rfid.Parser()
    serialinput.run()
    ci_file_path = input("Enter the file path to the CI File: ")
    rfid_file_path = input("Enter file path to the RFID File: ")
    mg = merger.Merger(ci_file_path, rfid_file_path)
    mg.merge()
    print("Thank you!")