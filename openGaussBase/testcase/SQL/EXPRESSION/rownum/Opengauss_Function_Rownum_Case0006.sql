-- @testpoint: 测试rownum在子查询/子链接中的表现

drop table if exists t_rownum_0006;
create table t_rownum_0006
(
    s_id int primary key,
    s_name varchar(10) not null
);
insert into t_rownum_0006 values (2017100001, 'aaa');
insert into t_rownum_0006 values (2017100002, 'bbb');
insert into t_rownum_0006 values (2017100003, 'ccc');
insert into t_rownum_0006 values (2017100004, 'ddd');
insert into t_rownum_0006 values (2017100005, 'eee');
insert into t_rownum_0006 values (2017100006, 'fff');
--测试点1：两层子链接
select * from t_rownum_0006 where s_id in (select s_id from t_rownum_0006 where rownum < 3 union select s_id from t_rownum_0006 where rownum != 5) order by s_id;
--测试点2：三层子查询/子链接混用
select * from t_rownum_0006 where s_id in (select s_id from t_rownum_0006 where rownum < 3 union select * from (select s_id from t_rownum_0006 order by 1 desc) as result where rownum != 5) order by s_id;
drop table if exists t_rownum_0006;
