# sales_report
Processes your sales for you in csv format. Just give it The monthly csv files with your sales and it calculates the revenue.
Creates a text file with the Revenue per month and the top products. Also creates a csv if you need it for other reports.

Example:
<img width="200" height="237" alt="image" src="https://github.com/user-attachments/assets/bc17e69f-b6d7-49ff-b736-22f3ccb13971" />


# Error Handling
if you have a bad file or in a file you have some nonsense you get to see where the problem is and it still calculates the rest of the file/s

Bad row in csv file: 

product,price,quantity
Pen,3,2
Book,4,10
Apple,1.5,50
Banana,2,5
kiwi,abc,15

The error you get:
Skipped rows: 1
  mar.csv, row 6
  
## How to run
1. download the .py
2. in terminal put: py sales_report.py --data-dir "here path to your folder with your .csv" --output "name your file.txt"
   My example: py sales_report.py --data-dir sample_data --output my_report.txt
3. Wait until its done

# Input format
It only works if your csv has "product,price,quantity" as header (without the "")
