-- @testpoint: JSON函数和jsonb

--array_to_json:返回JSON类型的数组
select array_to_json('{{1,5},{99,100}}'::jsonb[]);
select array_to_json('{{"1","5"},{"99","100"}}'::jsonb[]);
select array_to_json('{{null,true},{"null",false}}'::jsonb[]);
select array_to_json('{{"null","true"},{"null","false"}}'::jsonb[]);
select array_to_json('{{\"aaa\",\"bbb\"},{\"ccc\",\"ddd\"}}'::jsonb[]);

--row_to_json:返回JSON类型的行
select row_to_json(row('1','"foo"'));
select row_to_json(row('1','0.58'));
select row_to_json(row('"AAA"','null'));
select row_to_json(row('AAA','null'));
select row_to_json(row('true','"false"'));
select row_to_json(row('[true,111,aaa,null]','"false"'));
select row_to_json(row('{true:1}','{false:0}'));