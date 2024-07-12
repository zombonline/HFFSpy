
██╗░░██╗███████╗███████╗░██████╗██████╗░██╗░░░██╗  ██╗░░░██╗░░███╗░░░░░░█████╗░░░░░█████╗░
██║░░██║██╔════╝██╔════╝██╔════╝██╔══██╗╚██╗░██╔╝  ██║░░░██║░████║░░░░░██╔══██╗░░░██╔══██╗
███████║█████╗░░█████╗░░╚█████╗░██████╔╝░╚████╔╝░  ╚██╗░██╔╝██╔██║░░░░░██║░░██║░░░██║░░██║
██╔══██║██╔══╝░░██╔══╝░░░╚═══██╗██╔═══╝░░░╚██╔╝░░  ░╚████╔╝░╚═╝██║░░░░░██║░░██║░░░██║░░██║
██║░░██║██║░░░░░██║░░░░░██████╔╝██║░░░░░░░░██║░░░  ░░╚██╔╝░░███████╗██╗╚█████╔╝██╗╚█████╔╝
╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░╚═════╝░╚═╝░░░░░░░░╚═╝░░░  ░░░╚═╝░░░╚══════╝╚═╝░╚════╝░╚═╝░╚════╝░

HFFSpy is a tool to quickly scan the Steam workshop for user generated content (UGC) for Human Fall
Flat. Get up to date data on levels and models added to the workshop and pair with a steam login 
with the right permissions for even more data quickly sorted into an excel sheet.

-----------------------------------------------SETUP-----------------------------------------------


. Extract the installer 'HFFSpy Insaller.exe'
. Run the installer and run through setup, nothing important, just select where you would like 
shortcuts to be made.
. Once installed, run HFFSpy.exe, you may need to run as administrator the first time to allow the
program to setup some files.
. You will be prompted to install Chromdriver, click the link provided in the HFFSpy program.
. Select the version of Chromedriver that matches your current Google Chrome install.
. Once downloaded, place this in the HFFSpy program folder, usually 'C:\Program Files (x86)\HFFSpy'
. Close and reopen HFFSpy, if succesful you should no longer see the Chromedriver screen.
. You may be prompted for a steam api key. You can generate on here provided your steam account
meets the requirements. https://steamcommunity.com/dev/apikey
. Simply enter the api key where prompted and continue. If the key is valid you will be taken 
to the program menu.

----------------------------------------------CREATORS---------------------------------------------

You can add known creators to the app so that when generating excel sheets any recognized creators
will be hilighted. simply navigate to the creators page from the menu and add their steam use ID to
one of three lists, signed creators, contacted creators, notable creators (planning to contact).
When a user from one of these lists is included in an excel sheet, they're name will be hilighted a
particular colour.

--------------------------------------------STEAM LOGIN--------------------------------------------

Logging in to a steam account with the correct permissions is required to access particular data
like ratsings, visitors count etc. It will mean that scans include workshop items hidden from 
public view. Simply navigate to the 'Steam Login' page and enter the user name and password, it may
take a moment for the program to load up steam and enter the details and return the log in result
so sit tight. If log in is succesful, you'll see your username at the top bar of the program. If an
email verification code is required, a new text box will appear and wait for your input. If you 
need to verify by the steam app on your phone a message will appear and a buton saying 'I'm done'.
Verify the login on your phone and then hit the 'I'm done' button.

-----------------------------------------HFF WORKSHOP SCAN-----------------------------------------

The HFF Workshop scan page allows you to create excel sheets with data on levels and models created
for Human Fall Flat. You can set a date range, the amount of items within that range, how to sort 
and also decide if you want to sort levels and models separately. Then choose the data you want 
included on the sheet and hit 'Scan'. 

Example 1:
Date range is from 2024-01-10 to 2024-01-17. Amount of items is left blank. Sort by is set to
'Most Recent' and 'seperate levels and models' is unchecked.
Every single item made between the 10th Jan 2024 (Inclusive) and the 17th Jan 2024 (Inclusive) are
scanned. All of them are inserted into an excel sheet ordered by the most recent and both levels 
and models are in the same tab.

Example 2:
Date range is from 2024-01-31 to 2024-01-31. Amount of items is set to 20. Sort by is set to 
'Most Popular' and 'seperate levels and models is checked.
The top 20 most popular levels and the top 20 most popular models during the month of January 2024
are scanned. They are inserted into an excel sheet into two separate tabs, one for levels and one
for models. If that month, only 4 levels were made, then only 4 levels are put into the levels tab.

Some data you may want to include in excel is grabbed without the use of the steam api and is 
grabbed through webscraping, these are marked as 'intensive' as they can add around a second for 
each item on to the time of your scan so only include these if absolutely necessary. 

There are two preset shortcuts at the top labelled 'Weekly Scan' and 'Monthly Scan' which do what
they say on the tin. Weekly scan will change the options to a weekly total content scan with the 
date range set to the last FULL week. Monthly scan changes the options to a top 20 levels and 
models scan with the date range set to the last full month.

--------------------------------------------STEAM TOP 100--------------------------------------------

This scan will pop over to steamDB and grab the top 100 currently most popular steam games that 
have wokshop content. It will then scan each one for it's total amount of UGC overall and generate
an excel sheet with the information. 




Any issues?

Find my details on my github profile. https://github.com/zombonline