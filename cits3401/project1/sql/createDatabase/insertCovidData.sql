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

 
 :setvar csvFilesPath "C:\cits3401\project1\csvFilesWindows\"

 :setvar DatabaseName "CovidDW"

 /*
 * Execute the script to insert the dimension table data
 */

 USE CovidDW
 GO

 BULK INSERT [dbo].[DimTime] FROM '$(csvFilesPath)DimTime.csv'
 WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    TABLOCK
);

 BULK INSERT [dbo].[DimLocation] FROM '$(csvFilesPath)DimLocation.csv'
 WITH (
	CHECK_CONSTRAINTS,,
	DATAFILETYPE    = 'char',
	FIELDTERMINATOR = ',',
	ROWTERMINATOR   = '\n',
	TABLOCK
);

 BULK INSERT [dbo].[DimCountrySize] FROM '$(csvFilesPath)DimCountrySize.csv'
 WITH (
	CHECK_CONSTRAINTS,
	DATAFILETYPE    = 'char',
	FIELDTERMINATOR = ',',
	ROWTERMINATOR   = '\n',
	TABLOCK
);

 BULK INSERT [dbo].[DimLifeExpectancy] FROM '$(csvFilesPath)DimLifeExpectancy.csv'
 WITH (
	CHECK_CONSTRAINTS,
	DATAFILETYPE    = 'char',
	FIELDTERMINATOR = ',',
	ROWTERMINATOR   = '\n',
	TABLOCK
);

 BULK INSERT [dbo].[FactCovidData] FROM '$(csvFilesPath)FactCovidData.csv'
 WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    TABLOCK
 )

