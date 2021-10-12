-- @testpoint: 函数svals(hstore)，获取hstore中的值

select svals('"aa"=>"bb"');
select svals('a=>1,b=>2');
select svals('a=>1,b=>2,c=>3');

