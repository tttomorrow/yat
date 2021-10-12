-- @testpoint: 测试修改物化视图，合理报错

--修改物化视图
drop table if exists student cascade;
drop user if exists mv_test;
create table student
(
    id int primary key,
    name varchar(10) not null
);
insert into student values (1, 'aaa');
insert into student values (2, 'bbb');
insert into student values (3, 'ccc');
insert into student values (4, 'ddd');
insert into student values (5, 'eee');
insert into student values (6, 'fff');
create materialized view student_mv (id, name) with (FILLFACTOR=60,COMPRESSION=NO) as select * from student;
select * from student_mv;
--修改物化视图action
--为后续的ANALYZE操作设置针对每列的统计收集目标
alter materialized view student_mv alter id set statistics 300;
alter materialized view student_mv alter column id set statistics percent 30;
--设置或重置每个属性的选项
alter materialized view student_mv alter id set (n_distinct=50);
alter materialized view student_mv alter column id reset (n_distinct);
--为一列设置存储模式
alter materialized view student_mv alter id set storage plain;
--为未来的cluster操作选择或移除默认索引
create unique index index_test on student_mv(name);
alter materialized view student_mv cluster on index_test;
alter materialized view student_mv set without cluster;
--设置或重置存储参数
alter materialized view student_mv set (FILLFACTOR=60,COMPRESSION=NO);
alter materialized view student_mv set (orientation=column);
alter materialized view student_mv reset (FILLFACTOR, COMPRESSION);
alter materialized view student_mv reset (orientation);
--修改物化视图属主
create user mv_test identified by 'test@123';
alter materialized view student_mv owner to mv_test;
alter materialized view student_mv owner to current_user;
alter materialized view student_mv owner to session_user;
--修改物化视图列名
alter materialized view student_mv rename column id to id_new;
select * from student_mv;
--修改物化视图名
alter materialized view student_mv rename to student_mv_new;
select * from student_mv_new;
--检查下对关键字的屏蔽，期望报错
alter materialized view student_mv rename column id to rownum;--error
alter materialized view student_mv rename to user;--error
--修改物化视图模式
drop schema if exists mv_schema cascade;
create schema mv_schema;
alter materialized view student_mv_new set schema mv_schema;
select schemaname, matviewname from pg_matviews where matviewname = 'student_mv_new';
--修改物化视图表空间
drop tablespace if exists mv_space;
create tablespace mv_space relative location 'postgres_tbs';
alter materialized view mv_schema.student_mv_new set tablespace mv_space;
select spcname from pg_tablespace where oid = (select reltablespace from pg_class where relname = 'student_mv_new');
--增加物化视图列
alter materialized view mv_schema.student_mv_new add column id_new;--error
--删除物化视图列
alter materialized view student_mv drop column id int;--error

drop materialized view mv_schema.student_mv_new cascade;
drop tablespace mv_space;
drop schema mv_schema;
drop user mv_test;
