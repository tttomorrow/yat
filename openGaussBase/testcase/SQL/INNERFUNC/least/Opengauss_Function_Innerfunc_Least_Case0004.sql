--@testpoint:视图
drop table if exists FVT_OBJ_DEFINE_table_least;
CREATE TABLE FVT_OBJ_DEFINE_table_least(COL_1 char(20),COL_2 int);
drop view if exists v_Stu_Cou_least_ZHQ;
create view v_Stu_Cou_least_ZHQ as SELECT COL_1 FROM FVT_OBJ_DEFINE_table_least where COL_1 in (least(125251.123456,100562),least(125251.123456,100563),least(125251.123456,100569),least(125251.123456,100659));
drop view if exists v_Stu_Cou_least_ZHQ;
drop table if exists FVT_OBJ_DEFINE_table_least;