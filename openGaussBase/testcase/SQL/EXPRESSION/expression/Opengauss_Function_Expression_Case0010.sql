-- @testpoint: NVL 合理报错
--如果value1为NULL则返回value2，如果value1非NULL，则返回value1

--value1为null，返回value2，否则返回value1，覆盖常用数据类型
SELECT nvl(null,1);
SELECT nvl(null,1::int);
SELECT nvl(null,'test'::varchar);
SELECT nvl(null,'test'::clob);
SELECT nvl(null,'test'::text);
SELECT nvl(null,'3 days'::reltime);
SELECT nvl(1,null);
SELECT nvl(1::int,null);
SELECT nvl('test'::varchar,null);
SELECT nvl('test'::clob,null);
SELECT nvl('test'::text,null);
SELECT nvl('3 days'::reltime,null);

--不支持的数据类型：合理报错
SELECT nvl(null,B'10101'::bit(5));
SELECT nvl(null,'false'::boolean);
SELECT nvl(null,inet '0.0.5.0/24'::cidr);
SELECT nvl(null,lseg '(1,2),(3,2)');

--value1value2均为null
SELECT nvl(null,null);
SELECT nvl('','');

--多参少参无参
SELECT nvl(1,2,3,4,5);
SELECT nvl(1,2,3);
SELECT nvl(null);
SELECT nvl('test');
SELECT nvl();

--清理环境
--no need to clean
