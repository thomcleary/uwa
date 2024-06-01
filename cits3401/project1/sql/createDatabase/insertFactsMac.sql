/* 
 * HOW TO RUN THIS SCRIPT:
 *
 * 1. Enable full-text search on your SQL Server instance. 
 *
 * 2. Open the script inside SQL Server Management Studio and enable SQLCMD mode. 
 *    This option is in the Query menu.
 *
 * 3. Set the following environment variable to your own data path.
 */

 
 :setvar csvFilesPath "C:\cits3401\project1\csvFilesMac\"

 :setvar DatabaseName "CovidDW"

 /*
 * Execute the script to insert the fact table data
 */

 USE CovidDW
 GO

 BULK INSERT [dbo].[FactCovidData] FROM '$(csvFilesPath)FactCovidData.csv'
 WITH (
    CHECK_CONSTRAINTS,
    --CODEPAGE='ACP',
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='0x0a',
    --KEEPIDENTITY,
    TABLOCK
 )