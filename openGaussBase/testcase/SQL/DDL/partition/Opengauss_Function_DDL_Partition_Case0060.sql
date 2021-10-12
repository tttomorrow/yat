-- @testpoint: 测试A表外键对应A表主键:success
--建立外键表
drop table if exists pstudent_table_05 cascade;
create table pstudent_table_05
(
    s_date timestamp primary key,
    s_name varchar not null,
    m_date timestamp references pstudent_table_05 (s_date) on update cascade on delete set null
)partition by range(s_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
--添加数据
insert into pstudent_table_05 values (date '2020-09-01', '张三', date '2020-09-01');
insert into pstudent_table_05 values (date '2020-09-02', '李四', date '2020-09-02');
insert into pstudent_table_05 values (date '2020-09-03', '王二', date '2020-09-03');
--测试delete和update结果
select * from pstudent_table_05;
update pstudent_table_05 set s_date = date '2020-09-09' where s_date = date '2020-09-01';
select * from pstudent_table_05;
delete pstudent_table_05 where s_date = date '2020-09-02';
select * from pstudent_table_05;
drop table if exists pstudent_table_05;
