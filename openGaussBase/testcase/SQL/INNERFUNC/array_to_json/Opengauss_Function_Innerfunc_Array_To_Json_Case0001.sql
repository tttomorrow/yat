--  @testpoint: --array_to_json(anyarray [, pretty_bool])描述：返回JSON类型的数组。一个多维数组成为一个JSON数组的数组。--如果pretty_bool为true，将在一维元素之间添加换行符。返回类型：json
SELECT array_to_json('{{1,5},{99,100}}'::TINYINT[]);
SELECT array_to_json('{{1,5},{99,100}}'::SMALLINT[]);
SELECT array_to_json('{{1,5},{99,100}}'::INTEGER[]);
SELECT array_to_json('{{1,5},{99,100}}'::BINARY_INTEGER[]);
SELECT array_to_json('{{1,5},{99,100}}'::bigint[]);
SELECT array_to_json('{{1.1,5.5},{99.9,100.99}}'::REAL[]);