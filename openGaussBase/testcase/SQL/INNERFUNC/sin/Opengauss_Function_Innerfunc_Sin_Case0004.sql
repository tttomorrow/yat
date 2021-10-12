-- @testpoint: sin函数中参数为0及函数嵌套

drop table if exists TEST_SIN_02;
create table TEST_SIN_02(id int,COL_SIN double precision);
insert into TEST_SIN_02 values(1,sin(sin(1.23)));
insert into TEST_SIN_02 values(2,1.23);
update TEST_SIN_02 set COL_SIN = SIN(0) where id = 2;

select COL_SIN as result from TEST_SIN_02;

drop table TEST_SIN_02;