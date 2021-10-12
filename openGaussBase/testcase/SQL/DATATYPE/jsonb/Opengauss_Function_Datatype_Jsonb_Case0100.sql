-- @testpoint: jsonb额外支持操作函数：jsonb_lt(little than(<),小于。判断两个jsonb是不是左边小于右边,输入不合理，合理报错）
-- 比较规则:object-jsonb > array-jsonb > bool-jsonb > num-jsonb > str-jsonb > null-jsonb

--同类型
select jsonb_lt('"str"','"string"');
select jsonb_lt('null','null' );
select jsonb_lt('false','false');
select jsonb_lt('false','true');
select jsonb_lt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','{"b":[10,2,3]}');
select jsonb_lt('[null, false, 123,{"a":true},"test"]','[123,{"a":false},"test",null, false]');
select jsonb_lt('105.2e-3','1.0520e-1');

--不同类型
select jsonb_lt('"str"', 'null');
select jsonb_lt('null','true' );
select jsonb_lt('null','0' );
select jsonb_lt('null', '{"b":[10,2,3]}');
select jsonb_lt('null','[12,"test",null, false]');
select jsonb_lt('true','1');
select jsonb_lt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','[{"b":[10,2,3]},{"a":1},{"c":{"b":"d"}}]');
select jsonb_lt('[{"a":false},{"a":true}]','{"a": true,"a": false}');
select jsonb_lt('105.2e3','"0.1052"');
select jsonb_lt('0','false');
select jsonb_lt('258','{"a":258}');
select jsonb_lt('0.369','[0.369]');
select jsonb_lt('"true"','true' );
select jsonb_lt('"true"','{"a":"true"}' );
select jsonb_lt('"true"','["true"]' );
select jsonb_lt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','true');
select jsonb_lt('[{"a":false},{"a":true}]','false');

--入参非jsonb
select jsonb_lt('{a:1, b: [10,2,3],c:{b:d}}','true');
select jsonb_lt('{a:1, a: [10,2,3],a:{b:d}}','{a:1}');
select jsonb_lt('[{a:false},{a:true},123,'qwer','null']','{"a":false}');
select jsonb_lt('[{a:false},{a:true},123,'qwer','null']','123');
select jsonb_lt('[{a:false},{a:true},123,'qwer','null']','qwer');
select jsonb_lt('[{a:false},{a:true},123,'"qwer"','null']','qwer');