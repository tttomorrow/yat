-- @testpoint: GREATEST和LEAST 合理报错
--从一个任意数字表达式的列表里选取最大的数值和最小值

--参数均为null
SELECT greatest(NULL,null,'') as result;
SELECT LEAST(NULL,null,'') as result;

--参数中含有null但不全为null
SELECT greatest(9.888::float,'555','',null) as result;
SELECT LEAST(9.888::float,'555','',null) as result;
SELECT greatest('true'::boolean,'false'::boolean,null) as result;
SELECT least('true'::boolean,'false'::boolean,null) as result;

--可进行比较
SELECT greatest(629.888::clob,'555'::varchar,'999',549.9841::text) as result;
SELECT LEAST(629.888::clob,'555'::varchar,'999',549.9841::text) as result;
SELECT greatest(932.888::smallint,952.888::int,25.88::tinyint,894.888::bigint) as result;
SELECT least(932.888::smallint,952.888::int,29.888::tinyint,894.888::bigint) as result;
SELECT greatest(inet '0.0.0.0/24',inet '0.0.5.0/24'::cidr,'08:00:2b:01:02:03'::macaddr) as result;
SELECT least('2020-10-13','2020-10-14 pst','2020-10-15',current_date) as result;
SELECT greatest(inet '0.0.0.0/24',inet '0.0.5.0/24'::cidr) as result;
SELECT least(inet '0.0.0.0/24',inet '0.0.5.0/24'::cidr) as result;
SELECT greatest('true'::boolean,'false'::boolean) as result;
SELECT least('true'::boolean,'false'::boolean) as result;

--无法比较：合理报错
SELECT greatest(inet '0.0.0.0/24',inet '0.0.5.0/24'::cidr,'08:00:2b:01:02:03'::macaddr) as result;
SELECT least(inet '0.0.0.0/24',inet '0.0.5.0/24'::cidr,'08:00:2b:01:02:03'::macaddr) as result;
SELECT greatest(629.888::clob,'555'::int,'999',549.9841::text) as result;
SELECT least(629.888::clob,'555'::int,'999',549.9841::text) as result;
SELECT greatest(lseg '(1,2),(3,2)',lseg '(1,2),(3,8)',lseg '(1,2),(3,9)') as result;
SELECT least(lseg '(1,2),(3,2)',lseg '(1,2),(3,8)',lseg '(1,2),(3,9)') as result;

--1参和无参
SELECT greatest(549.9841::int) as result;
SELECT LEAST(549.9841::int) as result;
SELECT greatest() as result;
SELECT LEAST() as result;

--清理环境
--no need to clean
