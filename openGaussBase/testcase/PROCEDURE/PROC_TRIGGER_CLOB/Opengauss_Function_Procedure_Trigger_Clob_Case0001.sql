-- @testpoint: 验证匿名块是否支持插入clob类型

--创建测试表
drop table if exists temp;
create table temp
(
  name      varchar2(200),
  age       number,
  temp_clob clob
);

--创建匿名块
declare
       v_lang clob := '待插入的海量字符串';
begin
  insert into temp values ('grand.jon', 22, v_lang);
end;
/
--查看表数据
select * from temp;

--清理环境
drop table temp;