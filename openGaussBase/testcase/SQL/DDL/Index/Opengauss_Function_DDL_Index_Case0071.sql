--  @testpoint: --对某一列建索引，重复列名:合理报错

--普通表
--行存表 btree索引
drop table if exists test_index_071;
create table test_index_071(id int);
drop index if exists index_01;
create index index_01 on test_index_071(id,id,id) local;

--行存表 btree索引
drop index if exists index_01;
create index index_01 on test_index_071(id,id,id) ;

--行存表 gist索引
drop index if exists index_01;
create index index_01 on test_index_071 using gist(id,id,id);

--列存表 btree索引
drop table if exists test_index_071;
create table test_index_071(id int) with (orientation=column);
drop index if exists index_01;
create index index_01 on test_index_071 using btree(id,id,id);

--列存表 psort索引
drop index if exists index_01;
create index index_01 on test_index_071 using psort(id,id,id);

--行存表 gist索引
drop index if exists index_01;
create index index_01 on test_index_071 using gist(id,id,id);

---------------------------------------
--临时表
--行存表 btree索引
drop table if exists test_index_071;
create temporary table test_index_071(id int);
drop index if exists index_01;
create index index_01 on test_index_071(id,id,id);

--行存表 gist索引
drop index if exists index_01;
create index index_01 on test_index_071 using gist(id,id,id);

--列存表 btree索引
drop table if exists test_index_071;
create temporary table test_index_071(id int) with (orientation=column);
drop index if exists index_01;
create index index_01 on test_index_071 using btree(id,id,id);

--列存表 psort索引
drop index if exists index_01;
create index index_01 on test_index_071 using psort(id,id,id);

--行存表 gist索引
drop table if exists test_index_071;
create temporary table test_index_071(id text)with (orientation=row);
drop index if exists index_01;
create index index_01 on test_index_071 using gist(id,id,id);

--清理数据
drop table if exists test_index_071 cascade;
