-- @describe:存储过程中数组函数的使用 array_ndims

--创建存储过程
CREATE OR REPLACE procedure pro_record_014() AS
begin
create table test_array_014(
items text,
id int
);
insert into test_array_014(SELECT array_ndims(ARRAY[[1,2,3], [4,5,6]]) AS RESULT,5);
end;
/

--调用存储过程
call pro_record_014();

--查看表数据
select * from test_array_014;

--删除表
drop table test_array_014;

--删除存储过程
drop procedure pro_record_014;
