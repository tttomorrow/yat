-- @testpoint: create table时指定关键字NOCOMPRESS则不对表进行压缩

drop table if exists tab_10;
CREATE TABLE tab_10(
ID int,
name VARCHAR(100),
age int
)NOCOMPRESS;

begin
	for i in 1..1000 loop
insert into tab_10 values(i,'zhangsan',16);
    end loop;
end;
/

select * from tab_10;
drop table if exists tab_10;
 
 
