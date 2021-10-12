-- @testpoint: NULLIF 合理报错
--只有当value1和value2相等时，NULLIF才返回NULL。否则它返回value1
--value1和value2为同一数据类型，覆盖相等和不相等

DROP TABLE if exists test_expression_08 cascade;
CREATE TABLE test_expression_08 (
    NI_VALUE1 VARCHAR(10),
    NI_VALUE2 VARCHAR(10)
);
INSERT INTO test_expression_08 VALUES('abc', 'abc');
INSERT INTO test_expression_08 VALUES('abc', 'efg');

SELECT NI_VALUE1, NI_VALUE2, NULLIF(NI_VALUE1, NI_VALUE2) FROM test_expression_08 ORDER BY 1, 2, 3;

--如果value1等于value2则返回NULL，否则返回value1。
SELECT NULLIF('Hello','Hello World');
SELECT NULLIF('Hello','Hello');
SELECT NULLIF(1::int,2.2::int);
SELECT NULLIF(1::int,1::int);
SELECT NULLIF('7.7'::money,'7.7'::money);
SELECT NULLIF('7.7'::money,'7.8'::money);
SELECT NULLIF('2020-10-13'::timestamp,'2020-10-13'::timestamp);
SELECT NULLIF('2020-10-13',current_date);
SELECT NULLIF(lseg '(1,2),(3,2)',lseg '(1,2),(3,2)');
SELECT NULLIF(lseg '(1,2),(3,2)',lseg '(1,2),(3,2)');
SELECT NULLIF(inet '0.0.0.0/24',inet '0.0.0.0/24');
SELECT NULLIF(inet '0.0.0.0/24',inet '0.0.0.8/24');
SELECT NULLIF('The Fat Rats'::tsvector,'The Fat Rats'::tsvector);
SELECT NULLIF('The Fat Rats'::tsvector,'Fat Rats'::tsvector);

--value1和value2为不同数据类型，覆盖相等和不相等
SELECT NULLIF(1::int,2.2::varchar);
SELECT NULLIF(1::int,1::varchar);
SELECT NULLIF('7.7'::money,'7.7'::int);
SELECT NULLIF('7.7'::money,'7.7'::float);
SELECT NULLIF('2020-10-13'::timestamp,'The Fat Rats'::tsvector);
SELECT NULLIF(lseg '(1,2),(3,2)',inet '0.0.0.0/24');

--value和null值
SELECT NULLIF('Hello',' ');
SELECT NULLIF('Hello','');
SELECT NULLIF('Hello',NULL);
SELECT NULLIF(' ','Hello');
SELECT NULLIF('','Hello');
SELECT NULLIF(NULL,'Hello');

--多参少参无参
SELECT NULLIF('Hello','Hello World','Hello');
SELECT NULLIF('Hello');
SELECT NULLIF();

--清理环境
DROP TABLE if exists test_expression_08 cascade;
