-- @testpoint: 释放游标
drop table if exists  test;
create table test(id integer,name varchar(30),gg char(20),scores integer);
INSERT INTO test VALUES (1, 'A','reason1',75),(2, 'B','reason2',87),(3,'C','reason3',95);
START TRANSACTION;
CURSOR nc BINARY WITHOUT HOLD FOR select * FROM TEST;
close nc;
end;
drop table if exists  test;