-- @testpoint: 函数regr_avgx(Y, X),自变量的平均值 (sum(X)/N)

drop table if exists table_test;
create table table_test(id integer,
name varchar(10),
age integer,
height decimal(5,2),
hobbies text,
tel bigint
);
select regr_avgx(tel, height)from  table_test where id <5;
select regr_avgx(height, id)from  table_test where id <5;
select regr_avgx(age, id)from  table_test where id <9;
drop table table_test;