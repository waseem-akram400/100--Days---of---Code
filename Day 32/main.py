import pandas
import datetime as dt
import random
import os

# آج کی تاریخ نکالنا
today = dt.datetime.now()
today_tuple = (today.month, today.day)

# فائل کا صحیح راستہ
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "birthdays.csv")

print(f"آج کی تاریخ: {today_tuple} - چیک کر رہے ہیں...")

try:
    data = pandas.read_csv(csv_path)
    birthdays_dict = {(row["month"], row["day"]): row for (index, row) in data.iterrows()}

    if today_tuple in birthdays_dict:
        person = birthdays_dict[today_tuple]
        print(f"آج {person['name']} کی سالگرہ ہے!")

        # لیٹر کا راستہ
        letter_num = random.randint(1, 3)
        letter_path = os.path.join(BASE_DIR, "letter_templates", f"letter_{letter_num}.txt")

        with open(letter_path, "r") as f:
            letter = f.read()
            letter = letter.replace("[NAME]", person["name"])

        print("\n--- آپ کا لیٹر تیار ہے ---\n")
        print(letter)
        print("\n---------------------------\n")

        # اگر آپ ای میل بھیجنا چاہتے ہیں تو نیچے والے حصے سے # ہٹا دیں
        # اور اپنا App Password لگائیں

        # import smtplib
        # MY_EMAIL = "aapki_gmail@gmail.com"
        # MY_PASSWORD = "aapka_16_wala_app_password"
        # with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        #     connection.starttls()
        #     connection.login(MY_EMAIL, MY_PASSWORD)
        #     connection.sendmail(
        #         from_addr=MY_EMAIL,
        #         to_addrs=person["email"],
        #         msg=f"Subject:Happy Birthday!\n\n{letter}"
        #     )
        # print("ای میل بھیج دی گئی!")

    else:
        print("آج کسی کی سالگرہ نہیں ہے۔ ٹیسٹ کرنے کے لیے birthdays.csv میں آج کی تاریخ ڈال دیں۔")
        print(f"مثال کے طور پر: Ali,test@gmail.com,2000,{today.month},{today.day}")

except FileNotFoundError as e:
    print(f"فائل نہیں ملی: {e}")
    print("چیک کریں کہ birthdays.csv اور letter_templates فولڈر Day 32 کے اندر ہیں۔")
