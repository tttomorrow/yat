-- @testpoint: 数字操作符||/(立方根),非数值类型进行开立方，合理报错
drop table if exists data_01;
create table data_01 (clo1 int,clo2 char);
insert into data_01 values (255, 'A');
select ||/ clo2 from data_01;
SELECT ||/ 'a' AS RESULT;
drop table if exists data_01;