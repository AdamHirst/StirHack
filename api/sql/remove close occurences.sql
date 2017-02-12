use Test;

delete from personoccurrence where id in  (
select A.id as id FROM (select * from personoccurrence) as A, (select * from personoccurrence) as B
	where A.id <> B.id
      and A.id > b.id
	  and A.person_id = B.person_id
	  and abs(unix_timestamp(A.occurance_timestamp)- unix_timestamp(B.occurance_timestamp)) < 10)