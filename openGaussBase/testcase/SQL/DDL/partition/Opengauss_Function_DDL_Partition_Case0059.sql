-- @testpoint: 检测A表主键对应B表多个外键
--建立外键表
drop table if exists pteacher_table_04 cascade;
drop table if exists pstudent_table_04 cascade;
create table pteacher_table_04
(
    t_date timestamp primary key,
    t_name varchar not null
)partition by range(t_date) interval ('10 day') (
  partition part1 values less than ('1990-02-02 00:00:00'));
create table pstudent_table_04
(
    s_date timestamp,
    s_name varchar not null,
    yuwen_t_date timestamp REFERENCES pteacher_table_04 on update cascade on delete set null,
    shuxue_t_date timestamp REFERENCES pteacher_table_04 on update cascade on delete set null,
    yingyu_t_date timestamp REFERENCES pteacher_table_04 on update cascade on delete set null
)partition by range(s_date) interval ('10 day') (partition part1 values less than ('1990-02-02 00:00:00'));
--添加数据
INSERT INTO pteacher_table_04 VALUES (date '2020-09-01', '李老师');
INSERT INTO pteacher_table_04 VALUES (date '2020-09-02', '陈老师');
INSERT INTO pteacher_table_04 VALUES (date '2020-09-03', '张老师');
INSERT INTO pstudent_table_04 VALUES (date '2020-09-01', '张三', date '2020-09-01', null, null);
INSERT INTO pstudent_table_04 VALUES (date '2020-09-02', '李四', date '2020-09-02', date '2020-09-02', null);
INSERT INTO pstudent_table_04 VALUES (date '2020-09-03', '王二', date '2020-09-03', date '2020-09-03', date '2020-09-03');

SELECT * FROM pstudent_table_04;
update pteacher_table_04 set t_date = date '2020-09-09' where t_date = date '2020-09-03';
SELECT * FROM pstudent_table_04;
--delete set null  单独执行delete生效，在update之后执行delete不生效
DELETE FROM pteacher_table_04 WHERE t_date = date '2020-09-03';
SELECT * FROM pstudent_table_04;

--清理数据
drop table if exists pteacher_table_04 cascade;
drop table if exists pstudent_table_04 cascade;
