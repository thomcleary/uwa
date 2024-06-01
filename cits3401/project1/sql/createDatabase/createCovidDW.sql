USE master
GO

PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'CovidDW')
DROP DATABASE CovidDW
GO

PRINT '';
PRINT '*** Creating Database';
GO

CREATE DATABASE CovidDW
GO

USE CovidDW
Go

PRINT '';
PRINT '*** Creating Table DimDate';
GO

CREATE TABLE DimTime
(
	TimeID	INT		PRIMARY KEY,
	Month	INT		NOT NULL,
	Quarter	INT		NOT NULL,
	Year	INT		NOT NULL
)
GO

PRINT '';
PRINT '*** Creating Table DimLocation';
GO

CREATE TABLE DimLocation
(
	LocationID	INT			PRIMARY KEY,
	Country		VARCHAR(255)	NOT NULL,
	Region		VARCHAR(255)	NOT NULL
)
GO

PRINT '';
PRINT '*** Creating Table DimCountrySize';
GO

CREATE TABLE DimCountrySize
(
	CountrySizeID	INT			PRIMARY KEY,
	CountrySizeType	VARCHAR(255)	NOT NULL
)
GO

PRINT '';
PRINT '*** Creating Table DimLifeExpectancy';
GO

CREATE TABLE DimLifeExpectancy
(
	LifeExpectancyID		INT				PRIMARY KEY,
	LifeExpGreaterThan75	VARCHAR(255)	NOT NULL
)
GO

PRINT '';
PRINT '*** Creating Table FactCovidData';

CREATE TABLE FactCovidData
(
	CovidDataID			BIGINT	PRIMARY KEY		IDENTITY,
	TimeID				INT		NOT NULL,
	LocationID			INT		NOT NULL,
	CountrySizeID		INT		NOT NULL,
	LifeExpectancyID	INT		NOT NULL,

	ConfirmedCases		INT,
	Deaths				INT,
	Recoveries			INT
)
GO

PRINT '';
PRINT '*** Adding relations between Fact Table foregin keys to primary keys of Dimension Tables';
GO

ALTER TABLE FactCovidData ADD CONSTRAINT
FK_TimeID FOREIGN KEY (TimeID) REFERENCES DimTime(TimeID);

ALTER TABLE FactCovidData ADD CONSTRAINT
FK_LocationID FOREIGN KEY (LocationID) REFERENCES DimLocation(LocationID);

ALTER TABLE FactCovidData ADD CONSTRAINT
FK_CountrySizeID FOREIGN KEY (CountrySizeID) REFERENCES DimCountrySize(CountrySizeID);

ALTER TABLE FactCovidData ADD CONSTRAINT
FK_LifeExpectancyID FOREIGN KEY (LifeExpectancyID) REFERENCES DimLifeExpectancy(LifeExpectancyID);


