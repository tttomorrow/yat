-- @testpoint: 检测是否支持不同约束等级下的外键操作：合理报错
--行存
drop table if exists pstudent_table_02 cascade;
drop table if exists pclass_table_02 cascade;
drop table if exists pteacher_table_02 cascade;

create table pclass_table_02
(
    c_date TIMESTAMP primary key,
    c_name varchar not null
)partition by range(c_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));


create table pteacher_table_02
(
    t_date TIMESTAMP primary key,
    t_name varchar not null
)partition by range(t_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));

create table pstudent_table_02
(
    s_date TIMESTAMP primary key,
    s_name varchar not null,
    c_date TIMESTAMP,
    t_date TIMESTAMP,
    foreign key(c_date) references pclass_table_02(c_date)
)partition by range(s_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));

--添加数据
insert into pclass_table_02 values (date '2020-09-01', '1年1班');
insert into pclass_table_02 values (date '2020-09-02', '1年2班');
insert into pclass_table_02 values (date '2020-09-03', '1年3班');
insert into pclass_table_02 values (date '2020-09-04', '1年4班');
insert into pteacher_table_02 values (date '2020-09-01', '李老师');
insert into pteacher_table_02 values (date '2020-09-02', '张老师');
insert into pteacher_table_02 values (date '2020-09-03', '陈老师');
insert into pteacher_table_02 values (date '2020-09-04', '杨老师');
insert into pstudent_table_02 values (date '2020-09-01', '张三', date '2020-09-01', date '2020-09-01');
insert into pstudent_table_02 values (date '2020-09-02', '李四', date '2020-09-02', date '2020-09-02');
insert into pstudent_table_02 values (date '2020-09-03', '王二', date '2020-09-03', date '2020-09-03');
insert into pstudent_table_02 values (date '2020-09-04', '李明', date '2020-09-04', date '2020-09-04');

--增加外键约束
alter table pstudent_table_02 add constraint fk_student_tid foreign key (t_date)
references pteacher_table_02(t_date) on delete set null on update no action;

alter table pstudent_table_02 add constraint fk_student_cid foreign key (c_date)
references pclass_table_02(c_date) on delete cascade on update restrict;

--查看PG_CONSTRAINT表中情况
select conname, convalidated, confupdtype, confdeltype, confmatchtype
from PG_CONSTRAINT where conname in ('fk_student_tid', 'fk_student_cid');

--测试delete set null
select * from pstudent_table_02;
delete from pteacher_table_02 where t_date = date '2020-09-04';
select * from pstudent_table_02;

--测试delete cascade
delete from pclass_table_02 where c_date = date '2020-09-04';
select * from pstudent_table_02;

--测试update & no action
update pteacher_table_02 set t_date = date '2020-09-09' where t_date = date '2020-09-04';
select * from pstudent_table_02;

--测试update & restrict ：合理报错
update pclass_table_02 set c_date = date '2020-09-09' where c_date = date '2020-09-04';
select * from pstudent_table_02;

--外键约束更新
alter table pstudent_table_02 drop constraint fk_student_cid;
alter table pstudent_table_02 drop constraint fk_student_tid;
alter table pstudent_table_02 add constraint fk_pstudent_table_02_tdate foreign key (t_date) references pteacher_table_02(t_date) on delete no action on update cascade;
alter table pstudent_table_02 add constraint fk_pstudent_table_02_cdate foreign key (c_date) references pclass_table_02(c_date) on delete restrict on update set null;

--测试delete & no action
delete from pteacher_table_02 where t_date = date '2020-09-04';
select * from pstudent_table_02;
--测试delete & restrict ：合理报错
delete from pclass_table_02 where c_date = date '2020-09-04';
select * from pstudent_table_02;
--测试update & cascade
update pteacher_table_02 set t_date = date '2020-09-04' where t_date = date '2020-09-08';
select * from pstudent_table_02;
--测试update & set null
update pclass_table_02 set c_date = date '2020-09-04' where c_date = date '2020-09-08';
select * from pstudent_table_02;

--测试PG_CONSTRAINT表中情况
select conname, convalidated, confupdtype, confdeltype, confmatchtype
from PG_CONSTRAINT where conname in ('fk_pstudent_table_02_tdate', 'fk_pstudent_table_02_cdate');

--删除外键表
drop table pclass_table_02 cascade;
drop table pteacher_table_02 cascade;
drop table pstudent_table_02 cascade;
