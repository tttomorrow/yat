-- @testpoint: jsonb额外支持操作函数：jsonb_gt(greater than(>)。大于，判断两个jsonb是不是左边大于右边,输入不合理，合理报错）
-- 比较规则:object-jsonb > array-jsonb > bool-jsonb > num-jsonb > str-jsonb > null-jsonb

--同类型
select jsonb_gt('"str"','"string"');
select jsonb_gt('null','null' );
select jsonb_gt('false','false');
select jsonb_gt('false','true');
select jsonb_gt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','{"b":[10,2,3]}');
select jsonb_gt('[null, false, 123,{"a":true},"test"]','[123,{"a":false},"test",null, false]');
select jsonb_gt('105.2e-3','1.0520e-1');

--不同类型
select jsonb_gt('"str"', 'null');
select jsonb_gt('null','true' );
select jsonb_gt('null','0' );
select jsonb_gt('null', '{"b":[10,2,3]}');
select jsonb_gt('null','[12,"test",null, false]');
select jsonb_gt('true','1');
select jsonb_gt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','[{"b":[10,2,3]},{"a":1},{"c":{"b":"d"}}]');
select jsonb_gt('[{"a":false},{"a":true}]','{"a": true,"a": false}');
select jsonb_gt('105.2e3','"0.1052"');
select jsonb_gt('0','false');
select jsonb_gt('258','{"a":258}');
select jsonb_gt('0.369','[0.369]');
select jsonb_gt('"true"','true' );
select jsonb_gt('"true"','{"a":"true"}' );
select jsonb_gt('"true"','["true"]' );
select jsonb_gt('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','true');
select jsonb_gt('[{"a":false},{"a":true}]','false');

--入参非jsonb
select jsonb_gt('{a:1, b: [10,2,3],c:{b:d}}','true');
select jsonb_gt('{a:1, a: [10,2,3],a:{b:d}}','{a:1}');
select jsonb_gt('[{a:false},{a:true},123,'qwer','null']','{"a":false}');
select jsonb_gt('[{a:false},{a:true},123,'qwer','null']','123');
select jsonb_gt('[{a:false},{a:true},123,'qwer','null']','qwer');
select jsonb_gt('[{a:false},{a:true},123,'"qwer"','null']','qwer');