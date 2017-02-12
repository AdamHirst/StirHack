use Test;

select person_id, count(person_id) as 'freq' from personoccurrence
    where store_id = 1
      and occurance_timestamp >= '2010-01-31 12:01:01' and occurance_timestamp <= '2010-01-31 12:01:01'
	group by person_id
