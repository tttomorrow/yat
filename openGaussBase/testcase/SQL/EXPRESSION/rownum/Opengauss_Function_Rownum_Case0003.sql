-- @testpoint: 测试rownum在组合查询中的表现

drop table if exists t_rownum_0003_01;
drop table if exists t_rownum_0003_02;
create table t_rownum_0003_01
(
    s_id int primary key,
    s_name varchar(10) not null
);
create table t_rownum_0003_02
(
    t_id int primary key,
    t_name varchar(10) not null
);
insert into t_rownum_0003_01 values (2017100001, 'aaa');
insert into t_rownum_0003_01 values (2017100002, 'bbb');
insert into t_rownum_0003_01 values (2017100003, 'ccc');
insert into t_rownum_0003_01 values (2017100004, 'ddd');
insert into t_rownum_0003_01 values (2017100005, 'eee');
insert into t_rownum_0003_01 values (2017100006, 'fff');
insert into t_rownum_0003_02 values (2017100005, 'eee');
insert into t_rownum_0003_02 values (2017100006, '222');
insert into t_rownum_0003_02 values (2017100007, 'aaa');
insert into t_rownum_0003_02 values (2017100008, '444');
insert into t_rownum_0003_02 values (2017100009, '555');
insert into t_rownum_0003_02 values (2017100010, '666');
--测试点1：union
--简单的情况，包含子查询和union all，重复信息能得以保留
select rownum, * from (select * from t_rownum_0003_01 union all select * from t_rownum_0003_02) as result where rownum < 8;
--复杂一点了，子查询中包含了对rownum的限定，并且对union后的结果进行了rownum的限定
select rownum, * from (select * from t_rownum_0003_01 where rownum < 3 union select * from t_rownum_0003_02 where rownum != 4 order by 1 asc) as result where rownum != 3;
--再看下子查询中指定了别名，且union后的结果通过别名重新过滤，并对最终结果的rownum进行限定
select rownum, * from (select rownum rowno, * from t_rownum_0003_01 union all select rownum rowno, * from t_rownum_0003_02) as result where (rowno < 3 or rowno != 5) and rownum < 9;
--测试点2：intersect
--简单的测试下子查询中包含intersect all
select rownum, * from (select * from t_rownum_0003_01 intersect all select * from t_rownum_0003_02) as result where rownum <= 2;
--测试下包含了子查询rownum限定、排序，最终结果rownum限定的情况，和上面类似
select rownum, * from (select * from t_rownum_0003_01 where rownum != 6 intersect select * from t_rownum_0003_02 where rownum <= 3) as result where rownum != 2;
select rownum, * from (select * from t_rownum_0003_01 where rownum != 6 intersect select * from t_rownum_0003_02 where rownum <= 4 order by 1 asc) as result where rownum != 2;
--测试点3：except
--简单测试下except的基本功能
select rownum, * from (select * from t_rownum_0003_01 where rownum != 7 except select * from t_rownum_0003_01 where rownum <= 2) as result where rownum <= 3 order by s_id;
--测试下子查询结果排序，最终结果根据rownum再排序
select rownum, * from (select * from t_rownum_0003_01 where rownum <= 3 except select * from t_rownum_0003_01 where rownum != 2 order by 1 asc) as result order by s_id desc;
--测试点4：minus
--简单测试下minus基本功能（minus和except功能是一致的）
select rownum, * from (select rownum rowno, * from t_rownum_0003_01 where rownum != 7 minus select rownum rowno, * from t_rownum_0003_01 where rownum <= 3) where rowno >= 5 order by s_id;
--继续组合，测试下两层minus后的结果
select rownum, * from (select * from t_rownum_0003_01 minus select * from (select * from t_rownum_0003_01 where rownum != 7 minus select * from t_rownum_0003_01 where rownum <= 2) where rownum <= 2) order by s_id desc;
--针对上一个SQL颠倒下相减的顺序
select rownum, * from (select * from (select * from t_rownum_0003_01 where rownum != 7 minus select * from t_rownum_0003_01 where rownum <= 2) where rownum <= 2 minus select * from t_rownum_0003_01) order by 1 desc;

drop table if exists t_rownum_0003_01;
drop table if exists t_rownum_0003_02;
