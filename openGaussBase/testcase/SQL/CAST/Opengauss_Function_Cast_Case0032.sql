-- @testpoint: 单目操作符
-- @testpoint: 合理报错

CREATE or replace FUNCTION test_cast_fun_0032(integer) RETURNS name
    AS 'select typname from pg_type where oid = $1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/

--testpoint:单目操作符 - 取反：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='-' and oprkind != 'b';

explain performance select - 32::int8;
explain performance select - -32::int4;
explain performance select - 32::int2;
explain performance select - -32.32::float4;
explain performance select - 32.32::float8;
explain performance select - -8::interval;
explain performance select - 32.32::numeric;

--testpoint:单目操作符 @ 取绝对值：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='@' and oprkind != 'b';

explain performance select @ 32::int8;
explain performance select @ -32::int4;
explain performance select @ 32::int2;
explain performance select @ -32.32::float4;
explain performance select @ 32.32::float8;
explain performance select @ -32.32::numeric;

--testpoint:单目操作符 @@ 取中心点：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='@@' and oprkind != 'b';

explain performance select @@ box '(1,1),(2,2)';
explain performance select @@ lseg '(1,2),(3,2)';
--合理报错:暂未实现path_center函数
explain performance select @@ path '1,1,2,2,3,3,4,4';
explain performance select @@ polygon '1,1,2,2,3,3,4,4';
explain performance select @@ circle '((1,1)5)';

--testpoint:单目操作符 !! ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='!!' and oprkind != 'b';

explain performance select !! 32::int8;
explain performance select !! 'fat:ab & cat'::tsquery;

--testpoint:单目操作符 ~ “非”操作：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='~' and oprkind != 'b';

explain performance select ~ '08:00:2b:01:02:03'::macaddr;
explain performance select ~ inet '0.0.0.0/24';
explain performance select ~ inet '2001:4f8:3:ba::/64';
explain performance select ~ '101'::bit;
explain performance select ~ 32::int2;
explain performance select ~ 32::int4;
explain performance select ~ 32::int8;

--testpoint:单目操作符 # ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='#' and oprkind != 'b';

explain performance select # path '1,1,2,2,3,3,4,4';
explain performance select # polygon '1,1,2,2,3,3,4,4';

--testpoint:单目操作符 +：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='+' and oprkind != 'b';

explain performance select + 32::int2;
explain performance select + -32::int4;
explain performance select + 32::int8;
explain performance select + -32.32::float4;
explain performance select + 32.32::float8;
explain performance select + -32.32::numeric;

--testpoint:单目操作符 | ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='|' and oprkind != 'b';

explain performance select | tinterval(abstime 'May 10, 1947 23:59:12', abstime 'Mon May  1 00:30:30 1995');

--testpoint:单目操作符 ! ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='!' and oprkind != 'b';

explain performance select 32::int8 !;

--testpoint:单目操作符 |/ ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='|/' and oprkind != 'b';

explain performance select |/ 32.32::float8;

--testpoint:单目操作符 ||/ ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='||/' and oprkind != 'b';

explain performance select ||/ 32.32::float8;

--testpoint:单目操作符 @-@ ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o left join pg_proc p on p.oid=o.oprcode where oprname ='@-@' and oprkind != 'b';

explain performance select @-@ lseg '(1,2),(3,2)';
explain performance select @-@ path '1,1,2,2,3,3,4,4';

--环境清理
drop function if exists test_cast_fun_0032(integer) cascade;
