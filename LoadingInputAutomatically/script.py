from collections import namedtuple, OrderedDict
import xml.etree.ElementTree as ET
from openpyxl import load_workbook
import json
from email.mime.text import MIMEText
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
import os
import xlrd
import threading
import traceback

class Script:
    @staticmethod
    def run():
            try:
                Script._main()
            except:
                traceback.print_exc()


    FILE_DIR = "./data/"
    TIME = 5.0  # Repeat every TIME seconds

    MY_EMAIL = ""
    PASSWORD = ""

    EMAIL_SUBJECT = "A subject"
    EMAIL_TEXT = """
    This text is going to be placed in your email.
    """

    RECIPIENTS = [
        "stanislav.savchuk@gmail.com"    # Who is going to receive your email
    ]

    _associated = ["csv", "xml", "txt", "xlsx", "xls", "json"]
    _txt_splitter = ";"
    _csv_splitter = ";"

    # Unless you use GMail, you have to change this setting according to your e-mail
    _host = 'smtp.gmail.com'
    _port = 587

    Person = namedtuple("Person", ["name", "uni", "subject", "degree", "grade", "year"])

    @staticmethod
    def load_xml(filename):
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            table = root[4][0]
            people = []
            for row in table:
                try:
                    person = [cell[0].text for cell in row]
                    people.append(Script.Person(*person))
                except:
                    pass
            return people
        except:
            return None

    @staticmethod
    def _load_text(filename, splitter):
        try:
            with open(filename, "r") as f:
                data = f.read()

            people = []
            for line in data.split("\n"):
                try:
                    people.append(Script.Person(*line.split(splitter)))
                except:
                    pass
            return people
        except:
            return None

    @staticmethod
    def _load_xlxs(filename):
        try:
            wb = load_workbook(filename, read_only=True)
            wb = wb.worksheets[0]
            people = []
            for row in wb.rows:
                try:
                    person = [cell.value for cell in row]
                    people.append(Script.Person(*person))
                except:
                    pass
            return people
        except:
            return None

    @staticmethod
    def _load_json(filename):
        try:
            with open(filename, "r") as data_file:
                data = json.load(data_file, object_pairs_hook=OrderedDict)
            people = []

            for item in data:
                try:
                    person = [val[1] for val in item.items()]
                    people.append(Script.Person(*person))
                except:
                    pass
            return people
        except:
            return None

    @staticmethod
    def _load_xls(filename):
        try:
            xl_workbook = xlrd.open_workbook(filename)
            sheet_names = xl_workbook.sheet_names()
            xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])
            people = []
            for idx in xrange(0, xl_sheet.nrows):
                try:
                    person = [item.value for item in xl_sheet.row(idx)]
                    people.append(Script.Person(*person))
                except:
                    pass

            return people
        except:
            return None

    @staticmethod
    def _send_email(filename):
        msg = MIMEMultipart(
            From=Script.MY_EMAIL,
            To=COMMASPACE.join(Script.RECIPIENTS),
            Date=formatdate(localtime=True),
            Subject=Script.EMAIL_SUBJECT
        )
        msg.attach(MIMEText(Script.EMAIL_TEXT))
        msg['Subject'] = Script.EMAIL_SUBJECT

        with open(filename, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(filename),
                Name=basename(filename)
            ))
        mail = smtplib.SMTP(Script._host, Script._port)
        mail.ehlo()
        mail.starttls()
        mail.login(Script.MY_EMAIL, Script.PASSWORD)
        mail.sendmail(Script.MY_EMAIL, Script.RECIPIENTS, msg.as_string())
        mail.close()

    @staticmethod
    def _text_file(data):
        filename = "data.txt"
        with open(filename, "w") as f:
            for item in data:
                f.write("Personal name:    " + item.name + "\n")
                f.write("University name:  " + item.uni + "\n")
                f.write("Subject name:     " + item.subject + "\n")
                f.write("Degree type:      " + item.degree + "\n")
                f.write("Grade:            " + str(item.grade) + "\n")
                f.write("Year:             " + str(item.year) + "\n\n")
        return filename

    @staticmethod
    def _main():
        threading.Timer(Script.TIME, Script._main).start()

        try:
            with open("done_list.txt", "r") as f:
                done_list = f.read().split("\n")[:-1]
        except:
            done_list = []

        old_list = done_list[:]

        founded = False
        for filename in os.listdir(Script.FILE_DIR):
            form = filename.split(".")[-1]
            file_path = Script.FILE_DIR + filename
            if (form in Script._associated) and not (file_path in done_list):
                founded = True
                if form == "txt":
                    data = Script._load_text(file_path, Script._txt_splitter)
                elif form == "csv":
                    data = Script._load_text(file_path, Script._csv_splitter)
                elif form == "xlsx":
                    data = Script._load_xlxs(file_path)
                elif form == "xls":
                    data = Script._load_xls(file_path)
                elif form == "xml":
                    data = Script.load_xml(file_path)
                elif form == "json":
                    data = Script._load_json(file_path)

                if data:
                    tfile = Script._text_file(data)
                    try:
                        Script._send_email(tfile)
                        done_list.append(file_path)
                        print "File " + str(file_path) + " has been processed."
                    except:
                        print "File " + str(file_path) + " hasn't been sent by email."
                        traceback.print_exc()
                else:
                    print "File " + str(file_path) + " empty or corrupted."
                    done_list.append(file_path)

        if not founded:
            print "New files not found."

        if len(old_list) < len(done_list):
            new_list = old_list + done_list
            new_list = list(set(new_list))

            with open("done_list.txt", 'w') as f:
                for item in new_list:
                    f.write(item + "\n")

if __name__ == '__main__':
    Script.run()