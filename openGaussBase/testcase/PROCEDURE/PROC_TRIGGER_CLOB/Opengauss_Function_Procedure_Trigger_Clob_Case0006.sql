-- @testpoint: 验证存储过程是否支持clob类型删除
--创建测试表
drop table if exists temp;
create table temp
(
  name      varchar2(200),
  age       number,
  temp_clob clob
);

--创建存储过程
create or replace procedure proc_clob_001(str boolean)
is
  v_name temp.name%type;
  v_lang clob := '待插入的海量字符串';
begin
  insert into temp values ('grand.jon', 22, v_lang);
  delete from temp where name='grand.jon';
  raise info '删除的人名：%',v_name;
  end;
  /
 --调用存储过程
call proc_clob_001(true);

--清理环境
drop procedure proc_clob_001;
drop table temp;
