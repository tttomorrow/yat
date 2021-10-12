-- @testpoint: 修改模式后检查数据
set enable_bitmapscan to off;
set enable_seqscan to off;
--1.create schema
create schema schema_test_006;
--2.create table
create table schema_test_006.i_table(i int,x char(10));
--3.insert data
insert into schema_test_006.i_table values(generate_series(1,20000),'你tes');
--4.create index
create index schema_test_006.i_idx on schema_test_006.i_table(i);
create index x_idx on schema_test_006.i_table(x);
--5.create view
create view my_view as select i from schema_test_006.i_table;
--6.create materialized
CREATE MATERIALIZED VIEW schema_test_006.i_all AS SELECT * FROM schema_test_006.i_table;
--query data
select count(*) from schema_test_006.i_table where x='你tes';
explain select * from schema_test_006.i_table where i<12580;
explain select * from schema_test_006.i_table where x='hula';
select count(*) from my_view;
select count(*) from schema_test_006.i_all;
--7.create function
CREATE FUNCTION schema_test_006.func_add_sql(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/
select schema_test_006.func_add_sql(1,3);
--8.create user
create user user_case006 with password 'test@12345';
--9.alter schema
alter schema schema_test_006 rename to schema_test_006_new;
alter schema schema_test_006_new owner to user_case006;
--10.check data
select count(*) from schema_test_006_new.i_table where x='你tes';
explain select * from schema_test_006_new.i_table where i<12580;
explain select * from schema_test_006_new.i_table where x='hula';
select count(*) from my_view;
select count(*) from schema_test_006_new.i_all;
select schema_test_006_new.func_add_sql(1,3);

--tearDown
drop view if exists my_view;
drop MATERIALIZED VIEW if exists schema_test_006_new.i_all;
drop table if exists schema_test_006_new.i_table;
drop schema if exists schema_test_006 cascade;
drop schema if exists schema_test_006_new cascade;
drop user if exists user_case006 cascade;