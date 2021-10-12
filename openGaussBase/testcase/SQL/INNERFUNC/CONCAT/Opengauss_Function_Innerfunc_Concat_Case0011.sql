-- @testpoint:group by,having条件
drop table if exists TEST_LOWER_007;
create table TEST_LOWER_007(col1 varchar2(20),col2 int);
select sum(col2) from TEST_LOWER_007 group by concat(lower(col1),1) having concat(lower(col1),1) in ('ahggfgfaabn','aldjfghjjk');
drop table if exists TEST_LOWER_007;