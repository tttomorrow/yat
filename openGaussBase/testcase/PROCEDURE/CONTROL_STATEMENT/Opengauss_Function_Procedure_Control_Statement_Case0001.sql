-- @testpoint: 创建存储过程并测试execute immediate

drop table if exists  user_tables;
create table user_tables(
table_id int,
table_name varchar2(10));

insert into user_tables values(1,'t_cust');
insert into user_tables values(1,'t_user');

drop procedure if exists pro001;
create or replace procedure pro001(v_month int) is
  v_id int;
begin
  execute immediate 'select count(1) from user_tables where table_name=''t_cust'' '
    into v_id;
	raise notice '%',v_id;
  execute immediate 'select count(1) from user_tables where table_name=''t_cust'''
    into v_id;
	raise notice '%',v_id;
  declare
    v_num int;
  begin
    execute immediate 'select count(1) from user_tables where table_name in(''t_cust'',''t_user'') ' into v_num;
    raise notice '%',v_num;
  end;
end;
/

begin
   pro001(2);
end;
/

drop procedure pro001;
drop table user_tables;
