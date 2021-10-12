-- @testpoint: right函数有效值测试
drop table if exists right_table1;
create table right_table1(col_right1 varchar2(30), col_right2 varchar2(30));
insert into right_table1 values(right('@#$$%%@#',1),right('woheni',4));
select * from right_table1;
select right(col_right2,2) from right_table1; 
drop table right_table1;