-- @testpoint: 对普通表创建指定索引

drop table if exists using_test_01 cascade;
create table using_test_01(id int,c_int int,c_vchar varchar(100),c_blob text,c_date date);

create index idx_using_test_01 on using_test_01(c_int,c_vchar);
create index idx_using_test_02 on using_test_01(c_int,c_vchar,c_date);
create index idx_using_test_03 on using_test_01 using btree(c_vchar);

insert into using_test_01 values(1,1000,'abc123',lpad('11100011',50,'1100'),to_timestamp(to_char('2020-07-01 10:51:47'),'yyyy-mm-dd hh24:mi:ss'));

create or replace procedure proc_insert(tname varchar,startall int,endall int)
as sqlst varchar(500);
begin
  for i in startall..endall LOOP
		sqlst := 'insert into ' || tname ||' select id+'||i||',c_int+'||i||',c_vchar||'||i||',c_clob||'||i||',c_blob'||',c_date from '||tname|| ' where id=1';
  END LOOP;
END;
/
call proc_insert('using_test_01',1,10);
select * from using_test_01;
drop index idx_using_test_01,idx_using_test_02,idx_using_test_03;
drop table if exists using_test_01 cascade;
drop procedure proc_insert;