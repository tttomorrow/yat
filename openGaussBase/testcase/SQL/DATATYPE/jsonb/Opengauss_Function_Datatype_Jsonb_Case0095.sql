-- @testpoint: jsonb额外支持操作函数：jsonb_cmp(比较两个jsonb的大小,输入不合理，合理报错）
-- 比较规则:object-jsonb > array-jsonb > bool-jsonb > num-jsonb > str-jsonb > null-jsonb

--同类型
select jsonb_cmp('"str"','"string"');
select jsonb_cmp('null','null' );
select jsonb_cmp('false','false');
select jsonb_cmp('false','true');
select jsonb_cmp('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','{"b":[10,2,3]}');
select jsonb_cmp('[null, false, 123,{"a":true},"test"]','[123,{"a":false},"test",null, false]');
select jsonb_cmp('105.2e-3','1.0520e-1');

--不同类型
select jsonb_cmp('"str"', 'null');
select jsonb_cmp('null','true' );
select jsonb_cmp('null','0' );
select jsonb_cmp('null', '{"b":[10,2,3]}');
select jsonb_cmp('null','[12,"test",null, false]');
select jsonb_cmp('true','1');
select jsonb_cmp('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','[{"b":[10,2,3]},{"a":1},{"c":{"b":"d"}}]');
select jsonb_cmp('[{"a":false},{"a":true}]','{"a": true,"a": false}');
select jsonb_cmp('105.2e3','"0.1052"');
select jsonb_cmp('0','false');
select jsonb_cmp('258','{"a":258}');
select jsonb_cmp('0.369','[0.369]');
select jsonb_cmp('"true"','true' );
select jsonb_cmp('"true"','{"a":"true"}' );
select jsonb_cmp('"true"','["true"]' );
select jsonb_cmp('{"a":1, "b": [10,2,3],"c":{"b":"d"}}','true');
select jsonb_cmp('[{"a":false},{"a":true}]','false');

--入参非jsonb
select jsonb_cmp('{a:1, b: [10,2,3],c:{b:d}}','true');
select jsonb_cmp('{a:1, a: [10,2,3],a:{b:d}}','{a:1}');
select jsonb_cmp('[{a:false},{a:true},123,'qwer','null']','{"a":false}');
select jsonb_cmp('[{a:false},{a:true},123,'qwer','null']','123');
select jsonb_cmp('[{a:false},{a:true},123,'qwer','null']','qwer');
select jsonb_cmp('[{a:false},{a:true},123,'"qwer"','null']','qwer');