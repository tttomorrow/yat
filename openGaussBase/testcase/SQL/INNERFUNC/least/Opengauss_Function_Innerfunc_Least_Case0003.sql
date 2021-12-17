-- @testpoint: having的测试
drop table if exists FVT_OBJ_DEFINE_table_least;
CREATE TABLE FVT_OBJ_DEFINE_table_least(COL_1 char(20),COL_2 int);
insert into FVT_OBJ_DEFINE_table_least values('9876',3);
insert into FVT_OBJ_DEFINE_table_least values('111111111111',4);
select sum(COL_2) from FVT_OBJ_DEFINE_table_least having length(least('COL_1','6','0'))< 10;
select sum(COL_2) from FVT_OBJ_DEFINE_table_least having length(least('COL_1','6','0')) > 10;
drop table if exists FVT_OBJ_DEFINE_table_least;