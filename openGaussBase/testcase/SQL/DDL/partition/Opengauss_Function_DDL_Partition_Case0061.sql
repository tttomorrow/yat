-- @testpoint: 测试A表主键多个字段对应B表多个字段主键：合理报错
--建立外键表
drop table if exists pteacher_table_06 cascade;
drop table if exists pstudent_table_06 cascade;
create table pteacher_table_06
(
    t_date timestamp,
    t_day timestamp,
    t_name varchar not null,
    primary key (t_date, t_day)
)partition by range(t_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
create table pstudent_table_06
(
    s_date timestamp primary key,
    s_name varchar not null,
    t_date timestamp,
    t_day timestamp,
    CONSTRAINT FK_pstudent_table_06_1 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 on update cascade on delete set null
)partition by range(s_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
--插入数据
insert into pteacher_table_06 values (date '2020-09-01', date '2020-09-01', '张老师');
insert into pteacher_table_06 values (date '2020-09-02', date '2020-09-02', '李老师');
insert into pteacher_table_06 values (date '2020-09-03', date '2020-09-03', '陈老师');
--测试插入情况，只有主键全部字段都存在才能成功插入
--应当插入应当执行成功
insert into pstudent_table_06 values (date '2020-09-01', '王二', date '2020-09-01', date '2020-09-01');
insert into pstudent_table_06 values (date '2020-09-02', '张三', date '2020-09-02', date '2020-09-02');
insert into pstudent_table_06 values (date '2020-09-03', '吴五', date '2020-09-03', null);
select * from pstudent_table_06;
--外键约束中加入match full限制
delete from pstudent_table_06 where s_date = date '2020-09-03';
alter table pstudent_table_06 drop constraint FK_pstudent_table_06_1;
alter table pstudent_table_06 add constraint FK_pstudent_table_06_2 FOREIGN KEY (t_date, t_day) REFERENCES pteacher_table_06 MATCH FULL on update cascade on delete set null;
--以下插入应当执行失败
insert into pstudent_table_06 values (date '2020-09-04', '陈一', date '2020-09-02', date '2020-09-03');
insert into pstudent_table_06 values (date '2020-09-05', '李四', date '2020-09-03', null);
--测试update和delete情况
select * from pstudent_table_06;
update pteacher_table_06 set t_date = date '2020-09-09' where t_date = date '2020-09-01';
select * from pstudent_table_06;
delete from pteacher_table_06 where t_day = date '2020-09-01';
select * from pstudent_table_06;

drop table if exists pstudent_table_06 cascade;
drop table if exists pteacher_table_06 cascade;