-- @testpoint:make_set在存储过程中的测试,部分用例合理报错
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;

-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,false,null) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();

-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(0,'a','b') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(31,'a','b','c','d','e','f') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(1,'a','b') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(1,null,'b') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(2,'a',null) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3|1,'a','b','c','d') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(12+1,'a','b') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(null,null,'b') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(a,'a','b','c',null) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(110,'a','b','c',null) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(,'a','b','c','d') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set('','a','b','c','d') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(null,'null','2022-09-03') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(null,true) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,3,2022-09-03) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,false,true) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,false,好) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,￥￥,true) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3,false,null) into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop procedure if exists pro_Opengauss_MAKE_SET_Case0020_1;
-- 存储过程的创建与调用
create procedure pro_Opengauss_MAKE_SET_Case0020_1(
a1 out text
)
is
begin
select make_set(3|1,'a','b','c','d') into a1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 清理环境;expect: 清理环境成功
drop table if exists t_Opengauss_MAKE_SET_Case0020_1;
-- 创建表 expect:创建成功
create table t_Opengauss_MAKE_SET_Case0020_1(a int,b char(10));
-- 给表添加数据
insert into t_Opengauss_MAKE_SET_Case0020_1 values(1,'to'),(2,'xi'),(3,'dao'),(3,'to'),(4,'ruai'),(5,'mi'),(6,'fa'),(7,'xi'),(8,'xi'),(9,'la'),(10,'to'),(11,'no'),(11,'no'),(12,'buy'),(13,'buy'),(14,'buy'),(15,'bear'),(16,'bear');
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
  select make_set(3,1+6,6,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
  c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
 end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
  select make_set(3,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
  c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
 end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
  select make_set(3,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
  c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
 end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
 select make_set(l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix'; 
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(r,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(00l,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(011,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set('',false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set('',1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set('',1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(,false,1,'hello','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(,1+6,true,'hello') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(,1|6,'a','hello','hello','hello') from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(,'hello','world') from t_Opengauss_MAKE_SET_Case0020_1 where b='xi';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,a1,b1) from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,sr,c) from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,fa,dao) from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,) from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,) from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,) from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
 c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,a,b) from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
c text[];
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,a,a) from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,b,b) from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,a,b) from t_Opengauss_MAKE_SET_Case0020_1 where a=1;
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'a','b') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'a','a') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'b','b') from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'','') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'','') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'','b') from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'c','d') from t_Opengauss_MAKE_SET_Case0020_1 where b='xix';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'e','null') from t_Opengauss_MAKE_SET_Case0020_1 where b sounds like('t');
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();
-- 存储过程的创建与调用
create or replace procedure pro_Opengauss_MAKE_SET_Case0020_1(
out e text[]
)
is
declare done boolean default 0;
declare cursor cursor_Opengauss_MAKE_SET_Case0020_1 for
select make_set(3,'too','null') from t_Opengauss_MAKE_SET_Case0020_1 where b='to';
c text[];  
begin
 open cursor_Opengauss_MAKE_SET_Case0020_1;
 for i in 0..20 loop
 fetch cursor_Opengauss_MAKE_SET_Case0020_1 into c[i];
exit when cursor_Opengauss_MAKE_SET_Case0020_1%notfound;
  end loop;
 e := c;
close cursor_Opengauss_MAKE_SET_Case0020_1;
end;
/
select pro_Opengauss_MAKE_SET_Case0020_1();

