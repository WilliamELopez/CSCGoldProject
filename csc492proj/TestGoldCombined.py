import pandas as pd
import smtplib
from email.message import EmailMessage
import os
import glob
import shutil

os.chdir("C:\\Users\\KACronin001\\Documents\\Gold Project") #Make this the directory of where the code is
#print("Current Working Directory:", os.getcwd()) #Uncomment to check where it's looking

csvFolder = "EmailSentCSV" #Name this whatever the name of the folder is
os.makedirs(csvFolder,exist_ok=True)

excel_files = glob.glob('*.xlsx') + glob.glob('*.xls')

if not excel_files:
    print("No Excel files found in the current directory.")
else:
    print(f"Found {len(excel_files)} Excel file(s):")

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login("convcsc2025project@gmail.com", "omyu xsxt ryrh uxbp")

    for excel_file in excel_files:
        print(f"Processing: {excel_file}")
        
        base_name = os.path.splitext(excel_file)[0]
        parts = base_name.split('_')
        
        if parts and ',' in parts[-1]:
            prof_last_name = parts[-1].split(',')[0]
        else:
            prof_last_name = 'Unknown'

        print(f"Professor Last Name Detected: {prof_last_name}")

        dfTest = pd.read_excel(excel_file)

        dfTest_csv = dfTest.copy()
        dfTest_csv['Email Sent'] = ''
        
        for i in range(len(dfTest)):
            ID = dfTest.loc[i, 'Jenzabar ID']
            FN = dfTest.loc[i, 'FIRST NAME']
            LN = dfTest.loc[i, 'LAST NAME']
            email = dfTest.loc[i, 'email address']
            if pd.notnull(email):
                message = EmailMessage()
                message['From'] = "convcsc2025project@gmail.com"
                message['To'] = email
                message['Subject'] = "Test Email"
                message.set_content("Hi, this is a test email.")
                #smtp.send_message(message) #Uncomment to actually send the emails.
                dfTest_csv.at[i, 'Email Sent'] = 'Sent'
                print(f"Mail Sent To {email}")

        csv_path = os.path.join(csvFolder, base_name + '.csv')
        dfTest_csv.to_csv(csv_path, index=False)
        print(f"Saved CSV to: {csv_path}")

        #Name this whatever the name of the folder is and put the path to the folder of origin
        excelFolder = os.path.join("C:\\Users\\KACronin001\\Documents\\Gold Project", "EmailSentXLSX")
        os.makedirs(excelFolder, exist_ok=True)

        #Move the excel file from the main folder to the EmailSentXLSX folder
        shutil.move(excel_file, os.path.join(excelFolder, os.path.basename(excel_file)))
        print(f"Moved {excel_file} to {excelFolder}") 

    smtp.quit()
