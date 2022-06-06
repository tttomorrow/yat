-- @testpoint: 二目运算符
--创建函数
CREATE or replace FUNCTION test_cast_fun_0032(integer) RETURNS name
    AS 'select typname from pg_type where oid = $1;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;
/

--testpoint:二目操作符  = ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o
left join pg_proc p on p.oid=o.oprcode
where oprname ='=' and oprkind = 'b' order by test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int), test_cast_fun_0032(oprresult::int) asc;

explain performance select '2020-09-30'::abstime = '2020-09-30'::abstime;
explain performance select true = false;
explain performance select 'test'::text = 'test'::clob;
explain performance select circle '((1,1)5)' = circle '((1,1)5)';
explain performance select 21::int4 = 21::int8;
explain performance select 1::bool = 1::bool;
explain performance select '21'::char = '21'::char;
explain performance select '21'::name = '21'::name;
explain performance select 21::int2 = 21::int2;
explain performance select 21::int4 = 21::int4;
explain performance select '21'::text = '21'::text;
explain performance select '212121'::xid = '212121'::xid;
explain performance select '212121'::xid = '212121'::int8;
explain performance select '212121'::xid32 = '212121'::xid32;
explain performance select '212121'::xid32 = '212121'::int4;
explain performance select '212121'::cid = '212121'::cid;
explain performance select '212'::int2vector = '212'::int2vector;
explain performance select 21::int8 = 21::int8;
explain performance select 21::int8 = 21::int4;
explain performance select box '(1,1),(2,2)'::box = box '(1,1),(2,2)'::box;
explain performance select 21::int2 = 21::int4;
explain performance select 21::int4 = 21::int2;
explain performance select '2020-09-29'::abstime = '2020-09-29'::abstime;
explain performance select 21::reltime = 21::reltime;
explain performance select 21::oid = 21::oid;
explain performance select 0.21::float4 = 0.21::float4;
explain performance select '21'::oidvector = '21'::oidvector;
explain performance select 0.21::float8 = 0.21::float8;
explain performance select path '(1,1),(2,2),(3,3),(4,4)'::path = path '(1,1),(2,2),(3,3),(4,4)'::path;
explain performance select 21.21::money = 21.21::money;
explain performance select '$ 21.21::money' = '$ 21.20::money';
explain performance select 21::bpchar = 21::bpchar;
explain performance select '2020-09-29'::date = '2020-09-29'::date;
explain performance select 0.21::float4 = 0.21::float8;
explain performance select 0.21::float8 = 0.21::float4;
explain performance select '0.0.0.0/24'::inet = '0.0.0.0/24'::inet;
explain performance select '2020-09-29'::timestamptz = '2020-09-29'::timestamptz;
explain performance select 21::interval = 21::interval;
explain performance select circle '1,1,5'::circle = circle '1,1,5'::circle;
explain performance select lseg '(1,2),(3,2)'::lseg = lseg '(1,2),(3,2)'::lseg;
explain performance select 0.21::numeric = 0.21::numeric;
explain performance select B'1'::bit = B'1'::bit;
explain performance select B'1'::varbit = B'1'::varbit;
explain performance select 21::int2 = 21::int8;
explain performance select 21::int8 = 21::int2;
explain performance select '2020-09-29'::timestamp = '2020-09-29'::timestamp;
explain performance select '2020-09-29'::date = '2020-09-29'::timestamp;
explain performance select '2020-09-29'::date = '2020-09-29'::timestamptz;
explain performance select '2020-09-29'::timestamp = '2020-09-29'::date;
explain performance select '2020-09-29'::timestamptz = '2020-09-29'::date;
explain performance select '2020-09-29'::timestamp = '2020-09-29'::timestamptz;
explain performance select '2020-09-29'::timestamptz = '2020-09-29'::timestamp;
explain performance select HEXTORAW('DEADBEEF')::raw = HEXTORAW('DEADBEEF')::raw;
explain performance select 21::int1 = 21::int1;
explain performance select '2020-09-29'::smalldatetime = '2020-09-29'::smalldatetime;
explain performance select '[105.2e3,"test",{"a":1}]'::jsonb = '[105.2e3,"test",{"a":1}]'::jsonb;
explain performance select '[105.2e3,"test",{"a":1}]'::jsonb = '[107.2e3,"test",{"a":1}]'::jsonb;

--testpoint:二目操作符  <= ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o
left join pg_proc p on p.oid=o.oprcode
where oprname ='<=' and oprkind = 'b' order by test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int) asc;

explain performance select '2020-09-29'::date <= '2020-09-30'::timestamp;
explain performance select true <= false;
explain performance select 'test'::varchar <= 'test'::clob;
explain performance select circle '((1,1)5)' <= circle '((1,1)5)';
explain performance select '[105.2e3,"test",{"a":1}]'::jsonb <= '[105.2e3,"test",{"a":1}]'::jsonb;
explain performance select '[109.2e3,"test",{"a":1}]'::jsonb <= '[105.2e3,"test",{"a":1}]'::jsonb;

--testpoint:二目操作符  >= ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o
left join pg_proc p on p.oid=o.oprcode
where oprname ='>=' and oprkind = 'b' order by test_cast_fun_0032(oprleft::int) ,test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int)asc;

explain performance select '2020-09-29'::date >= '2020-09-30'::timestamp;
explain performance select true >= false;
explain performance select 'test'::varchar >= 'test'::clob;
explain performance select circle '((1,1)5)' >= circle '((1,1)5)';
explain performance select '[105.2e3,"test",{"a":1}]'::jsonb >= '[105.2e3,"test",{"a":1}]'::jsonb;
explain performance select '[101.2e3,"test",{"a":1}]'::jsonb >= '[105.2e3,"test",{"a":1}]'::jsonb;

--testpoint:二目操作符  @@@ ：success
select oprname,oprkind,test_cast_fun_0032(oprleft::int),test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int),proname from pg_operator o
left join pg_proc p on p.oid=o.oprcode
where oprname ='@@@' and oprkind = 'b' order by test_cast_fun_0032(oprleft::int) ,test_cast_fun_0032(oprright::int),test_cast_fun_0032(oprresult::int)asc;

explain performance SELECT to_tsvector('fat cats ate rats') @@@ to_tsquery('cat & rat');

--环境清理
drop function if exists test_cast_fun_0032(integer) cascade;