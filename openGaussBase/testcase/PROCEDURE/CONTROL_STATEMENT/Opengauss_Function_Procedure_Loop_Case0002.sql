-- @testpoint: 简单loop语句

drop table if exists table_loop_001;
create table table_loop_001(
id int,
name varchar(20)
);

create or replace procedure proc_loop_001()
as
begin
     for i in 1 .. 9 loop
        insert into table_loop_001 values(i,'haha'||i);
  end loop;
end;
/

call proc_loop_001();
drop procedure proc_loop_001;
drop table table_loop_001;
