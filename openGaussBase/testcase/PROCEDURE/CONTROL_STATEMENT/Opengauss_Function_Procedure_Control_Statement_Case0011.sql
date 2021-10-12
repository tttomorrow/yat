-- @testpoint: 创建存储过程并调用

create or replace procedure p4(v_id in out int) is
begin
  raise notice 'p4 begin';
  v_id:=v_id+1;
  raise notice 'p4 end';
end;
/
create or replace procedure p3(v_id in out int) is
begin
  raise notice 'p3 begin';
  v_id:=v_id+1;
  p4(v_id);
  raise notice 'p3 end';
end;
/
create or replace procedure p2(v_id in out int) is
begin
  raise notice 'p2 begin';
  v_id:=v_id+1;
  p3(v_id);
  raise notice 'p2 end';
end;
/
create or replace procedure pro1(v_id int) is
v_num int:=1;
begin
  raise notice 'pro1 begin';
  p2(v_num);
  raise notice 'v_num=%',v_num;
  raise notice 'pro1 end';
  p3(v_num);
   raise notice 'v_num=%',v_num;
end;
/

begin
	pro1(2);
end;
/

drop procedure pro1;
drop procedure p2;
drop procedure p3;
drop procedure p4;
