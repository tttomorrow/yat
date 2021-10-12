-- @testpoint: decode 合理报错
--只有当value1和value2相等时，NULLIF才返回NULL。否则它返回value1 合理报错

SELECT DECODE('A','A',1,'B',2,0);
--包含base_expr和1组compare，无default
SELECT DECODE('A','A',1,'B',2);
SELECT DECODE('A','B',2);
SELECT DECODE('A','A',1);

--包含base_expr和1组compare和default
SELECT DECODE('A','A',1,0);
SELECT DECODE('A','B',1,0);

--包含base_expr和多组compare和default
SELECT DECODE('A','B',1,'C',2,'D',3,'E',4,0);

--value和default为同一数据类型，覆盖常用数据类型
SELECT DECODE('A','A',1::int,'B',2::int, 7::int);
SELECT DECODE('A','A','7.7'::money,'B','8.7'::money, '9.7'::money);
SELECT DECODE('A','A1','2020-10-13'::timestamp,'B','2020-10-14'::timestamp, '2020-10-17'::date);
SELECT DECODE('A','A','true'::BOOLEAN, 'false'::BOOLEAN);
SELECT DECODE('A','A1',lseg '(1,2),(3,2)','B',lseg '(1,2),(3,2)', lseg '(1,2),(3,2)');
SELECT DECODE('A','A',inet '0.0.0.0/24','B',inet '0.0.0.1/24', inet '0.0.0.7/24');
SELECT DECODE('B','A','The Fat Rats'::tsvector,'B','The'::tsvector, 'Fat Rats'::tsvector);

--value和default为不同数据类型，合理报错
SELECT DECODE('A','A',1::int,'B',2::int, 7::money);
SELECT DECODE('A','A','true'::BOOLEAN, lseg '(1,2),(3,2)');
SELECT DECODE('A','A',inet '0.0.0.0/24','B',B'10101'::bit(5), inet '0.0.0.7/24');
SELECT DECODE('B','A','The Fat Rats'::tsvector,'B','The'::tsvector, 'Fat Rats'::varchar);

--少参无参:合理报错
SELECT DECODE('A','B');
SELECT DECODE();

--清理环境
--no need to clean
