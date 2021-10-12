-- @testpoint: merge into补充
drop table if exists test_limit_009;
create table test_limit_009 ("LIMIT" int,id int);
insert into test_limit_009 values (-999,1);
insert into test_limit_009 values (-10000,2);
insert into test_limit_009 values (-10000,3);
insert into test_limit_009 values (100,3);
insert into test_limit_009 values (100,2);
drop table if exists test_limit_011;
create table test_limit_011 ("LIMIT" int,id int);
insert into test_limit_011 values (-999,9);
insert into test_limit_011 values (1,10);
insert into test_limit_011 values (2,11);
MERGE INTO test_limit_011 t1 USING test_limit_009 t2 ON (t1."LIMIT" = t2."LIMIT")
      WHEN MATCHED THEN UPDATE SET t1.id = t2.id
	  WHEN NOT MATCHED THEN INSERT ("LIMIT",id) VALUES (t2."LIMIT",t2.id);
select id,"LIMIT" from test_limit_011 order by id,"LIMIT";
--清理环境
drop table if exists test_limit_009;
drop table if exists test_limit_011;