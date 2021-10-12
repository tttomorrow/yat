-- @describe:存储过程中定义数组类型

--创建存储过程
CREATE OR REPLACE procedure pro_record_010() AS
BEGIN	
create table t_books_001(
	id serial primary key,
	items integer[]
);
insert into t_books_001(items) values('{1,2}');
insert into t_books_001(items) values('{3,4,5}');
END;
/
--查看表结构，合理报错
select * from t_books_001;

--调用存储过程
call pro_record_010();

--再次查看表结构
select * from t_books_001;

--删除表
drop table t_books_001;

--删除存储过程
drop procedure  pro_record_010;

