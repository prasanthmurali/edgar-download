
select distinct(year, quarter) from filings;

select * from filings where type='10-K' and year='2016' and quarter='QTR3' limit 10;
