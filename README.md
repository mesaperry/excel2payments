# excel2payments
## Motivation
Built in response to Checkbook's challenge:  
Create a tool that takes data from an Excel spreadsheet and automatically sends out payments using the Checkbook API.

## Procedure
1. Open `config.txt` and configure settings under `general`.
Set `type` to the type of payment your Excel sheet contains, either digital, physical, or multi.
Point `path` to your sheet.
2. Go to the section of your payment type, and point each field to its respective column on your sheet.
If a field isn't used on your sheet, you can leave it blank.
3. (Recommended) If you wish to return results for which checks were successfully sent, set `successful` to a column, and the script will write the results to that column.
4. Run `python main.py`
5. Paste in your API key and secret key when prompted.

If you need to target a specific range of rows, decrease batch size to lower memory intensity, or go into production mode, all of these can be changed in `general` settings.

## Examples
I included four example Excel sheets to demonstrate the flexibility.
With the default settings, the digital payment sample sheet is selected.
Running the script should successfully send three checks.

If you change `type = physical` and `path = samplephysical.xlsx`, the script now targets a physical payment sample sheet.
Running the script should send three checks.
Notice how the remittance record columns are indicated in the config.

If you change `type = multi` and `path = samplemulti.xlsx`, you'll get a similar effect for multi payments.

The last sample sheet I included to demonstrate how the check sending is checked and logged.
Change `type = digital` and `path = samplefail.xlsx` and set `successful = E` under `digital`.
The results of whether the check sending was successful or not will be logged in column E.
Running it reveals the first check successful, but then the second check not due to an invalid email, and the third not due to a blank `amount` cell.

