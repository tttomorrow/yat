-- @testpoint: 推迟检查约束，在commit时合理报错
--建立外键表，加入推迟检查约束
drop table if exists pstudent_table_03 cascade;
drop table if exists pteacher_table_03 cascade;
create table pteacher_table_03
(
    t_date timestamp primary key,
    t_name varchar not null
)partition by range(t_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));
create table pstudent_table_03
(
    s_date timestamp,
    s_name varchar not null,
    t_date timestamp REFERENCES pteacher_table_03 deferrable initially deferred
)partition by range(t_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));
--添加数据
INSERT INTO pteacher_table_03 VALUES (date '2020-09-01', '李老师');
INSERT INTO pstudent_table_03 VALUES (date '2020-09-01', '张三', date '2020-09-01');
--测试推迟检查约束，应当在commit时报错
START TRANSACTION;
INSERT INTO pstudent_table_03 VALUES (date '2020-09-04', '李四', date '2020-09-04');
update pstudent_table_03 set s_date = date '2020-09-09';
COMMIT;
select * from pstudent_table_03;

drop table if exists pstudent_table_03 cascade;
drop table if exists pteacher_table_03 cascade;

